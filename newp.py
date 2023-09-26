import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
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
bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgBackground = cv2.imread('Resources\pppp.jpg')
# Resources/background.png
# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))   


# Load the encoding file 
print("loading encoidng  file...")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds= pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownWithIds
print("encode file loaded")
modeType = 0
counter=0
id=-1
imgStudent=[] 

while True:
    success, img = cap.read()


    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    # imgs=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    faceCurFrame= face_recognition.face_locations(imgs)
    encodeCurFrame= face_recognition.face_encodings(imgs,faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc  in zip(encodeCurFrame,faceCurFrame):
         matches= face_recognition.compare_faces(encodeListKnown,encodeFace)
         faceDis= face_recognition.face_distance(encodeListKnown,encodeFace)
        #  print("matches",matches)
        #  print("faceDis",faceDis)
         
         matchIndex= np.argmin(faceDis)
         print("match Index",matchIndex)  
         if matches[matchIndex]:
            # print("known face detected")
            # print(studentIds[matchIndex])
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1 * 4,x2 * 4,y2 * 4,x1 * 4
            bbox= 55 + x1,162 + y1,x2-x1,y2-y1
            imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
            id=studentIds[matchIndex]
            print(id)
            if counter== 0:
                counter=1
                modeType=1
    if counter!=0:
        
        if counter==1:
           # get the data
           studentInfo= db.reference(f'Students/{id}').get()

           print(studentInfo)
           # get the image from the storage 
           blob=bucket.get_blob(f'Images/{id}.png')
           array=np.frombuffer(blob.download_as_string(),np.uint8)
           imgStudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

           # update the path
           ref=db.reference(f'Students/{id}')
           studentInfo['total_attendance']+=1
           ref.child('total_attendance').set(studentInfo['total_attendance'])
        if 10<counter<20:
            modeType=2


        if counter<=10:
                cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                          cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                cv2.putText(imgBackground, str(studentInfo['Doctor_specialisation']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentInfo['Availability']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                imgBackground[175:175+216,909:909+216]=imgStudent

        counter+=1
        


    cv2.imshow("webcam", img)   
    cv2.imshow("Face Attendance", imgBackground)
    if(cv2.waitKey(1) & 0xFF==ord('q')):
        cv2.destroyAllWindows()

