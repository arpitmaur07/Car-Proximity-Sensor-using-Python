import cv2
from threading import Thread
import numpy as np
from playsound import playsound

alarmOn=False

def soundAlerm(soundFile):
    while alarmOn==True:
        playsound(soundFile)

cap=cv2.VideoCapture(0)
_,prev=cap.read()
prev=cv2.flip(prev,1)
_,new=cap.read()
new=cv2.flip(new,1)
while True:
    diff=cv2.absdiff(prev,new)
    diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    diff=cv2.blur(diff,(5,5))
    _,thresh=cv2.threshold(diff,10,255,cv2.THRESH_BINARY)
    thresh=cv2.dilate(thresh,None,3)
    thresh=cv2.erode(thresh,np.ones((4,4)),1)
    contor,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contours in contor:
        if cv2.contourArea(contours)>190000:            
            if not alarmOn:        
                alarmOn=True  
                t=Thread(target=soundAlerm, args=("C:/Users/Arpit Maurya/Desktop/Programs/car/3rd/alarm.wav",))
                t.daemon=True
                t.start()
                if alarmOn==True:
                    pass
        alarmOn=False   
             
    cv2.imshow('frame',prev)
    prev=new
    _,new=cap.read()
    new=cv2.flip(new,1)
    if cv2.waitKey(1)==ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()