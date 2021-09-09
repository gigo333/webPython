from PIL import Image, ImageDraw
import math
import time
import socket

import numpy as np
from scipy.interpolate import griddata

from colour import Color

from struct import unpack

import cv2

#low range of the sensor (this will be blue on the screen)
MINTEMP = 26

#high range of the sensor (this will be red on the screen)
MAXTEMP = 32

#how many color values we can have
COLORDEPTH = 1024*8

ADDRESS="192.168.0.109"
PORT=1234

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def recvall(so : socket, l : int):
    buffer=b''
    while(len(buffer)<l):
        b=so.recv(l-len(buffer))
        #if len(b)==0:
            #return b''
        buffer+=b
    return buffer

class ThremalImg():

    def __init__(self):
        self.__imgBuff=b''
        self.maxtemp=0
        self.mintemp=0


    def run(self):
        so=None
        connected=False
        while(not connected):
            try:
                so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                so.connect((ADDRESS,PORT))
                connected=True
            except:
                time.sleep(0.05)


        points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
        grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

        #sensor is an 8x8 grid so lets do a square
        height = 240*2
        width = 240*2

        #the list of colors we can choose from
        blue = Color("indigo")
        colors = list(blue.range_to(Color("red"), COLORDEPTH))

        #create the array of colors
        colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

        displayPixelWidth = width / 30
        displayPixelHeight = height / 30

        img=Image.new("RGB", (height,width), (255,255,255))
        draw=ImageDraw.Draw(img)

        #let the sensor initialize
        time.sleep(.1)
            
        while(1):
            try:
                #read the pixels
                buffer=recvall(so, 256)
                pixels=np.array(unpack("<64f", buffer))
                maxtemp=pixels.max()
                mintemp=pixels.min()
                pixels = [map(p,mintemp, maxtemp, 0, COLORDEPTH - 1) for p in pixels]
                
                #perdorm interpolation
                bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
                
                #draw everything
                for ix, row in enumerate(bicubic):
                    for jx, pixel in enumerate(row):
                        draw.rectangle((displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight*(ix+1), displayPixelWidth*(jx+1)), colors[constrain(int(pixel), 0, COLORDEPTH- 1)] )
                
                numpy_image=np.array(img)
                opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
                is_success, im_buf_arr = cv2.imencode(".jpg", opencv_image)
                if(is_success):
                    self.imgBuff = im_buf_arr.tobytes()
                    self.maxtemp = maxtemp
                    self.mintemp = mintemp

            except:
                so.close()
                connected=False
                while(not connected):
                    try:
                        so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        so.connect((ADDRESS,PORT))
                        connected=True
                    except:
                        time.sleep(0.05)

    def getImg(self):
        return [self.imgBuff, self.mintemp, self.maxtemp]
