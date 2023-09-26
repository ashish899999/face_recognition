import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognition-58f18-default-rtdb.firebaseio.com/",
    'storageBucket':"facerecognition-58f18.appspot.com"

})
# student information 
folderpath = 'Images'
PathList = os.listdir(folderpath)
print(PathList)
imgList = []
studentIds=[]
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderpath, path)))
    studentIds.append(os.path.splitext(path)[0])
    
    fileName=f'{folderpath}/{path}'
    bucket=storage.bucket()
    blob= bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(os.path.splitext(path))
print(studentIds)

def findEncodings(imgageslist):
    encodeList=[]
    for img in imgList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

print("encoding started.....")
encodeListKnown=findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown,studentIds]
print(encodeListKnown)
print("encoding completed")


file=open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("file saved")