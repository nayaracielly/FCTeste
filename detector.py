import cv2,os
import numpy as np
from PIL import Image 
import pickle

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cam = cv2.VideoCapture(0)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        if(nbr_predicted==2):
             nbr_predicted='Altair'
        elif(nbr_predicted==1):
             nbr_predicted='Nayara'
        elif(nbr_predicted==3):
             nbr_predicted='Alisson'
             
      
        if (str(conf) >= '40'):
            cv2.cv.PutText(cv2.cv.fromarray(im),str(nbr_predicted)+"--"+str(conf), (x,y+h),font, 255) #Draw the text
            cv2.imshow('im',im)
            cv2.waitKey(10)
        else:
            cv2.cv.PutText(cv2.cv.fromarray(im)," Desconhecido ", (x,y+h),font, 255) #Draw the text
            cv2.imshow('im',im)
            cv2.waitKey(10)    








