import sys
import cv2
import numpy

stdin = sys.stdin.buffer.read()
array = numpy.frombuffer(stdin, dtype='uint8')
img = cv2.imdecode(array, 1)

edges = cv2.Canny(img,100,200)

cv2.imshow("window", edges)
cv2.waitKey()

