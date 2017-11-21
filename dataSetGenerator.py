import cv2,os
import sqlite3
cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('Classifiers/face.xml')
i = 0
offset = 50


def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print 'Creating schema'
        sql = '''create table if not exists PEOPLES(
        ID INTEGER PRIMARY KEY,
        Name TEXT);'''
        sql_image = '''create table if not exists PICTURES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Picture BLOB,
        Type TEXT,
        File_name TEXT);'''
        sql_trainer = '''create table if not exists TRAINER(
        ID INTEGER PRIMARY KEY,
        File BLOB,
        Type TEXT,
        File_name TEXT);'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
        conn.execute(sql_image) # create image table
        conn.execute(sql_trainer) # create trainer table
    else:
        print 'Schema exists\n'
    return conn

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM PEOPLES WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE PEOPLES SET NAME='"+str(Name)+"' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO PEOPLES(ID,NAME)Values("+str(Id)+",'"+str(Name)+"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()

def insert_picture(picture_file):
    conn = create_or_open_db('FaceBase.db')
    with open(picture_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(picture_file)
        afile, ext = os.path.splitext(base)
        sql = '''INSERT INTO PICTURES
        (PICTURE, TYPE, FILE_NAME)
        VALUES(?, ?, ?);'''
        conn.execute(sql,[sqlite3.Binary(ablob), ext, afile]) 
        conn.commit()
	
# picture_file = "./dataSet/face- 2.1.jpg"
# insert_picture(conn, picture_file)
# conn.close()

id=raw_input('Digite o id ')
name=raw_input('Digite o Nome ')
create_or_open_db('FaceBase.db')
insertOrUpdate(id,name)

while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        i=i+1
        cv2.imwrite("dataSet/face-"+id +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
        #picture_file = "./dataSet/face-"+id +'.'+ str(i) + ".jpg"
        #insert_picture(picture_file)
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.waitKey(100)
    if i>70:
        cam.release()
        cv2.destroyAllWindows()
        break

