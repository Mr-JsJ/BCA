import datetime
import os
import time
import cv2
import pandas as pd
from pandas import DataFrame

import automail
import threading
def recognize_criminal():
    a='none'
    d='none'
    camid='parathodu'
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("CriminalDetails"+os.sep+"CriminalDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['CRIMINAL ID', 'NAME', 'DATE', 'TIME','LOCATION']
    attendance: DataFrame = pd.DataFrame(columns=col_names)
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)

        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 100:
                aa = df.loc[df['CRIMINAL ID'] == Id]['NAME'].values
                confstr = "{0}%".format(round(100 - conf))
                tt = str(Id)+"-"+aa
            else:
                Id = ' Unknown '
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                d=[Id, aa]
                p=[Id, aa, date, timeStamp,camid]
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp,camid]
            tt = str(tt)[2:-2]

            if(100-conf) > 64:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100-conf) > 55:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                g = 1
            elif (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)
        detected = attendance.drop_duplicates(subset=['CRIMINAL ID'], keep='first')
        cv2.imshow('Detected', im)
#***********************CALLING AUTO MAIL FUNCTION FOR 'ALERT'**************
        if str(a) != str(d):
            img=aa + "." + str(Id) + ".jpg"#image file name
            imgpath="mailed" + os.sep + img #image file directory
            cv2.imwrite(imgpath, im)  #image file saving to the directory
            mail_thread = threading.Thread(target=automail.mail, args=(p,img))
            mail_thread.start()
            a = str(d)
#***********************END OF THE LOOP AFTER PRESS 'q'*********************
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Notification"+os.sep+"notification_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
    detected.to_csv(fileName, index=False)
    print(fileName)
    print("STOPED SURVEILLANCES")
    cam.release()
    cv2.destroyAllWindows()

recognize_criminal()
