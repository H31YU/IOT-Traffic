import streamlit as st
import pandas as pd
import pymysql
import numpy as np
import json
from AWSDB import *
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime

def makegraph(data,col1,col2,xlabel,ylabel): 
  chart = alt.Chart(data).mark_line().encode(
            x=alt.X('{}'.format(col1), axis=alt.Axis(labelOverlap="greedy",grid=False)),
            y=alt.Y('{}'.format(col2), scale=alt.Scale(domain=[data['{}'.format(col2)].min(), data['{}'.format(col2)].max()]))
  )

  c = alt.Chart(data).mark_line().encode(
    x = alt.X('{}:T'.format(col1), axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("{}:Q".format(col2), scale=alt.Scale(domain=[data['{}'.format(col2)].min(), data['{}'.format(col2)].max()]))
    )
  c.encoding.x.title = '{}'.format(xlabel)
  c.encoding.y.title = '{}'.format(ylabel)
  chart = alt.layer(
      c.mark_line()
  ).interactive()

  st.altair_chart(chart, use_container_width=True)

def weathergraphs(region, traffic,temp,con):
  if temp:
    st.write("""
    #### Past Weather conditions in {}
    Based on Met offic weather code: https://www.metoffice.gov.uk/services/data/datapoint/code-definitions 
    """.format(region))
    makegraph(traffic[['datetime','Weather']],'datetime','Weather',"Date",'Weather condition code')

    ####################################################################################
  if con:
    st.write("""
    #### Past Temperature in {}
    """.format(region))
    makegraph(traffic[['datetime','Temp']],'datetime','Temp',"Date",'Temperature (Degrees)')

  ####################################################################################


f = open('RDSlogin.json')
rdslogin = json.load(f)
f.close()

db, cursor = connect(rdslogin)
finddb(cursor, "Hampton")
tablename = "HamptonTraffic"
HamptonTraffic = getall(cursor,tablename)
#df = df.rename(columns={'id':'index'}).set_index('index')
HamptonTraffic['Temp'] = pd.to_numeric(HamptonTraffic['Temp'], downcast='float')

tablename = "Hamptoncars"
sql = "select * from {}".format(tablename)
cursor.execute(sql) 
hamptoncars = pd.DataFrame(cursor.fetchall(), columns = ["id","datetime", "cars"])


finddb(cursor, "LEEDS")
tablename = "Leedscars"
sql = "select * from {}".format(tablename)
cursor.execute(sql) 
leedscars = pd.DataFrame(cursor.fetchall(), columns = ["id","datetime", "cars"])
#print(leedscarsdf[-1000:-13])

tablename = "LeedsTraffic"
LeedsTraffic = getall(cursor,tablename)
LeedsTraffic['Temp'] = pd.to_numeric(LeedsTraffic['Temp'], downcast='float')
#print(LeedsTrafficdf[-1000:-1])

tablename = "LeedsCounter"
sql = "select * from {}".format(tablename)
cursor.execute(sql)
leedscounter = pd.DataFrame(cursor.fetchall(), columns = ["id","datetime", "cars"])


selection = st.sidebar.selectbox(
    "Select Journey",
    ("LEEDS to Hampton", "Hampton (Local journey)")
)
weather = st.sidebar.selectbox(
    "Show Weather graphs",
    (None,"Weather condition", "Temperature", "Weather Condition and Temperature")
)



if selection == "LEEDS to Hampton":
  region = "LEEDS"
  traffic = LeedsTraffic
  cars =  leedscars
  junction = "M1 Junction 42"
else:
  region = "Hampton"
  traffic = HamptonTraffic
  cars =  hamptoncars
  junction = "Hampton Lane"


st.write("""
# Traffic and weather data

## Graphs show the local traffic and weather in {}
Double click on graphs to return to original view
""".format(region))

if region == "LEEDS":
  st.write("""
  # Number of cars on {} in the last ten minutes: {}
  """.format(junction,leedscounter["cars"].iloc[-1]))

st.write("""
#### Past Traffic in {}
""".format(region))

#print(datetime.strptime(traffic['datetime'].iloc[0], '%Y-%m-%d %H:%M'))
range = st.slider("Date range", value=[datetime.strptime(traffic['datetime'].iloc[0], '%Y-%m-%d %H:%M'),datetime.strptime(traffic['datetime'].iloc[-1], '%Y-%m-%d %H:%M')])
st.write(""" from {}    to     {}
""".format(range[0],range[1]))
traffic['datetime']=pd.to_datetime(traffic['datetime'])
mask = (traffic['datetime'] > range[0]) & (traffic['datetime'] <= range[1])

makegraph(traffic.loc[mask][['datetime','Duration_in_Traffic']],'datetime','Duration_in_Traffic',"Date",'Duration in Traffic (s)')
####################################################################################

cars['datetime']=pd.to_datetime(cars['datetime'])
mask = (cars['datetime'] > range[0]) & (cars['datetime'] <= range[1])
####################################################################################
st.write("""
#### Past Car count on {}
""".format(junction))
makegraph(cars.loc[mask][['datetime','cars']],'datetime','cars',"Date",'Number of cars')
####################################################################################

st.write("""
#### Scatter graph of car count against Traffic duration
""")
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.scatter(cars["cars"][-412:-13],traffic["Duration_in_Traffic"][-400:-1])
plt.xlabel("Car count")
plt.ylabel("Traffic duration (s) from google maps")
st.write(fig)


if weather == "Weather condition": 
  weathergraphs(region, traffic,0,1)
elif weather == "Temperature":
  weathergraphs(region, traffic,1,0)
elif weather == "Weather Condition and Temperature":
  weathergraphs(region, traffic,1,1)