import cv2
import numpy as np
import pickle

Log=[]
histw=[]
FPS=24
def SceneCut(videopath, name):
    print("장면 분할")

    for i in range(256):
        histw.append(0)

    cap = cv2.VideoCapture(videopath)
    while True:
        retval, frame = cap.read()
        if not retval:
            cap.release()
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist(images=[frame], channels=[0], mask=None, histSize=[256], ranges=[0, 256])
        sum = 0
        for i in range(256):
            sum += abs(hist[i] - histw[i])
            histw[i] = hist[i]
        Log.append(sum / 256)
    cutline = 0
    Max = 0
    for i in Log:
        if Max < i:
            Max = i
        cutline = cutline + i

    cutline = cutline / len(Log)
    cutline = (cutline + Max) / 3
    Cutlst = []
    for i in range(len(Log)):
        if Log[i] > cutline:
            Cutlst.append(i)
    i = 0
    
    while i < len(Cutlst) - 1:
        if Cutlst[i + 1] - Cutlst[i] < FPS / 2:
            Cutlst[i] = (Cutlst[i] + Cutlst[i + 1]) / 2
            Cutlst.remove(Cutlst[i + 1])
        else:
            i = i + 1

    ##########################################
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoCapture(videopath)
    framecount = 0
    cutcur = 0
    framesize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    histList = np.array([])
    start = 0
    end = 0
    
    
    out = cv2.VideoWriter("./" + str(cutcur) + '_' + name + '.mp4', fourcc, FPS, framesize)
    while True:
        retval, frame = cap.read()
        if not retval:
            cap.release()
            out.release()
            break
        if cutcur < len(Cutlst) and int(Cutlst[cutcur]) <= framecount:
            try:
                out.release()
            except:
                pass
            end = framecount - 1
            if cutcur != len(Cutlst):
                cutcur += 1
            if not start >= end:
                ######
                
                ######
                start = framecount
            out = cv2.VideoWriter("./" + str(cutcur - 1) + '_' + name + '.mp4', fourcc, FPS, framesize)

        out.write(frame)
        framecount = framecount + 1



    print("분할 완료")
if __name__=="__main__":
    SceneCut("yourVideoPath.mp4", "VideoName")
    
