import numpy as np
import cv2
from pubsub import pub
from ModuleBase import Module

class CV_Test(Module):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def run(self):
        ret, frame = self.cap.read()
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
'''
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & False:
        break
cap.release()
cv2.destroyAllWindows()
'''
