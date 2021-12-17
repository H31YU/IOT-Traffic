import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df

#f = open('googleKey.json')

#data = json.load(f)

#print(data)

#f.close()


##test data

'''
year =datetime.now().year
month= datetime.now().month
day= datetime.now().day
hour = datetime.now().hour
minute = datetime.now().minute

newTraffic = {}
newTraffic[datetime.now().strftime("%Y %m %d %H %M %S")] = datetime.now().strftime("%Y %m %d %H %M")



with open('test.json', 'rb') as f:
    traffic = json.load(f)
    traffic.update(newTraffic)
f.close()


with open("test.json", "w") as outfile:
    json.dump(traffic, outfile)'''


traffic = pd.read_csv('test.csv',index_col=0)
#traffic = df()
#print(list(traffic.columns))


newTraffic = df({"Stamp":[datetime.now().strftime("%Y %m %d %H %M %S")],"data":[datetime.now().strftime("%Y %m %d %H %M")]})
#print(newTraffic)

traffic = pd.concat([traffic, newTraffic],axis=0,ignore_index=True)

print(traffic)
traffic.to_csv('test.csv')


