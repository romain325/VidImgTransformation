import cv2


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
        
