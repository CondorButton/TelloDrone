import cv2
import numpy as np
from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 25, 0)
time.sleep(0.5)

# ##### PARAMETERS #####
# fspeed = 117/10 #Forward Speed, cm/s  #tune-able
# aspeed = 360/10 #Angular Speed Deg/s  #tune-able
# interval = 0.25
# dInterval = fspeed*interval
# aInterval = aspeed*interval
# #############################
# xMap, yMap = 500, 500
# a = 0
# yaw = 0
#
w,h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0] #tune-able
pError = 0

# points = [(0,0), (0,0)]

# #Movement Mapping Code
# def drawPoints(img, points):
#     for point in points:
#         cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
#
#     cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, f'({(points[-1][0]-500)/100}, {(points[-1][1]-500)/100})m',
#                 (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

#Facial Detection Code
def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    FaceListC = []
    FaceListArea = []

    # global xMap, yMap

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w//2
        cy = y + h//2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        FaceListC.append([cx, cy])
        FaceListArea.append(area)
    if len(FaceListArea) != 0:
        i = FaceListArea.index(max(FaceListArea))
        return img, [FaceListC[i], FaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(me, info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0
    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)

    me.send_rc_control(0, fb, 0, speed)
    return error, [fb, speed, x, y]

#cap = cv2.VideoCapture(1)

while True:
    #_, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w,h))
    img, info = findFace(img)
    pError, vals = trackFace(me, info, w, pid, pError)
    # mapImg = np.zeros((1000, 1000, 3), np.uint8)
    # if(vals[0] == 20):
    #     d = dInterval
    #     a = 270
    # elif(vals[0] == -20):
    #     d = -dInterval
    #     a = -90
    # if(vals[1] != 0):
    #     yaw += aInterval
    #
    # if(points[-1][0] != vals[2] or points[-1][1] != vals[3]):
    #     points.append((vals[2], vals[3]))
    # drawPoints(mapImg, points)
    #print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    # cv2.imshow("Map", mapImg)
    # time.sleep(interval)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break