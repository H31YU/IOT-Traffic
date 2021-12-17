

import pymysql
import json
from datetime import datetime as dt
from pymysql.cursors import Cursor

f = open('RDSlogin.json')
rdslogin = json.load(f)
f.close()

db = pymysql.connect(host =rdslogin['host'], user = rdslogin['user'], password=rdslogin['password'])#, db= 'iotTraffic')

cursor = db.cursor()

cursor.execute("select version()")

data = cursor.fetchone()

###drop database
##sql = '''drop database <name>''' sql = '''drop table HamptonTraffic'''
##cursor.execute(sql)

###create datatbase
#sql = '''create database Hampton'''
#cursor.execute(sql)
#cursor.connection.commit()

###use database
sql = '''use Hampton'''
cursor.execute(sql)

##Create table
sql = '''
create table person(
id int PRIMARY KEY NOT NULL auto_increment,
fname text NOT NULL,
lname text NOT NULL,
)
'''
cursor.execute(sql)


##display table
sql = '''show tables'''
cursor.execute(sql)
cursor.fetchall()


###insert information
sql = '''
insert into person(fname, lname) values('%s', '%s')'''%('harvey', 'wong')
cursor.execute(sql)
db.commit()


##get data from table
sql = '''select * from HamptonTraffic'''
cursor.execute(sql)
cursor.fetchall()