import fdk
from fdk import response

import cv2
import numpy as np
import linecache
import sys


from pydarknet import Detector, Image


def getActiveLine():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def handler(ctx, data=None, loop=None):
    res=""
    try:
        net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))
        res = str(net)
    except Exception as ex:
        res = "Exception:" + str(ex) + ' at ' + getActiveLine()
        return res 
    return res


if __name__ == "__main__":
    fdk.handle(handler)
