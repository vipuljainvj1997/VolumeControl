import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam = 640,480

cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetetctor(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
volBar = 400
volPer = 0

pTime=0
while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList)!=0:
    # print(lmList[4])
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2), 15, (255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy), 15, (255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        #Hand Range - 22 to 245
        #Volume Range - -48 to 12

        vol = np.interp(length,[22,245],[minVol,maxVol])
        volBar = np.interp(length,[22,245],[400,150])
        volPer = np.interp(length,[22,245],[0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<22:
            cv2.circle(img,(cx,cy), 15, (0,255,0),cv2.FILLED)
        if length>245:
            cv2.circle(img,(x1,y1), 15, (0,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2), 15, (0,0,255),cv2.FILLED)
    cv2.rectangle(img, (50,150), (85,400), (255,0,0),3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (255,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cTime = time.time()
    fps = 1/cTime-pTime
    pTime = cTime

    cv2.putText(img,f'FPS{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)


    cv2.imshow("image", img)
        
    key = cv2.waitKey(1)
    if key == ord('q'):  # Check if 'q' is pressed
        print("Exiting...")
        break

