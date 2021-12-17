import requests
import json
import ast
from datetime import datetime


'''f = open('accuKey.json')
accuKey = json.load(f)['key']
f.close()
print(accuKey)'''

f = open('MetKey.json')
MetKey = json.load(f)['key']
f.close()

def Prevdayweather(key):
    parameters = {
        "BULK_FILE_NAME":"weather_16_mmddyy_hhmm.json.gz",

        "appid":key,
    }

    url = "http://bulk.openweathermap.org/archive/{BULK_FILE_NAME}"
    response = requests.get(url, params=parameters)
    filename = 'weather16'
    outfile = open(filename,'wb')
    #pickle.dump(response,outfile)
    outfile.close()
    print(type(response))

def getWeather(key):

    parameters = {
        "q":"feltham",

        "units":"metric",

        "appid":key,
    }

    url = "http://api.openweathermap.org/data/2.5/weather"


    response = requests.get(url, params=parameters)


    #print(response.text)
    #dirData= ast.literal_eval(response.text)
    weatherData = ast.literal_eval(response.text)
    return weatherData['weather'][0]['main'], weatherData['main']['temp'] 


def getMetWeather(key):

    weathercodes= {"NA":"Not available",
                "0":"Clear night",
                "1":"Sunny day",
                "2":"Partly cloudy (night)",
                "3":"Partly cloudy (day)",
                "4":"Not used",
                "5":"Mist",
                "6":"Fog",
                "7":"Cloudy",
                "8":"Overcast",
                "9":"Light rain shower (night)",
                "10":"Light rain shower (day)",
                "11":"Drizzle",
                "12":"Light rain",
                "13":"Heavy rain shower (night)",
                "14":"Heavy rain shower (day)",
                "15":"Heavy rain",
                "16":"Sleet shower (night)",
                "17":"Sleet shower (day)",
                "18":"Sleet",
                "19":"Hail shower (night)",
                "20":"Hail shower (day)",
                "21":"Hail",
                "22":"Light snow shower (night)",
                "23":"Light snow shower (day)",
                "24":"Light snow",
                "25":"Heavy snow shower (night)",
                "26":"Heavy snow shower (day)",
                "27":"Heavy snow",
                "28":"Thunder shower (night)",
                "29":"Thunder shower (day)",
                "30":"Thunder}"
    }


    parameters = {
        "res":"hourly",

        "time":datetime.now().strftime("%Y-%m-%dT%HZ"),

        "key":key,
    }

    url = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3344"


    response = requests.get(url, params=parameters)


    #print(response.text)
    #dirData= ast.literal_eval(response.text)
    weatherData = ast.literal_eval(response.text)
    return weathercodes[weatherData['SiteRep']['DV']['Location']['Period']['Rep']['W']], weatherData['SiteRep']['DV']['Location']['Period']['Rep']['T']

#print(getWeather(''))
#Prevdayweather('')
#print(getMetWeather(MetKey))

