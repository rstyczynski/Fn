import fdk
import json
import time

import cv2
import numpy

import base64

from PIL import Image
import cv2
from io import StringIO
import struct
import numpy as np
import linecache
import sys

def getActiveLine():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

response = "(-)"
def handler(ctx, data=None, loop=None):
    response = "OK"
    #
    try:
        if data and len(data) > 0:
            #
            # 1. decode base64
            #
            base64_string=struct.pack("b"*len(data),*data)
            img_utf = base64.b64decode(base64_string)
            nparr = np.fromstring(img_utf, np.uint8)
            #
            # 1. decode byte stream
            #
            #nparr=np.frombuffer(data, np.uint8)
            #
            # 2. decode image
            #
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            #
            # 3. convert image
            #
            edges = cv2.Canny(img_np,100,200)
            #
            # 4. enode bas64
            #
            retval, buffer = cv2.imencode('.jpg', edges)
            encoded = base64.urlsafe_b64encode(buffer)
            response = encoded
    except Exception as ex:
        response = "Exception:" + str(ex) + ' at ' + getActiveLine()
    #
    return response

if __name__ == "__main__":
    fdk.handle(handler)
