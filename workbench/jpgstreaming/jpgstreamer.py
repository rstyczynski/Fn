#!/usr/bin/env python
from flask import Flask, Response

import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import numpy as np
import cv2

import time, sys, threading

##
## Configure
##

# Image format. Use known file extensions as bmp, jpg, tiff, png
imageExt = "jpg"

# Listen only on given segment
imageSegment = "0"

# Listen only on given camera location
cameraLocation = "testRoom"

# Listen only on given camera name
cameraName = "cam01"

# Output directory
imageOutput = '/Volumes/RAMDisk/splitcam'

# Debug
debug = False

##
## Global variables
##
image_initial = open('film-2891853_1280.jpg', 'rb').read()
image_current = image_initial
image_lock = threading.Lock()
image_ready = True
image_initial = True

##
## Watch for new files
##

#filePattern=r'[0-9]+\.[0-9]+_' + imageSegment + '_' + cameraLocation + '_' +  cameraName + '\.' + imageExt
filePattern=r'' + imageSegment + '_' + cameraLocation + '_' +  cameraName + '\.' + imageExt
if debug: print('Image pattern:' + filePattern)

class ImageMonitor(PatternMatchingEventHandler):
    patterns=['*.' + imageExt]

    def on_created(self, event):
        global image_current
        global image_ready
        global image_lock
        #
        if re.search( filePattern, event.src_path):
            if debug: print('Recognized file:' + event.src_path) 
            with image_lock:
                if not image_ready:
                    print('/', end='', flush=True)
                    image_current = open(event.src_path, 'rb').read()
                    image_ready = True
                else:
                    print('.', end='', flush=True)

##
## Camera simulator
##
def get_frames():
    global image_current
    global image_initial
    global image_ready
    global image_lock
    
    while True:
        with image_lock:                 
            if image_ready:
                print('>', end='', flush=True)
                image_ready = False
                #
                if image_initial:
                    image_initial = False
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_current + b'\r\n' 
                           b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_current + b'\r\n')
                else:
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_current + b'\r\n')

##
## Flask main code
##

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(get_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    observer = Observer()
    observer.schedule(ImageMonitor(), path=imageOutput)
    observer.start()

    app.run(host='0.0.0.0', debug=True)

    observer.join()

