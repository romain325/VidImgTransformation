#!/usr/bin/python3

import sys, getopt, os
from imageInteraction import createTmpFolder, remove_tmp_file, getGlobItems
from videoInteraction import saveAllFrames
from ImgToAscii import ConvToAscii
from imgToVideo import video_creation


def parse_args(argv):
    helpMessage = "Help Usage:\n./videoToFakeAscii -i <InputFile> [-o <OutputFile>] [-f <FrameRate>]"
    inputfile = ''
    outputfile = ''
    framerate = 1
    remotePath = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:f:r:", ["inputfile", "outputfile","framerate","remotePath"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(helpMessage)
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-f", "--framerate"):
            framerate = float(arg)
        elif opt in ("-r", "--remotePath"):
            remotePath = arg
    
    if inputfile == '':
        print(helpMessage)
        sys.exit()
    
    if outputfile == '':
        outputfile = os.getcwd() + "/output"

    return inputfile, outputfile, framerate, remotePath



def main(argv):
    currFolder = os.getcwd()
    
    inputfile, outputfile, framerate, remotePath = parse_args(argv)
    createTmpFolder(currFolder)
    saveAllFrames(inputfile, outputfile, 1/framerate)
    for i in getGlobItems(currFolder, "tmp"):
        ConvToAscii(i)

    video_creation(currFolder, outputfile, framerate)
    
    remove_tmp_file(currFolder)
    

if __name__ == '__main__':
    main(sys.argv[1:])