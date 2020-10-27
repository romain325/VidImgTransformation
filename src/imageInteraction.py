
from PIL import Image
import sys, os
import glob
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import cv2

def resize(folderPath):
    print("**************************************")
    print("Start Images Processing")
    print("**************************************")
    for item in getGlobItems(folderPath):
        if os.path.isfile(item):
            im = Image.open(item)
            imResize = im.resize((1920,1080), Image.ANTIALIAS)
            imResize.save(folderPath + "/tmp/" + item.split("/")[-1])
            print("Done: " + item)
        else:
            print("Not A Valid Image Folder")
            sys.exit()
    print("**************************************")
    print("Image Processing: Done")
    print("**************************************")

def remove_tmp_file(folderPath):
    for item in getGlobItems(folderPath,"tmp"):
        os.remove(item)
    for item in glob.glob(folderPath + "/driveRenderTMP_*"):
        os.remove(item)
    os.rmdir(folderPath+ "/tmp")

def createTmpFolder(folderPath):
    print("*** CREATING TMP FOLDER ***")
    os.mkdir(folderPath + "/tmp")

def get_imgArray(folderPath):
    img_array = []

    for filename in sorted(getGlobItems(folderPath,"tmp")):
        img = cv2.imread(filename)
        print(img.shape)
        img_array.append(img)

    return img_array

def getGlobItems(folderPath, subFolder = ''):
    return [f for files in [glob.glob(folderPath + "/" +subFolder + "/*" + e) for e in [".png",".jpg"]] for f in files]

def getAvgColor(img):
    avg_row = np.average(img, axis = 0)
    avg_color = np.average(avg_row, axis =0)
    return avg_color

def getDomColor(img):
    NClusters = 5
    img = img.resize((10,10))
    ar = np.asarray(img)
    ar = ar.reshape(scipy.product(ar.shape[:2]), ar.shape[2]).astype(float)

    codes,dist = scipy.cluster.vq.kmeans(ar, NClusters)
    vecs, dist = scipy.cluster.vq.vq(ar,codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    return peak