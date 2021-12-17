from analyser import analyser
import timeit
import time
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df
from YOLO import realTime
import glob


outputfilename = "Hamptoncars"
#analyser(video, output)

def Store(newdata,outputfile):
    data = pd.read_csv('{filename}.csv'.format(filename=outputfile),index_col=0)
    
    update = df(newdata, index=[0])

    data = pd.concat([update,data],axis=0,ignore_index=True)
    data.to_csv('{filename}.csv'.format(filename=outputfile))


if __name__=="__main__":
    

    files =[]
    for i in ['05','06','07','08','09']:
        files = files + (glob.glob('S:/CCTV/ContraCam/LuowiceR8_554\\2021\\12\\{}\\*.gif'.format(i),recursive=True))
    last10 = files[0].split('\\')[-1][18]
    newdata = {"datetime":files[0].split('\\')[-1][4:23],
                        "cars":0,
                        }
    tempdata = []
    for f in files:
        date = f.split('\\')[-1][4:23]
        if date[14] == last10:
            newdata["datetime"] = "{y}-{m}-{d} {H}:{M}0:00".format(y=date[0:4], m = date[5:7], d = date[8:10],H = date[11:13],M = date[14])
            num = realTime(f)
            newdata['cars'] += num
            last10 = date[14]
            print(f)
            print(newdata)
        elif date[18] != last10:
            tempdata.append(newdata)
            Store(newdata,"Hamptoncars - Copy")
            newdata['cars'] = 0
            newdata["datetime"] = "{y}-{m}-{d} {H}:{M}0:00".format(y=date[0:4], m = date[5:7], d = date[8:10],H = date[11:13],M = date[14])
            num = realTime(f)
            newdata['cars'] += num
            last10 = date[14]
            print(f)
            print(newdata)

    data = pd.read_csv('{filename}.csv'.format(filename=outputfilename),index_col=0)
    
    update = df(tempdata)

    data = pd.concat([update,data],axis=0,ignore_index=True)
    data.to_csv('{filename}.csv'.format(filename=outputfile))
