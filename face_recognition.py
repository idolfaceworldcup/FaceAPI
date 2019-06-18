import cv2
import numpy as np
import os
from collections import OrderedDict
import datetime
import RPi.GPIO as GPIO
import time
import sys

newCode="sudo modprobe bcm2835-v4l2"
os.system(newCode)

GPIO.setmode(GPIO.BCM)

sensor = 23
Sled = 20
Fled = 21

GPIO.setup(sensor, GPIO.IN)
GPIO.setup(Sled, GPIO.OUT)
GPIO.setup(Fled, GPIO.OUT)

file_data = OrderedDict()
face_name="unkown"

def successCap(id):
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                cv2.imwrite("successCap/"+ id + ".png", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
                return  True


def failCap():
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.imwrite("successCap/unkwon.png", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
        return  True

time.sleep(2)
print ("센서 작동중")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'JIHOON', ] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

time.sleep(4)

while True:
    state = False
    count = 0;
    if GPIO.input(sensor):
        print ("움직임이 감지되었습니다")
        print ("얼굴을 인식합니다")
        while True:

            ret, img =cam.read()
            img = cv2.flip(img, 1) # Flip vertically

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))

                    if(int(confidence) > 50):

                        face_recog_state=successCap(id)

                        face_name=id
                        GPIO.output(Sled, True)
                        print("얼굴인식이 되었습니다. 문이 열립니다")
                        time.sleep(2)

                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    confidence = "  {0}".format(round(100 - confidence))                 
                    print("얼굴인식에 실패했습니다")
                    count=count+1
                    print(count)
                    if count==5:
                        GPIO.output(Fled, True)
                        fail_state=True
                        face_recog_state=True
                    break

                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img) 


            if face_recog_state == True:
                time.sleep(4)
                GPIO.output(Sled, False)
                GPIO.output(Fled, False)
                state=True
                
                break

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                state=True
                break

    if state == True:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
