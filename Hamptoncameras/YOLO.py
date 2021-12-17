import cv2
import csv
import collections
import numpy as np
from tracker import *
import imutils
import time

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
required_class_index = [2, 3, 5, 7]
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



middle_line_position = 300   
up_line_position = middle_line_position - 30
down_line_position = middle_line_position + 30


# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0, 0, 0]
down_list = [0, 0, 0, 0, 0, 0]

# Function for finding the center of a rectangle
def find_center(x, y, w, h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy=y+y1
    return cx, cy

def count_vehicle(box_id, img):

    x, y, w, h, id, index = box_id
    
    # Find the center of the rectangle for detection
    center = find_center(x, y, w, h)
    ix, iy = center

def postProcess(outputs,img):
    global detected_classNames 
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    # print(classIds)

    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            # print(x,y,w,h)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])
            cv2.rectangle(img, (x, y), (x + w, y + h), (160,200,120), 1)

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    return(len(boxes_ids))


def realTime(vid):
    cap = cv2.VideoCapture(vid)
    frameC = 0
    epochnum = []
    count = 0
    while True:
        success, img = cap.read()
        if type(img) == type(None):
            break
        #img = cv2.resize(img,(0,0),None,0.5,0.5)   
        ih, iw, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)  ####320×320
        # Set the input of the network
        net.setInput(blob)
        layersNames = net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
        # Feed data to the network
        outputs = net.forward(outputNames)
    
        # Find the objects from the network output
        
        temp = postProcess(outputs,img)
        epochnum.append(temp)


        #cv2.imshow('output',img)
        #if len(epochnum)>=2:
        #    print(abs(temp-(sum(epochnum[-5:-1])/4)),"#####",abs(epochnum[-2]-(sum(epochnum[-5:-2])/3)),"####",temp,"####",(sum(epochnum[-5:-1])/4))

        if abs(temp-(sum(epochnum[-5:-1])/4))>=0.6 and len(epochnum)>=5 and abs(epochnum[-2]-(sum(epochnum[-5:-2])/3))>=0.6:
            count += 1
            #print('##################')
        #if cv2.waitKey(1) == ord('q'):
        #   break
    return count

#realTime("Contacam\\1210\\rec_2021_12_10_00_01_29.gif")