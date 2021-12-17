from analyser import analyser
from imganalyser import *
from TrafficCam import *
import timeit
import time
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df
import pymysql
from AWSDBLEEDScars import *
import requests

f = open('RDSlogin.json')
rdslogin = json.load(f)
f.close()

db, cursor = connect(rdslogin)
finddb(cursor, "LEEDS")
tablename = "Leedscars"

outputfilename = "cars"





#analyser(video, output)
def Store(newdata,outputfile):
    data = pd.read_csv('{filename}.csv'.format(filename=outputfile),index_col=0)
    
    update = df(newdata)

    data = pd.concat([data, update],axis=0,ignore_index=True)
    print(data)
    data.to_csv('{filename}.csv'.format(filename=outputfile))


if __name__=="__main__":
    newdata = {"datetime":[datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "cars":0,
                    }
    session = requests.session()
    sr = upscaler()
    last = datetime.now().strftime("%M")[0]
    counter = list(range(0,60))
    while True:
        last = datetime.now().strftime("%M")[0]
        while (datetime.now().strftime("%M")[0] == last):
            if (datetime.now().second%10 == 0):
                ##function
                #revivecam(session)
                time.sleep(1)
                newdata["datetime"] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                try:
                    frame = retrievecam(session)
                    result, num = imganalyse(frame,sr)
                    newdata['cars'] += num
                    counter.pop()
                    counter.insert(0,num)
                    update(cursor,sum(counter),"LeedsCounter")
                    print(newdata)
                except Exception as ex:
                    print(ex)
                    continue

        print("Storing") ###########
        insertrow(cursor,newdata,db,tablename)
        newdata['cars'] = 0
        print("TIME:" + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #cv2.imwrite('imagesampleLB{time}.png'.format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")), result)
        #revivecam(session)
