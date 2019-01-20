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
        if data and len(data) > 0:
            #
            # 1. decode byte stream
            #
            nparr=np.frombuffer(data, np.uint8)
            #
            # 3. convert image
            #
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)            
            #
            net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))
            #
            dark_frame = Image(img)
            results = net.detect(dark_frame)
            del dark_frame
            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(img, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                cv2.putText(img, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
            #
            # 4. write response to byte array
            #
            retval, buf = cv2.imencode('.jpg', img)
            #
            # 5 Convert buffer to bytes for row response
            res= buf.tobytes()
    except Exception as ex:
        res = "Exception:" + str(ex) + ' at ' + getActiveLine()
        return res 
    return response.RawResponse(
            ctx, response_data=res, headers={
                "Content-Type": "application/octet-stream",
            }
    )
if __name__ == "__main__":
    fdk.handle(handler)
