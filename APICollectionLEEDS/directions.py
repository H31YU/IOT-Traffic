import requests
import json
import ast

f = open('googleKey.json')
googleKey = json.load(f)['key']
f.close()

def getMapsDir(key):

    parameters = {
        "destination":"place_id:ChIJzwAKy8WxEmsRh-SqQrC5mnk",
        
        "origin":"place_id:EhRIYS1IYSBSZCwgTG9uZG9uLCBVSyIuKiwKFAoSCT1jodz6qNhHEaI_0kP5923xEhQKEgnz8xe3Wxt2SBEKsgA5eS6RSQ",

        "mode":"driving",

        "departure_time":"now",

        "key": key

    } 

    url = "https://maps.googleapis.com/maps/api/directions/json"


    response = requests.get(url, params=parameters)


    #print(response.text)
    dirData= ast.literal_eval(response.text)
    return dirData['routes'][0]['legs'][0]['duration']['value'], dirData['routes'][0]['legs'][0]['duration_in_traffic']['value'], response.text


#print(getMapsDir(googleKey))