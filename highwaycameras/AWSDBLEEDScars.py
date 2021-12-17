import pymysql
import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
from pymysql.cursors import Cursor


f = open('RDSlogin.json')
rdslogin = json.load(f)
f.close()




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
    datetime VARCHAR(16) NOT NULL,
    cars INT NOT NULL
    )""".format(tablename)

    cursor.execute(create_table)
    cursor.connection.commit()

def insertrow(cursor,data,db,tablename):
    query ="""INSERT INTO {}(datetime, cars) 
    VALUES(%s,%s)
    """.format(tablename)
    row_to_insert = (data["datetime"],data["cars"])
    cursor.execute(query,row_to_insert)
    db.commit()

def df2db(cursor,df,db,tablename):
    for i,row in df.iterrows():
        insertrow(cursor,row,db,tablename)

def getall(cursor,tablename):
    #HamptonTraffic
    sql = "select * from {}".format(tablename)
    cursor.execute(sql) 
    df = pd.DataFrame(cursor.fetchall(), columns = ["id","datetime", "cars"])
    return df


def deleteData(cursor,tablename):
    sql = "DELETE FROM {}".format(tablename)
    cursor.execute(sql)
    cursor.connection.commit()

def update(cursor,data,tablename):
    sql = "UPDATE {table} SET cars = {newdata} WHERE id = 1".format(table = tablename,newdata=data)
    cursor.execute(sql)
    cursor.connection.commit()
##cursor.execute("ALTER TABLE HamptonTraffic CHANGE id id INT PRIMARY KEY NOT NULL auto_increment")
##cursor.execute("DROP TABLE HamptonTraffic")



#db, cursor = connect(rdslogin)
#finddb(cursor, "LEEDS")
#tablename = "Leedscars"
#df = getall(cursor,tablename)


"""
createtable(cursor,tablename)
df2db(cursor,data,db,tablename)
cursor.connection.commit()
"""

