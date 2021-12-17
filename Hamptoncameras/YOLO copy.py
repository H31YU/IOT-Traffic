import cv2
import csv
import collections
import numpy as np
from tracker import *
import imutils

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
    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)  # end here
    # print(up_list, down_list)

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

            color = [int(c) for c in colors[classIds[i]]]
            name = classNames[classIds[i]]
            detected_classNames.append(name)
            # Draw classname and confidence score 
            cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        count_vehicle(box_id, img)
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
        img = cv2.resize(img,(0,0),None,0.5,0.5)   
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
        #print(abs(temp-(sum(epochnum[-5:-1])/4)),"#####",temp,"####",(sum(epochnum[-5:-1])/4))
        if abs(temp-(sum(epochnum[-5:-1])/4))>=1 and len(epochnum)>=5:
            count += 1
            #print('##################')


        # Show the frames
        cv2.imshow('Output', img)

        if cv2.waitKey(1) == ord('q'):
            break

    # Write the vehicle counting information in a file and save it
    # print("Data saved at 'data.csv'")
    # Finally realese the capture object and destroy all active windows
    print(count)
    cap.release()
    cv2.destroyAllWindows()

def detectByPathVideo(path, writer,):
    print(writer)
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    frame = frame
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return
    print('Detecting people...')
    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()
        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            print(frame.shape)
            #frame = detect(frame)
            
            if writer is not None:
                #print(frame.shape)
                writer.write(frame)
            
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()



def from_static_image(image):
    #img = cv2.imread(image)
    #img = img
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]


    #print(net.getUnconnectedOutLayers())
    #outputNames = [] 
    #for i in net.getUnconnectedOutLayers():
        #print(i)
        #outputNames.append((layersNames[i[0] - 1]))

    
    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    postProcess(outputs,image)

    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    return image, (sum([frequency[i] for i in frequency.keys()]))
    # Draw counting texts in the frame
    #cv2.putText(img, "Car:        "+str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    #cv2.putText(img, "Motorbike:  "+str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    #cv2.putText(img, "Bus:        "+str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    #cv2.putText(img, "Truck:      "+str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)


    #cv2.imshow("image", img)

    #cv2.waitKey(0)

    # save the data to a csv file
    #with open("static-data.csv", 'a') as f1:
        #cwriter = csv.writer(f1)
        #cwriter.writerow([image, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
        


        #img = cv2.imread(image)
        #from_static_image("imagesample.png")
#realTime("rec_2021_12_05_15_02_18.mp4")