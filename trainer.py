import cv2,os
import sqlite3
import numpy as np
from PIL import Image 

recognizer = cv2.createLBPHFaceRecognizer()
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

def get_images_and_labels(path):
     image_paths = [os.path.join(path, f) for f in os.listdir(path)]
     # images will contains face images
     images = []
     # labels will contains the label that is assigned to the image
     labels = []
     for image_path in image_paths:
         # Read the image and convert to grayscale
         image_pil = Image.open(image_path).convert('L')
         # Convert the image format into numpy array
         image = np.array(image_pil, 'uint8')
         # Get the label of the image
         nbr = int(os.path.split(image_path)[1].split(".")[0].replace("face-", ""))
         #nbr=int(''.join(str(ord(c)) for c in nbr))
         print nbr
         # Detect the face in the image
         faces = faceCascade.detectMultiScale(image)
         # If face is detected, append the face to images and the label to labels
         for (x, y, w, h) in faces:
             images.append(image[y: y + h, x: x + w])
             labels.append(nbr)
             cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
             cv2.waitKey(10)
     # return the images list and labels list
     return images, labels

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print 'Creating treiner schema'
        sql_treiner = '''create table if not exists TREINER(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        File BLOB,
        Type TEXT,
        File_name TEXT;'''
        conn.execute(sql_treiner) # create treiner table
    else:
        print 'Treiner schema exists\n'
    return conn

def insert_file(treiner_file, db_file):
     conn = sqlite3.connect(db_file)
     with open(treiner_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(treiner_file)
        afile, ext = os.path.splitext(base)
        sql = '''INSERT INTO TREINER
        (FILE, TYPE, FILE_NAME)
        VALUES(?, ?, ?);'''
        conn.execute(sql,[sqlite3.Binary(ablob), ext, afile]) 
        conn.commit()

images, labels = get_images_and_labels(path)
cv2.imshow('test',images[0])
cv2.waitKey(1)

recognizer.train(images, np.array(labels))
recognizer.save('trainer/trainer.yml')

create_or_open_db('FaceBase.db')
insert_file('trainer/trainer.yml','FaceBase.db')


cv2.destroyAllWindows()
