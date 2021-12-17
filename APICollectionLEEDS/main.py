from directions import getMapsDir
from weather import getMetWeather

from threading import Timer
import time
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df
import json
import ast
import pymysql
from AWSDBLEEDS import *

f = open('googleKey.json')
googleKey = json.load(f)['key']
f.close()

f = open('accuKey.json')
#accuKey = json.load(f)['key']
accuKey = ''
f.close()

f = open('MetKey.json')
MetKey = json.load(f)['key']
f.close()


def Store(newdata,outputfile):
    data = pd.read_csv('{filename}.csv'.format(filename=outputfile),index_col=0)
    
    update = df(newdata)

    data = pd.concat([data, update],axis=0,ignore_index=True)
    print(data)
    data.to_csv('{filename}.csv'.format(filename=outputfile))

def startAt10():
    while (datetime.now().minute%1) != 0:
        time.sleep(10)

weatherdict = {
        "Clear night" : 0,
        "Sunny day" : 1,
        "Partly cloudy (night)" : 2,
        "Partly cloudy (day)": 3,
        "Not used":4,
        "Mist":5,
        "Fog":6,
        "Cloudy":7,
        "Overcast":8,
        "Light rain shower (night)":9,
        "Light rain shower (day)":10,
        "Drizzle":11,
        "Light rain":12,
        "Heavy rain shower (night)":13,
        "Heavy rain shower (day)":14,
        "Heavy rain":15,
        "Sleet shower (night)":16,
        "Sleet shower (day)":17,
        "Sleet":18,
        "Hail shower (night)":19,
        "Hail shower (day)":20,
        "Hail":21,
        "Light snow shower (night)":22,
        "Light snow shower (day)":23,
        "Light snow":24,
        "Heavy snow shower (night)":25,
        "Heavy snow shower (day)":26,
        "Heavy snow":27,
        "Thunder shower (night)":28,
        "Thunder shower (day)":29,
        "Thunder":30
}

db, cursor = connect(rdslogin)
finddb(cursor, "LEEDS")
tablename = "LeedsTraffic"

if __name__ == "__main__":
    startAt10()
    newdata = {"datetime":[datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "Traffic":[0],
                    "Duration in Traffic":[0],
                    "Weather":[0],
                    "Temp": [0],
                    "mapsdata":[0],
                    }
    newdata['Weather'],newdata['Temp'] = getMetWeather(MetKey)
    newdata['Weather'] = weatherdict[str(newdata['Weather'])]
    print("ENTERING LOOP#####") ###########
    print(newdata['Weather'])
    while True:
        if ((datetime.now().minute%10 == 0) or (datetime.now().minute == 0)) & (datetime.now().minute != 50):
            ##function

            newdata["datetime"] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            try:
                newdata['Traffic'],newdata['Duration in Traffic'],newdata['mapsdata']  = getMapsDir(googleKey)
                print(newdata)
            except Exception as ex:
                print(ex)
                continue

            print("Storing") ###########
            insertrow(cursor,newdata,db,tablename)
            
            print("TIME:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(61)



        if datetime.now().minute == 50:
            ##function
            newdata["datetime"] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            try:
                newdata['Weather'],newdata['Temp'] = getMetWeather(MetKey)
                newdata['Weather'] = weatherdict[str(newdata['Weather'])]
                newdata['Traffic'],newdata['Duration in Traffic'],newdata['mapsdata']  = getMapsDir(googleKey)
            except Exception as ex:
                print(ex)
                continue

            print("Storing2") ###########
            print(newdata) ###########
            insertrow(cursor,newdata,db,tablename)
            
            print("TIME:" + datetime.now().strftime("%m/%d %H:%M:%S"))
            time.sleep(61)
        



