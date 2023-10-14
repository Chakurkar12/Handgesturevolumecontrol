import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
###################################################
wCam , hCam = 640 , 480


cap = cv2.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4 , hCam)
pTime = 0
vol = 0
volBar = 400
volper = 0
detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
#volume.setMasterVolumelevel(-20.0 , None)

minvol = volrange[0]
maxvol = volrange[1]


while True:
    success , img  = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img , draw = False)
    if(len(lmlist) != 0):
        #print(lmlist[4] , lmlist[8])
        x1 , y1 = lmlist[4][1] , lmlist[4][2]
        x2 , y2 = lmlist[8][1] , lmlist[8][2]
        cx , cy = (x1 + x2) //2 , (y1 + y2)//2

        cv2.circle(img , (x1 , y1) , 12 , (138,43,226) , cv2.FILLED)
        cv2.circle(img , (x2 , y2) , 12 , (138,43,226) , cv2.FILLED)

        cv2.line(img , (x1 , y1) , (x2 , y2) , (128,0,128) , 3)
        cv2.circle(img , (cx , cy) , 15 , (138,43,226) , cv2.FILLED)

        length = math.hypot((x2 - x1) , (y2 - y1))
        #print(length)
        #handrange = 50 to 300
        #vol range is from -65 to 0

        vol = np.interp(length , [50 , 300] , [minvol , maxvol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])
        print(int(length) , vol)
        volume.SetMasterVolumeLevel(vol, None)
        if( length < 50):
            cv2.circle(img , (cx , cy) , 12 , (0,43,226) , cv2.FILLED)
    cv2.rectangle(img , (50 , 150) , (85 , 400) , (0,43,226) , 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 43, 226), cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img , f'FPS: {int(fps)}' , (40 , 70) , cv2.FONT_HERSHEY_TRIPLEX , 1 , (255 , 0 , 0) , 2)
    cv2.putText(img, f'{int(volper)} %', (30, 450), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("img" , img)
    cv2.waitKey(1)

