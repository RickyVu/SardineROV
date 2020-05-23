import numpy as np
import cv2
from HTTP_Connectors import HTTP_Sender
import time
Turn = 0 #int
def nothing(x):
    pass
def SliderLimit(minimum, range_):
    maximum = minimum+range_
    if maximum>255:
        maximum = 255
    return maximum
cv2.namedWindow('Sliders')
cv2.createTrackbar('H','Sliders',0,255,nothing)
cv2.createTrackbar('H_Range','Sliders',0,255,nothing)
cv2.createTrackbar('S','Sliders',0,255,nothing)
cv2.createTrackbar('S_Range','Sliders',0,255,nothing)
cv2.createTrackbar('V','Sliders',0,255,nothing)
cv2.createTrackbar('V_Range','Sliders',0,255,nothing)

cap = cv2.VideoCapture(0)
ret, frame = cap.read(0)
height = frame.shape[0]
width = frame.shape[1]
origin = (0, 0)
center = (width//2, height//2)
Sender = HTTP_Sender()
Sender.connect(1234)


while True:
    ret, frame = cap.read(0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    H = cv2.getTrackbarPos('H','Sliders')
    H = 102
    H_Range = cv2.getTrackbarPos('H_Range','Sliders')
    H_Range = 51
    S = cv2.getTrackbarPos('S','Sliders')
    S = 40
    S_Range = cv2.getTrackbarPos('S_Range','Sliders')
    S_Range = 140
    V = cv2.getTrackbarPos('V','Sliders')
    V = 90
    V_Range = cv2.getTrackbarPos('V_Range','Sliders')
    V_Range = 80
    lower_blue = np.array([H,S,V]) #110-130
    upper_blue = np.array([SliderLimit(H, H_Range),SliderLimit(S, S_Range),SliderLimit(V, V_Range)])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    grayImage = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    thresh, blackAndWhiteImage = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    white_elements = np.argwhere(blackAndWhiteImage == 255)
    x_total = 0
    y_total = 0
    for i in range(len(white_elements)):
        y_total+=white_elements[i][0]
        x_total+=white_elements[i][1]
    try:
        x_average = x_total//(len(white_elements))
        y_average = y_total//(len(white_elements))

        cv2.circle(blackAndWhiteImage, (x_average, y_average), 2, (255, 255, 255), 6)
        cv2.circle(blackAndWhiteImage, (width//2, height//2), 2, (255, 255, 255), 6)
        cv2.imshow('Black white image', blackAndWhiteImage)
        cv2.imshow('res', res)

        x_coordinate = x_average-width//2
        output = x_coordinate/(width//2)
        if not Sender.disconnected:
            print(output)
            Sender.send(str(output))
        #print("%.2f" % output)
        #time.sleep(1)
        
    except:
        pass
    #print(output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break


cap.release()
cv2.destroyAllWindows()
