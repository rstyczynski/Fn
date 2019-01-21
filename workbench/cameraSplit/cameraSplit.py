#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 16:00:11 2019

@author: rstyczynski
"""
import time
import os
import cv2
import numpy as np


##
## Configure
##

# Active camera index as specified in camers list
activeCamera = 3

# Number of segments per axis
segments_x = segments_y = 1

# Image format. Use known file extensions as bmp, jpg, tiff, png
imageExt = "jpg"

# Keep images or delete previous ones, and keep only current frame
keepImages = True

# Remove all images after program end
cleanupAfterEnd = False

# Output directory
imageOutput = '/Volumes/RAMDisk/splitcam'


# Debug
debug = False


##
## Static configuration
##

cameras = []
# Camera connection strings
cameras.append(
    {
         'cameraType' : 1,
         'cameraName' : 'cam01',
         'cameraLocation' : 'testRoom',
         'cameraURL'  : 'http://192.168.1.108/cgi-bin/snapshot.cgi?channel=1',
         'cameraUser' : 'admin',
         'cameraPass' : 'welcome1',
         'cameraFPS'  : 1
    }
)

cameras.append(
    {
         'cameraType' : 2,
         'cameraName' : 'cam01',
         'cameraLocation' : 'testRoom',
         'cameraURL'  : 'https://raw.githubusercontent.com/madhawav/darknet/master/data/dog.jpg',
         'cameraUser' : '',
         'cameraPass' : '',
         'cameraFPS'  : 5
    }
)

cameras.append(
    {    
         'cameraType' : 2,
         'cameraName' : 'cam01',
         'cameraLocation' : 'testRoom',
         'cameraURL'  : 'http://lorempixel.com/400/200/sports/',
         'cameraUser' : '',
         'cameraPass' : '',
         'cameraFPS'  : 5
    }
)

cameras.append(
    {
         'cameraType' : 3,
         'cameraName' : 'cam01',
         'cameraLocation' : 'testRoom',
         'cameraURL'  : 0,
         'cameraUser' : '',
         'cameraPass' : '',
         'cameraFPS'  : 5
    }
)


##
## Proceed
##

cameraType = cameras[activeCamera]['cameraType']
cameraName = cameras[activeCamera]['cameraName']
cameraLocation = cameras[activeCamera]['cameraLocation']
cameraURL  = cameras[activeCamera]['cameraURL']
cameraUser = cameras[activeCamera]['cameraUser']
cameraPass = cameras[activeCamera]['cameraPass']
cameraFPS   = cameras[activeCamera]['cameraFPS']

# keep list of already saved image files
imageFiles = []

# images are stored in tmp directory to be moved in one step to target directory
# it's guarantee that no one will read partially written image. Linux guarantees 
# access to deleted file, if was opened before deletion. 
tmpPath=os.path.join(imageOutput, "tmp")
try:
    os.makedirs(tmpPath)
except OSError:
    if not os.path.isdir(tmpPath):
        raise

# remove images from output directory. Left after previous run of the software
imageFiles = os.listdir(imageOutput)
if debug: print("Initial cleanup:" + imageOutput, imageFiles)
for image in imageFiles:
    if debug: print(os.path.join(imageOutput, image))
    theFile = os.path.join(imageOutput, image)
    if os.path.isfile(theFile):    
        os.remove(theFile)  
        
##
## Main picture grabber loop
##
camera = None
frame = None
while True:
    # Get image from camera
    if cameraType == 1:
        import requests
        from requests.auth import HTTPDigestAuth
        #
        response = requests.get(cameraURL, auth=HTTPDigestAuth(cameraUser, cameraPass))
        image = np.fromstring(response.content, np.uint8)
        frame = cv2.imdecode(image, -1)
    elif cameraType == 2:
        import urllib
        #
        response = urllib.urlopen(cameraURL)
        arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(arr, -1)
    elif cameraType == 3:
        if camera == None:
            camera = cv2.VideoCapture(cameraURL)
        status, frame = camera.read()
    #
    if frame is None:
        raise Exception("Camera connection error.")
    
    # Remeber timestamp
    frameTimestamp = time.time()
    
    # Get size, compute segment size
    height = frame.shape[0]
    width = frame.shape[1]
    segment_size_x = int(width / segments_x)
    segment_size_y = int(height / segments_y)
    
    # Divide into segments
    segments = []
    ndx=0
    for x in range(0, width, segment_size_x):
        for y in range(0, height, segment_size_y):
            # does not copy data, just references
            segment = frame[y:y + segment_size_y, x:x+segment_size_x]
            segments.append(segment)
            ndx+=1
    ##
    ## Save segments
    ##
    for ndx in range(0, len(segments)):
        if debug: print(">>>>> Segment no.{0}".format(ndx))
        segment=segments[ndx]
        #outPath = os.path.join(imageOutput, "tmp", str(frameTimestamp) +'_' + str(ndx) + '_' + cameraLocation + '_' + cameraName + '.' + imageExt)
        outPath = os.path.join(imageOutput, "tmp", str(ndx) + '_' + cameraLocation + '_' + cameraName + '.' + imageExt)
        cv2.imwrite(outPath ,segment)
        if debug:
            cv2.imshow("", segment)
            cv2.waitKey(1)
    #
    #
    # delete previously created images
    if debug: print(imageFiles)
    if (len(imageFiles) > 0):
        if (keepImages == False):
            for image in imageFiles:
                theFile = os.path.join(imageOutput, image)
                if debug: print('Delete:' + theFile)
                if os.path.isfile(theFile):
                    os.remove(theFile)
    #
    # move current images to out directory
    imageFiles = os.listdir(tmpPath)
    if debug: print("tmp images:" + tmpPath, str(imageFiles))
    if debug: print("target path:" + imageOutput)
    for image in imageFiles:
        srcFile = os.path.join(tmpPath, image)
        dstFile = os.path.join(imageOutput, image)
        if os.path.isfile(srcFile):
            if debug: print("Move:" + srcFile, dstFile)
            os.rename(srcFile, dstFile)   
    #
    time.sleep(float(1) / cameraFPS)

##
## clean up
##
    
# remove images from output directory. 
if cleanupAfterEnd:
    imageFiles = os.listdir(imageOutput)
    if debug: print("Final cleanup:" + imageOutput, imageFiles)
    for image in imageFiles:
        theFile = os.path.join(imageOutput, image)
        if debug: print(theFile)
        if os.path.isfile(theFile):
            os.remove(theFile)  
 
    
