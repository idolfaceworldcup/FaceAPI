# -*- coding: utf-8 -*-

import cv2
import os

newCode="sudo modprobe bcm2835-v4l2"
os.system(newCode)

cam = cv2.VideoCapture(0)

if (cam.isOpened() == False): 
  print("Unable to read camera feed")

cam.set(3, 180 ) # set video width
cam.set(4, 240) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")

input_face_ID=face_id
count = 0

while(True):

    ret, img = cam.read()
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        cv2.imwrite("./dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()


