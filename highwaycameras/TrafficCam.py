import requests
import cv2
import numpy as np
import json
from imganalyser import upscaler
sr = upscaler()

##LOGIN DETAILS
def initcam():

    f = open('config.json')
    logindat = json.load(f)
    f.close()


    login_url = "https://www.highwaystrafficcameras.co.uk/HETCOperational/HETCLogin"


    ##init

    session = requests.session()
    session.post(login_url)
    sessID = session.cookies.get_dict()['JSESSIONID']
    cookies = {'_gid': 'GA1.3.2116531759.1639178487','_ga':'GA1.3.698040768.1638784088','_gat':'1','JSESSIONID':sessID}

    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}

    session.post(login_url, data=logindat,cookies=cookies,headers=headers)
    session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/DisclaimerAccepted?disclaimerAccepted=true")

    return session

def retrievecam(session):
    m1j42 = "https://www.highwaystrafficcameras.co.uk/HETCOperational/Image.action?username=harveywong&id=00021,24997&sid=0.8154699562194646&firsttimerequested=false"
    m621_9_2A = "https://www.highwaystrafficcameras.co.uk/HETCOperational/Image.action?username=harveywong&id=00021,20092&sid=0.7057666657709265&firsttimerequested=false"
    altm1j42 = "https://public.highwaystrafficcameras.co.uk/cctvpublicaccess/images/24997.jpg?sid=0.014999202498130804"
    r = session.get(altm1j42)
    print(r.url)
    nparr = np.fromstring(r.content, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_np = cv2.fastNlMeansDenoisingColored(img_np,None,10,10,7,21)
    return img_np

def Manualcam(session):
    m1j42 = "https://www.highwaystrafficcameras.co.uk/HETCOperational/Image.action?username=harveywong&id=00021,24997&sid=0.8154699562194646&firsttimerequested=false"
    m621_9_2A = "https://www.highwaystrafficcameras.co.uk/HETCOperational/Image.action?username=harveywong&id=00021,20092&sid=0.7057666657709265&firsttimerequested=false"
    altm1j42 = "https://public.highwaystrafficcameras.co.uk/cctvpublicaccess/images/24997.jpg?sid=0.014999202498130804" ##public access, lower refresh
    r = session.get(altm1j42)
    print(r.url)
    nparr = np.fromstring(r.content, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow('tempimg',img_np)
    img_np = sr.upsample(img_np)
    #img_np = cv2.fastNlMeansDenoisingColored(img_np,None,10,10,7,21)
    cv2.imshow('tempimg',img_np)
    img_np = cv2.fastNlMeansDenoisingColored(img_np,None,10,10,7,21)
    cv2.imshow('tempimg',img_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def revivecam(session):
    session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/Heartbeat.action?sid=0.5613762952783469")

def logout(session):
    session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/DisclaimerAccepted?disclaimerAccepted=false") ##logout proxy

#session = requests.session()
#Manualcam(session)

'''
###OUTPUT CAMERA FEED TEST
r = session.post(login_url, data=logindat,cookies=cookies,headers=headers)
r = session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/DisclaimerAccepted?disclaimerAccepted=true")
while True:
    time.sleep(6)
    r2 = session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/Image.action?username=harveywong&id=00021,24997&sid=0.8154699562194646&firsttimerequested=false")
    file = open("sample_image.png", "wb")
    file.write(r2.content)
    file.close()
    print(r2.url)
'''


#r = session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/DisclaimerAccepted?disclaimerAccepted=false") ##logout proxy
#r = session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/Heartbeat.action?sid=0.5613762952783469") ## keepalive
#r2 = session.get("https://www.highwaystrafficcameras.co.uk/HETCOperational/popup.jsp?id=00021,24997&rccid=4&refresh=6&description=M1 299/7A J41-42&orientation=The carriageway closest to the camera is Northbound")