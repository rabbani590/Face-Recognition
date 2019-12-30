# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 21:20:13 2019

@author: girik
"""

import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
import PIL
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import re
import smtplib

#subject import module
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#attachment import module
#from email.mime.base import MIMEBase
#from email import encoders


window = tk.Tk()
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
window.configure(background='White')



window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#img = ImageTk.PhotoImage(Image.open("C:\\Users\\Work\\Desktop\##\\Face-Recognition-Based-Attendance-System-master\\codegnan-logo.jpg"))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.


# Font is a tuple of (font_family, size_in_points, style_modifier_string)



message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,fg="Black"  ,width=50  ,height=3,font=('Times New Roman', 30, ' bold ')) 

message.place(x=200, y=20)




lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="Black"   ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20   ,fg="Black",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="Black"  ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20   ,fg="Black",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl4=tk.Label(window, text="Enter Email" ,width=20 ,fg="Black" ,height=2, font=('times' ,15, 'bold'))
lbl4.place(x=400 ,y=360)

txt4 = tk.Entry(window,width=50   ,fg="Black",font=('times', 15, ' bold ')  )
txt4.place(x=700, y=360)


lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="Black"   ,height=2 ,font=('times', 15,' bold ')) 
lbl3.place(x=400, y=420)

message = tk.Label(window, text=""   ,fg="Black"  ,width=30  ,height=2 ,font=('times', 15, ' bold ')) 
message.place(x=700, y=420)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="Black"    ,height=2 ,font=('times', 15, '  bold  '  )) 
lbl3.place(x=400, y=650)


message2 = tk.Label(window, text="" ,fg="Black"   ,activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=650)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    Email=(txt4.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 60
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name + "Email : " + Email
        row = [Id , name ,Email]#row format 
        #updating student details file
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    #recognizer.save("TrainingImageLabel\Trainner.yml")
    recognizer.write('recognizer/trainningData.yml')
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    #recognizer.read("TrainingImageLabel\Trainner.yml")
    #recognizer.load('recognizer/trainningData.yml')
    recognizer.read('recognizer/trainningData.yml')
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    print(df)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w]) 
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            #if(conf > 75):
            if 'Id' in df and (conf < 50):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    b = attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    print(attendance)
    res=attendance
    message2.configure(text= res)
    #absentes extraction starts
    l=[]
    m=[]
    result=[]
    with open('D:\Face-Recognition\StudentDetails\StudentDetails.csv','rt')as f1:
      data1 = csv.reader(f1)
      for row in data1:
          m.append(row[0])
          

    with open('D:\Face-Recognition\\'+fileName,'rt')as f2:
      data2 = csv.reader(f2)
      for row in data2:
          l.append(row[0])
    
    for i in m:
       if i not in l:
           if i!='':
               result.append(i)
    #absentes extraction ends
    for i in result:
        with open('D:\Face-Recognition\StudentDetails\StudentDetails.csv','rt')as f1:
            data1 = csv.reader(f1)
  
        

            for row in data1:
                 if i==row[0]:
        #subject starts
                    email_user = 'girik7411@gmail.com'
                    email_send = str(row[2])
                    subject = 'Today\'s Attendance'

                    msg = MIMEMultipart()
                    msg['From'] = email_user
                    msg['To'] = email_send
                    msg['subject'] = subject
                    body = '''Dear parent,
                                    This is to inform that today your son/daughter did not attend the college. You are requested to
                                    contact the counsellor and explain the reason for your child's absence. please make sure that the
                                    attendance percentage did not drop.

                                    Regards,
                                    
                                    HOD
                                    Department of CSE
                                    SACET'''
                    msg.attach(MIMEText(body,'plain'))

                    # attachment starts

                    #filename = fileName
                    #attachment = open(filename, 'rb')

                    #part = MIMEBase("application","octet-stream")
                    #part.set_payload((attachment).read())
                    #encoders.encode_base64(part)
                    #part.add_header("content-Disposition","attachment;filename = %s" %filename)

                    #msg.attach(part)
                    # attachment ends
                    text = msg.as_string()
                    #subject ends
                    server = smtplib.SMTP('smtp.gmail.com',587)

                    server.starttls()
                    # login 
                    server.login(email_user,'Kumari96')
                    #sending mail
                    server.sendmail(email_user,email_send,text)

                    server.close()
                  
        
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"    ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"   ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"   ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"   ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"   ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=800, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"   ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1100, y=500)
 
window.mainloop()
