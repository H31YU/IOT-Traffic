import pymysql
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
from pymysql.cursors import Cursor


f = open('RDSlogin.json')
rdslogin = json.load(f)
f.close()


##read csv

outputfile = "test"
data = pd.read_csv('{filename}.csv'.format(filename=outputfile),index_col=0)


##remove rows with NaN

data = data.drop(columns=['mapsdata'])
first = np.where(pd.isnull(data))[0][-1] + 1
data= data[first:]
columns = list(data.columns)

data["datetime"] = pd.to_datetime(data["datetime"], format='%Y %m %d %H %M', errors='coerce')
print(data[data.datetime.isnull()])
data["datetime"] = data["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")


data['Weather'] = data['Weather'].map({
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
})
print(data[data.Weather.isnull()])




def connect(rdslogin):
    db = pymysql.connect(host =rdslogin['host'], user = rdslogin['user'], password=rdslogin['password'])#, db= 'iotTraffic')
    cursor = db.cursor()
    return db, cursor

def finddb(cursor, dbname):
    sql = "use {}".format(dbname)
    cursor.execute(sql)


def createtable(cursor,tablename):
    create_table = """
    CREATE TABLE {}(
    id INT PRIMARY KEY NOT NULL auto_increment,
    Traffic INT NOT NULL,
    Weather TEXT NOT NULL,        
    datetime VARCHAR(16) NOT NULL, 
    Temp DECIMAL(12,1) NOT NULL,
    Duration_in_Traffic INT NOT NULL
    )""".format(tablename)

    cursor.execute(create_table)
    cursor.connection.commit()


def insertrow(cursor,data):
    query ="""INSERT INTO HamptonTraffic(Traffic, Weather, datetime, Temp, Duration_in_Traffic) 
    VALUES(%s,%s,%s,%s,%s)
    """
    row_to_insert = (data["Traffic"],data["Weather"],data["datetime"],data["Temp"],data["Duration in Traffic"])
    cursor.execute(query,row_to_insert)

def df2db(cursor,df):
    for i,row in df.iterrows():
        insertrow(cursor,row)

def getall(cursor,tablename):
    #HamptonTraffic
    sql = "select * from {}".format(tablename)
    cursor.execute(sql) 
    df = pd.DataFrame(cursor.fetchall(), columns = ["id","Traffic", "Weather", "datetime", "Temp", "Duration_in_Traffic"])
    return df


def deleteData(cursor,tablename):
    sql = "DELETE FROM {}".format(tablename)
    cursor.execute(sql)
    cursor.connection.commit()

##cursor.execute("ALTER TABLE HamptonTraffic CHANGE id id INT PRIMARY KEY NOT NULL auto_increment")
##cursor.execute("DROP TABLE HamptonTraffic")



#db, cursor = connect(rdslogin)
#finddb(cursor, "Hampton")
#tablename = "HamptonTraffic"
#df = getall(cursor,tablename)


"""
createtable(cursor,tablename)
df2db(cursor,data)
cursor.connection.commit()
"""

