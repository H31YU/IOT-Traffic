from cv2 import dnn_superres
import cv2
import numpy as np
import argparse
import math
from YOLO import from_static_image
from tracker import *


################################################################
################################################################
tracker = EuclideanDistTracker()

# Initialize the videocapture object
input_size = 320

# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2

font_color = (0, 0, 255)
font_size = 0.5
font_thickness = 2


# Store Coco Names in a list
classesFile = "coco.names"
classNames = open(classesFile).read().strip().split('\n')

# class index for our required detection classes
required_class_index = [0, 1, 2, 3, 5, 7]
detected_classNames = []
#print([classNames[i] for i in required_class_index])


## Model Files
modelConfiguration = 'yolov3-320.cfg'
modelWeigheights = 'yolov3-320.weights'

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)
# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')



#middle_line_position = 400   
#up_line_position = middle_line_position - 100
#down_line_position = middle_line_position + 100


# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0, 0, 0]
down_list = [0, 0, 0, 0, 0, 0]


################################################################
################################################################


thres = 0.4 # Threshold to detect object

classNames = []
classFile = "coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    return img,objectInfo

def detect(frame):
    items = [
        'cat',
        'dog',
        'horse',
        'sheep',
        'cow',
        'elephant',
        'bear',
        'zebra',
        'giraffe',
        'person',
        'car',
        'truck',
        'bus',
        'motorcycle'
    ]
    result, objectInfo = getObjects(frame,thres,0.2,objects=items)
    person = 1
    for i in objectInfo:
        person+=1
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    return frame , (person-1)

def upscaler():
    # Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()
    # Read the desired model
    #path = "EDSR_x3.pb"
    path = "FSRCNN_x2.pb"
    sr.readModel(path)
    # Set the desired model and scale to get correct pre- and post-processing
    #sr.setModel("edsr", 3)
    sr.setModel("fsrcnn",2)
    # Upscale the image
    return sr


def imganalyse(frame,sr):
    #cv2.imshow('output', frame)
    result = sr.upsample(frame)
    result1, num1 = from_static_image(result)

    #result = cv2.fastNlMeansDenoisingColored(result,None,10,10,7,21)

    #result = imutils.resize(result , width=min(800,frame.shape[1]))
    #print(frame.shape)
    #result = frame
    #cv2.imwrite('imagesample.png', result)

    #cv2.imshow('imagesample.png',result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #result, num = from_static_image(result)
    #print(num1, num,"#####")

    #cv2.imshow('imagesample.png',result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #cv2.imwrite('imagesampleLB.png', result)
    return result1,num1


    c#v2.imshow('imagesample.png',result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()






