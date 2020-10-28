import cv2
import os
from ImgToAscii import ConvToAscii

def saveFrame(videoCap, sec, cnt):
    videoCap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrame, image = videoCap.read()
    if hasFrame:
        cv2.imwrite("tmp/frame"+str('{:04}'.format(cnt))+".jpg", image)
    return hasFrame

def saveAllFrames(fileName, outFolder, frameRate):
    video = cv2.VideoCapture(fileName)

    second = 0
    count = 1
    ctn = saveFrame(video, second, count)

    while ctn:
        count += 1
        second = round(second + frameRate, 2)
        ctn = saveFrame(video, second, count)
        

def printASCII(frame):
    arr = ConvToAscii(frame, False)
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

    for i in arr:
        print(i)

def useCam(framerate, seeCam):
    vc = cv2.VideoCapture(0)

    if vc.isOpened():
        ctn, frame = vc.read()
    else:
        ctn = False
    
    while ctn:
        ctn, frame = vc.read()
        
        if seeCam:
            cv2.imshow('frame', frame)
        
        printASCII(frame)

        key = cv2.waitKey(framerate)

        if key == 27 or key == 113:
            vc.release()
            break
