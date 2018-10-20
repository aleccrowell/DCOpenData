import pandas as pd
import numpy as np
from osgeo import ogr

data = pd.read_csv("data/combined_Building_Permits.csv")

data = data[(data['PERMIT_TYPE_NAME'] == 'CONSTRUCTION') & (data['PERMIT_SUBTYPE_NAME'].isin(['ADDITION', 'ADDITION ALTERATION REPAIR', 'ALTERATION AND REPAIR',  'DEMOLITION', 'NEW BUILDING', 'RAZE']))]

coords = data.reset_index()[['index','LONGITUDE','LATITUDE']].values

tracts_shapefile = "data/Census_Tracts_in_2010.shp"

#from https://gis.stackexchange.com/questions/173020/convert-coordinates-to-census-tract-for-large-dataset
def getCensusTracts(long_lat_list, shapefile_name):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile_name, 0)
    layer = dataSource.GetLayer()
    results_dict = {}
    i = 0
    for feature in layer:
        geom = feature.GetGeometryRef()
        i += 1
        for pt in long_lat_list:
            gid = pt[0]
            lon = pt[1]
            lat = pt[2]
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(lon, lat)
            if point.Within(geom) == True:
                feat_id = feature.GetField("TRACT")
                if gid in results_dict and feat_id not in results_dict[gid]:
                    results_dict[gid].append(feat_id)
                else:
                    results_dict[gid] = [feat_id]
    for pt in long_lat_list:
        gid = pt[0]
        lon = pt[1]
        lat = pt[2]
        if gid not in results_dict:
            results_dict[gid] = ['NA']
    return results_dict


results_dict = getCensusTracts(coords, tracts_shapefile)
tracts = pd.DataFrame.from_dict(results_dict, orient='index')
tracts.columns = ['Census_Tract']
data = data.merge(tracts,right_index=True, left_index=True)

data = data[['ISSUE_DATE', 'LASTMODIFIEDDATE', 'PERMIT_SUBTYPE_NAME', 'LATITUDE', 'LONGITUDE', 'Census_Tract']]
data['ISSUE_DATE'] = data['ISSUE_DATE'].apply(lambda x: x.split('T')[0])
data['LASTMODIFIEDDATE'] = data['LASTMODIFIEDDATE'].apply(lambda x: x.split('T')[0])
data.to_csv('data/permits_processed.csv')

#############

crimes = pd.read_csv('data/dc-crimes.csv')
crimes['START_DATE'] = pd.to_datetime(crimes['START_DATE'], infer_datetime_format=True).dt.date
crimes['END_DATE'] = pd.to_datetime(crimes['END_DATE'], infer_datetime_format=True, errors='coerce').dt.date
crimes['REPORT_DAT'] = pd.to_datetime(crimes['REPORT_DAT'], infer_datetime_format=True).dt.date
crimes = crimes[['CENSUS_TRACT', 'offensegroup', 'END_DATE', 'SHIFT', 'START_DATE', 'OFFENSE', 'REPORT_DAT', 'METHOD', 'LONGITUDE', 'LATITUDE']]
crimes = crimes[np.isfinite(crimes['CENSUS_TRACT'])]
crimes['CENSUS_TRACT'] = crimes['CENSUS_TRACT'].apply(lambda x: np.int_(x))
crimes.to_csv('data/crimes_processed.csv')

