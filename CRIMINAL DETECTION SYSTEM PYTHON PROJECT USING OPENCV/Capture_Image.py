import csv
import cv2
import os
import threading
#***********************************save image function to directory************************************************
def save_image(name, Id, sampleNum, gray, x, y, w, h):
    cv2.imwrite("TrainingImage" + os.sep + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])


#***********************************checking inserted values************************************************


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

#********************************Take image function***************************************************

def takeImages():

    print("***********************")
    print("**ADDING NEW CRIMINAL**")
    print("***********************")
    Id = input("ENTER CRIMINAL ID: ")
    name = input("ENTER NAME: ")
    crime_no=input("ENTER THE CRIME NO: ")

    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(40,40),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
#**********************************create a thread and call save function*******************************
                sampleNum = sampleNum + 1
                t = threading.Thread(target=save_image, args=(name, Id, sampleNum, gray, x, y, w, h))
                t.start()
#****************************************display the frame**********************************************
                cv2.imshow('frame', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
#************************break if the sample number is more than 170************************************
            elif sampleNum > 170:
                break
        cam.release()
        cv2.destroyAllWindows()
        row = [Id, name, crime_no]
        with open("CriminalDetails"+os.sep+"CriminalDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
            takeImages()
        if(name.isalpha()):
            print("Enter Numeric ID")
            takeImages()
