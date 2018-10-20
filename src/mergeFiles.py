import pandas as pd


data1 = pd.read_csv('data/Building_Permits_in_2009.csv')
data2 = pd.read_csv('data/Building_Permits_in_2010.csv')
data3 = pd.read_csv('data/Building_Permits_in_2011.csv')
data4 = pd.read_csv('data/Building_Permits_in_2012.csv')
data5 = pd.read_csv('data/Building_Permits_in_2013.csv')
data6 = pd.read_csv('data/Building_Permits_in_2014.csv')
data7 = pd.read_csv('data/Building_Permits_in_2015.csv')
data8 = pd.read_csv('data/Building_Permits_in_2016.csv')
data9 = pd.read_csv('data/Building_Permits_in_2017.csv')
data10 = pd.read_csv('data/Building_Permits_in_2018.csv')


data = pd.concat([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])

data.to_csv('data/combined_Building_Permits.csv', index=False)
