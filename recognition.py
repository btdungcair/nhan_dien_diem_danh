import os
import cv2
import numpy as np
import face_recognition

parent_path = os.getcwd().replace('\\', '/')
path = parent_path + '/ImagesStudent'
destination = parent_path + '/result/'

image_student_file_list = os.listdir(path)

images = []
class_names = []

for file in image_student_file_list:
    img = cv2.imread(f'{path}/{file}')
    images.append(img)
    class_names.append(file.split('.')[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(attendance_id_list, id):
    attendance_id_list.append(id)

def faceRecognition(attendance_file_list):
    attendance_id_list = []
    result_image_list = []
    encodeListKnown = findEncodings(images)
    for file in attendance_file_list:
        img = cv2.imread(f'{file}')
        imgS = cv2.resize(img,(0,0),None,1,1)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)    
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)   
        
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                id = class_names[matchIndex]
                # student_name = controller.get_student(id)[1]
                y1,x2,y2,x1 = faceLoc
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,id,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(attendance_id_list, id)
        result_path = os.path.join(destination, os.path.splitext(file.split('/')[-1])[0]+"-res.jpg")
        cv2.imwrite(result_path, img)
        result_image_list.append(result_path)
    return attendance_id_list, result_image_list