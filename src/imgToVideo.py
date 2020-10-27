#!/usr/bin/python3

from driveInteraction import dl_drive_folder
from imageInteraction import resize, remove_tmp_file, get_imgArray, createTmpFolder
import cv2
import glob
import sys, getopt, os

helpMessage = "Help on usage:\nimgToVideo.py -i <InputFolder> -o <OutputFile> [-f <framerate>] [-r <googleDriveFolderUrl>]"

def parse_args(argv):
    inputfolder = ''
    outputfile = ''
    framerate = 1
    remotePath = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:f:r:", ["inputfolder", "outputfile","framerate","remotePath"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(helpMessage)
            sys.exit()
        elif opt in ("-i", "--inputfolder"):
            inputfolder = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-f", "--framerate"):
            framerate = float(arg)
        elif opt in ("-r", "--remotePath"):
            remotePath = arg
    
    if inputfolder == '' or outputfile == '':
        print(helpMessage)
        sys.exit()

    return inputfolder, outputfile, framerate, remotePath

def video_creation(folderPath, outputfile, framerate):
    img_array = get_imgArray(folderPath)
    
    print("NB Images: " + str(len(img_array)))

    print("Video Rendering, Pls Wait ...")

    h,w,_ = img_array[0].shape
    out = cv2.VideoWriter(outputfile + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'),framerate,(w,h))

    for i in range(len(img_array)):
        out.write(img_array[i])
        print("#"*i)
    out.release()

    print("**************************************")
    print("Video Successfully rendered at: " + outputfile)
    print("**************************************")

def main(argv):
    inputfolder, outputfile, framerate, remotePath = parse_args(argv)
    createTmpFolder(inputfolder)
    if(remotePath != ''):
        dl_drive_folder(remotePath, inputfolder)
    resize(inputfolder)
    video_creation(inputfolder, outputfile, framerate)
    remove_tmp_file(inputfolder)

if __name__ == '__main__':
    main(sys.argv[1:])