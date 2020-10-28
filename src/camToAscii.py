#!/usr/bin/python3
import os, getopt, sys
from videoInteraction import useCam


def parse_args(argv):
    helpMessage = "Usage Help:\n./camToAscii [-f <framerate>] [-c | --camera]"
    framerate = 50
    seeCam = False

    try:
        opts, args = getopt.getopt(argv, "hf:c", ["framerate","camera"])
    except getopt.GetoptError:
        print(helpMessage)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(helpMessage)
            sys.exit()
        elif opt in ("-f", "--framerate"):
            framerate = int(arg)
        elif opt in ("-c", "--camera"):
            seeCam = True

    return framerate, seeCam

def main(argv):
    framerate, seeCam = parse_args(argv)
    useCam(framerate, seeCam)

if __name__ == '__main__':
    main(sys.argv[1:])