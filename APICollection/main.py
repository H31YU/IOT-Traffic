from directions import getMapsDir
from weather import getMetWeather

from threading import Timer
import time
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df
import json
import ast
outputfilename = "test"

f = open('googleKey.json')
googleKey = json.load(f)['key']
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


if __name__ == "__main__":
    startAt10()
    newdata = {"datetime":[datetime.now().strftime("%Y %m %d %H %M")],
                    "Traffic":[0],
                    "Duration in Traffic":[0],
                    "Weather":[0],
                    "Temp": [0],
                    "mapsdata":[0],
                    }
    newdata['Weather'],newdata['Temp'] = getMetWeather(MetKey)

    print("ENTERING LOOP") ###########

    while True:
        if ((datetime.now().minute%10 == 0) or (datetime.now().minute == 0)) & (datetime.now().minute != 50):
            ##function

            newdata["datetime"] = [datetime.now().strftime("%Y %m %d %H %M")]
            try:
                newdata['Traffic'],newdata['Duration in Traffic'],newdata['mapsdata']  = getMapsDir(googleKey)
                #print(newdata)
            except Exception as ex:
                print(ex)
                continue

            print("Storing") ###########
            Store(newdata,outputfilename)
            
            print("TIME:" + datetime.now().strftime("%m/%d %H:%M:%S"))
            time.sleep(61)



        if datetime.now().minute == 50:
            ##function
            newdata["datetime"] = [datetime.now().strftime("%Y %m %d %H %M")]
            try:
                newdata['Weather'],newdata['Temp'] = getMetWeather(MetKey)
                newdata['Traffic'],newdata['Duration in Traffic'],newdata['mapsdata']  = getMapsDir(googleKey)
            except Exception as ex:
                print(ex)
                continue

            print("Storing2") ###########
            Store(newdata,outputfilename)
            
            print("TIME:" + datetime.now().strftime("%m/%d %H:%M:%S"))
            time.sleep(61)
        



