from PIL import Image, ImageDraw, ImageFont
import math
import random
import numpy as np
from imageInteraction import getAvgColor, getDomColor
import os


def getAverageL(image): 
    im = np.array(image)
    w,h = im.shape 
    return np.average(im.reshape(w*h)) 


def ConvToAscii(imagePath):
    img = Image.open(imagePath)
    aimg = []
    gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    gscale2 = '@%#*+=-:. '
    scale = 0.43
    cols = 80

    W, H = img.size
    w = W/cols
    h = w/scale
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows)) 
    print("tile dims: %d x %d" % (w, h))     
    # check if image size is too small 
    if cols > W or rows > H: 
        print("Image too small for specified cols!") 
        exit(0)

    pixels = img.load()
    outputImage = Image.new('RGB', (W,H), color=(0,0,0))
    draw = ImageDraw.Draw(outputImage)

    for j in range(rows):
        y1 = int(j*h) 
        y2 = int((j+1)*h) 
  
        if j == rows-1: 
            y2 = H 
  
        aimg.append("") 

        for i in range(cols):
            x1 = int(i*w) 
            x2 = int((i+1)*w) 

            if i == cols-1: 
                x2 = W 
  
            part = img.crop((x1, y1, x2, y2)) 
            
            #color = getAvgColor(part)
            color = part.getpixel((2,2))
            
            # TODO PERFORMANCE ISSUE
            #color = getDomColor(part)
            
            avg = int(getAverageL(part.convert('L'))) 
  
            # TODO CLI arg to choose set
            #gsval = gscale2[int((avg*9)/255)]
            gsval = gscale1[int((avg*69)/255)] 


            font = ImageFont.truetype(os.getcwd() + "/src/ASCII/Lucon.ttf",36)
            draw.text((int(i*w), int(j*h)), gsval, fill=(int(color[0]), int(color[1]), int(color[2])), font=font)

            aimg[j] += gsval 
      
    for r in aimg:
        print(r)
    outputImage.save(imagePath)
    return aimg 
