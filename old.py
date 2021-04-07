# Importing Libraries
import serial
import time
import cv2
import numpy as np
import sys


arduino = serial.Serial(port=sys.argv[1], baudrate=1000000, timeout=.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(1)
img = None

def write_read(x):
    print(bytes(x, 'utf-8'))
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.01)
    data = 'test'
    print(data)
    return data

def find_face():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)
    if len(faces) == 0:
        cv2.imshow('img', img)
        print('no face')
        return -1, -1
    else:
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]

        face_loc = (x+(w/2),y+(y/2))
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        '''
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        ex, ey, ew, eh = eyes[0]

        eye_loc = (int(ex+(ew/2)), int(ey+(eh/2)))
        cv2.circle(roi_color, eye_loc, 10, (0,0,255), 2)
        '''
        cv2.imshow('img', img)
        return face_loc

camera_angle = 65.563
scaling_const_x = 0.28125
scaling_const_y = 0.375
last_x = 0
last_y = 0
while True:
    _, img = cap.read()
    
    x, y = find_face()
    if x == -1 or y == -1:
        x = last_x
        y = last_y
    x_ratio = x/640
    y_ratio = y/480
    servo_x = round((180-camera_angle)/2 + (camera_angle*(1-x_ratio)), 1)
    servo_y = round((180-camera_angle)/2 + (camera_angle*y_ratio), 1)

    if x == last_x or abs(last_x - x) < 1 :
        
        continue
        
        
    print(f'new:({servo_x}, {servo_y})')
    value = write_read(str(servo_x))
    last_x = x

    time.sleep(0.01)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()
