#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 11:06:22 2019

@author: rstyczynski
"""

import sys
import time

import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

##
## Configure
##

# Image format. Use known file extensions as bmp, jpg, tiff, png
imageExt = "jpg"

# Listen only on given segment
imageSegment = "0"

# Listen only on given camera location
cameraLocation = "dog\.jpg"

# Listen only on given camera name
cameraName = "web"

# Output directory
imageOutput = '/tmp/splitcam'

# Debug
debug = True


##
## Proceed
##

filePattern=r'[0-9]+\.[0-9]+_' + imageSegment + '_' + cameraLocation + '_' +  cameraName + '\.' + imageExt 
if debug: print 'Image pattern:' + filePattern

class MyHandler(PatternMatchingEventHandler):
    patterns=['*.' + imageExt]

    def process(self, event):
        print event.src_path, 'r'

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        if re.search( filePattern, event.src_path):
            if debug: print 'Recognized file:' + event.src_path
            # TODO put here image processing logic.
        else:
            if debug: print 'Unknown file:' + event.src_path

if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path=imageOutput)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
