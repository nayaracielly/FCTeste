import cv2,os
import sqlite3
import numpy as np
from PIL import Image 
import pickle


def extract_picture(cursor, trainer_file):
      sql1 = "SELECT FILE, TYPE, FILE_NAME FROM TRAINER WHERE id = :id"
      param = {'id': trainer_file}
      cursor.execute(sql1,param)
      ablob, ext, afile = cursor.fetchone()
      filename = 'trainer/' + afile + ext
      with open(filename, 'wb') as output_file:
          output_file.write(ablob)
      return filename

recognizer = cv2.createLBPHFaceRecognizer()
conn = sqlite3.connect('FaceBase.db')
cur = conn.cursor()
filename = extract_picture(cur, 1)
cur.close()
#conn.close()

recognizer.load('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

cursor = conn.cursor()
cursor.execute('SELECT ID FROM Peoples')
result_set = list(cursor.fetchall())
result = [elem[0] for elem in result_set]
#print result[0]

cursor.execute('SELECT Name FROM Peoples')
result_set2 = list(cursor.fetchall())
result2 = [elem[0] for elem in result_set2]
#print result2

cam = cv2.VideoCapture(0)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)


    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
     #   print nbr_predicted, conf
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
             
        for idx, i in enumerate(result):
             # print result[idx]
              #if(nbr_predicted==result[idx]):
              #     nbr_predicted=result2[idx]
               #    print result2[idx]
               if(nbr_predicted==1):
                nbr_predicted='Altair'
               elif(nbr_predicted==2):
                nbr_predicted='Rafael'
               elif(nbr_predicted==3):
                nbr_predicted='Alisson'
        
        cv2.cv.PutText(cv2.cv.fromarray(im),str(nbr_predicted)+"--"+str(conf), (x,y+h),font, 255) #Draw the text
        cv2.imshow('im',im)
        cv2.waitKey(10)








