import numpy as np
import cv2
import copy
import re
from pubsub import pub
from ModuleBase import Module
from PubManager import pub_to_manager


Strafe_Deadzone = 30         #coordinate of CV display
Yaw_Deadzone = 0.2           #Radians
Updown_Deadzone = (70, 100)  #coordinate of CV display, [0]lower bound, [1]upper bound
max_line_distance = Updown_Deadzone[1]+70

def nothing(x):
    pass
def SliderLimit(minimum, range_):
    maximum = minimum+range_
    if maximum>255:
        maximum = 255
    return maximum
'''
cv2.namedWindow('Sliders')
cv2.createTrackbar('H','Sliders',0,255,nothing)
cv2.createTrackbar('H_Range','Sliders',0,255,nothing)
cv2.createTrackbar('S','Sliders',0,255,nothing)
cv2.createTrackbar('S_Range','Sliders',0,255,nothing)
cv2.createTrackbar('V','Sliders',0,255,nothing)
cv2.createTrackbar('V_Range','Sliders',0,255,nothing)
'''

def get_length(point1, point2):
    length = (((point1[0]- point2[0])**2)+(point1[1]-point2[1])**2)**(1/2)
    return abs(length)

def get_gradient(point1, point2):
    gradient = (point2[1]-point1[1])/(point2[0]-point1[0])
    return gradient

def within_range(value, lower_bound, upper_bound):
    if lower_bound<value and value< upper_bound:
        return True
    else:
        return False

def PowerFunction(A, B):
    if A >=0:
        return 1/B*(((B+1)**A)-1) 
    else:
        return -1/B*(((B+1)**-A)-1) 

class line_attr():
    def __init__(self):
        self.length = None
        self.angle = None
        self.top_intersect_x = None

    def set(self, List):
        self.length = List[0]
        self.angle = List[1]
        self.top_intersect_x = List[2]

class TransectLine(Module):
    def __init__(self, drive_power=0.3, strafe_mod=0.5, yaw_mod=0.5, updown_mod=0.99, simulation = False):
        pub.subscribe(self.showListener, 'show_transectline')
        pub.subscribe(self.activeListener, 'activate_transectline')
        pub.subscribe(self.simulation_photo_listener, "simulation_photo")
        #self.cap = cv2.VideoCapture(0)
        #ret, frame = self.cap.read()
        self.show = False
        self.drive_power, self.strafe_mod, self.yaw_mod, self.updown_mod = float(drive_power), float(strafe_mod), float(yaw_mod), float(updown_mod)
        self.captureON = False
        self.active = False
        self.simulation = simulation
        self.cap = None

    def showListener(self, message):
        self.show = message

    def activeListener(self, message):
        self.active = message

    def simulation_photo_listener(self, message):
        self.cap = message

    def relative(self, cv_coordinate, self_defined_center):
        return (cv_coordinate[0] - self_defined_center[0], -cv_coordinate[1] + self_defined_center[1])

    def run(self):
        if self.active:
            #pub.sendMessage("transectline", message = [1, 2, 3, 4, 5, 6])
            #pub_to_manager("transectline", message = [1, 2, 3, 4, 5, 6])
            #print("active: ",self.active)
            #print("show: ", self.show)
            if self.captureON == False:
                if self.simulation==False:
                    self.cap = cv2.VideoCapture(0)
                    self.captureON = True


                
                '''

                cv2.namedWindow('Sliders')
                cv2.createTrackbar('H','Sliders',0,255,nothing)
                cv2.createTrackbar('H_Range','Sliders',0,255,nothing)
                cv2.createTrackbar('S','Sliders',0,255,nothing)
                cv2.createTrackbar('S_Range','Sliders',0,255,nothing)
                cv2.createTrackbar('V','Sliders',0,255,nothing)
                cv2.createTrackbar('V_Range','Sliders',0,255,nothing)
                '''
                
            ret, frame = self.cap.read()

            height = frame.shape[0]
            width = frame.shape[1]
            origin = (0, 0)
            center = (width//2, height//2)

            process = np.zeros([height,width,1],dtype=np.uint8)
            process.fill(255)

            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            H = cv2.getTrackbarPos('H','Sliders')
            H = 102
            H_Range = cv2.getTrackbarPos('H_Range','Sliders')
            H_Range = 51
            S = cv2.getTrackbarPos('S','Sliders')
            S = 51
            S_Range = cv2.getTrackbarPos('S_Range','Sliders')
            S_Range = 128
            V = cv2.getTrackbarPos('V','Sliders')
            V = 102
            V_Range = cv2.getTrackbarPos('V_Range','Sliders')
            V_Range = 71
            lower_blue = np.array([H,S,V]) #110-130
            upper_blue = np.array([SliderLimit(H, H_Range),SliderLimit(S, S_Range),SliderLimit(V, V_Range)])


            
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            res = cv2.bitwise_and(frame,frame, mask= mask)
            median = cv2.medianBlur(res,5)
            
            #cv2.imshow('res',res)
            grayscaled = cv2.cvtColor(median,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('grayscaled',grayscaled)
            '''
            kernel = np.ones((10,10),np.uint8)
            erosion = cv2.erode(grayscaled,kernel,iterations = 1)
            cv2.imshow('erosion',erosion)
            '''
            #retval, threshold = cv2.threshold(grayscaled, 10, 255, cv2.THRESH_BINARY)

            #cv2.imshow('gray', grayscaled)
            # The bitwise and of the frame and mask is done so  
            # that only the blue coloured objects are highlighted  
            # and stored in res 
            #res = cv2.bitwise_and(frame,frame, mask= mask) 
            #Filter out all colours except for a range of blue
            
            #gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            #cv2.imshow('gray',gray)

            edges = cv2.Canny(grayscaled,50,150,apertureSize = 3)
            #cv2.imshow('edges',edges)
            '''
            theta = np.pi / 180
            rho = 50
            threshold = 15  # minimum number of votes (intersections in Hough grid cell)
            min_line_length = 50  # minimum number of pixels making up a line
            max_line_gap = 20
            lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),min_line_length, max_line_gap)
            '''
            point1_x, point1_y, point2_x, point2_y = width//2, height, width//2, 0
            lines = cv2.HoughLines(edges,10,np.pi/180, 200, 0) 
            line_amount = 4
            coordinates = []
            lines_seen = line_amount
            #Lines = [line_attr() for i in range(line_amount)]
            Lines = [] 
            pos_length = 0
            pos_len_count = 1
            neg_length = 0
            neg_len_count = 1
            for i in range(0, line_amount):
                try:
                    for r,theta in lines[i]:
                        
                        # Stores the value of cos(theta) in a 
                        a = np.cos(theta) 
                      
                        # Stores the value of sin(theta) in b 
                        b = np.sin(theta) 
                          
                        # x0 stores the value rcos(theta) 
                        x0 = a*r 
                          
                        # y0 stores the value rsin(theta) 
                        y0 = b*r 
                          
                        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
                        x1 = int(x0 + 1000*(-b)) 
                          
                        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
                        y1 = int(y0 + 1000*(a)) 
                      
                        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
                        x2 = int(x0 - 1000*(-b))

                        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
                        y2 = int(y0 - 1000*(a))

                        ###
                        
                        #y - y2 = s(x - x2)
                        #y = sx - sx2 + y2
                        s = get_gradient((x1,y1), (x2, y2))
                        t = -x2*s+y2

                        ###
                        
                        cv2.line(process, (x1, y1), (x2,y2), (0, 0, 255), 1)

                        m = -1/s
                        k = -m*center[0] + center[1]

                        ###
                        
                        #y - y2 = s(x - x2)
                        #y = sx - sx2 + y2
                        #y = sx + t

                        #y - centery = m(x - centerx)
                        #y = mx - mcenterx + centery
                        #y = mx + k

                        #sx + t = mx + k
                        #x(m-s) = t-k
                        #x = (t-k)/(m-s)

                        x_intersect = round((t-k)/(m-s))
                        y_intersect = round(s*x_intersect + t)
                        intersect = (x_intersect, y_intersect)
                       
                        remove = False
                        for coordinate in coordinates:
                            if within_range(x_intersect, coordinate[0]-50, coordinate[0]+50) and within_range(y_intersect, coordinate[1]-50, coordinate[1]+50):
                                line_amount -= 1
                                lines_seen -= 1
                                remove = True
                                continue  

                        if remove == True:
                            continue
                        coordinates.append(intersect)
           

                        ###
                        
                        cv2.line(process,(center),(intersect),(0,0,255),1)
                        cv2.circle(process, (intersect), 2, (0, 0, 255), 2)
                        cv2.circle(process, (center), 2, (0, 0, 255), 2)

                        if x_intersect < center[0]:
                            length = -1*get_length((center), (intersect))
                            neg_length = neg_length + length
                            neg_len_count +=1
                        else:
                            length = get_length((center), (intersect))
                            pos_length = pos_length + length
                            pos_len_count += 1
                        abs_length = abs(length)
                        
                        angle = np.arctan(self.relative(intersect, center)[1]/self.relative(intersect, center)[0])
                        #print(angle)
                        if self.relative(intersect, center)[1]>0 and self.relative(intersect, center)[0] < 0:
                            angle = np.pi + angle
                        if self.relative(intersect, center)[1]<0 and self.relative(intersect, center)[0] < 0:
                            angle = angle + np.pi
                        if self.relative(intersect, center)[1]<0 and self.relative(intersect, center)[0] > 0:
                            angle = 2*np.pi - angle*-1
                        
                        ###

                        #y = sx + t
                        #0 = sx + t
                        #-t = sx
                        #x = -t/s

                        top_intersect_x = -t/s
                        top_intersect = (top_intersect_x, 0)

                        ###
                        
                        #Lines[i].set((length, angle, top_intersect_x))
                        Lines = Lines + [line_attr()]
                        Lines[-1].set((length, angle, top_intersect_x))
                except:
                    lines_seen = lines_seen - 1
            

            if lines_seen > 0:
                neg_length = neg_length/neg_len_count
                pos_length = pos_length/pos_len_count
                Length_Deviation = pos_length + neg_length
                if pos_length == 0 or neg_length == 0: #If one side gone
                    pos_length = pos_length *2
                    neg_length = neg_length *2
                Line_Distance = (abs(neg_length) + pos_length)/2

                
                Total_Top = 0
                Top_pos = [0, 0] #value, amount
                Top_neg = [0, 0]
                Total_Angle = 0
                Angles = lines_seen
                #Total_Acute_Angle = 0
                #Total_Obtuse_Angle = 0
                #Total_Right_Angle = 0
                #Angle_Counter = [1, 1, 1, 3]  #Acute, Obtuse, Right, Types
                for i in range(line_amount):
                    try:
                        if Lines[i].top_intersect_x > center[0]:
                            Top_pos[0] = Top_pos[0] + Lines[i].top_intersect_x
                            Top_pos[1] = Top_pos[1] + 1
                        elif Lines[i].top_intersect_x < center[0]:
                            Top_neg[0] = Top_neg[0] + Lines[i].top_intersect_x
                            Top_neg[1] = Top_neg[1] + 1

                        if Lines[i].angle < np.pi/2:
                            Angle = Lines[i].angle + np.pi/2
                        elif Lines[i].angle > np.pi/2 and Lines[i].angle < np.pi:
                            Angle = Lines[i].angle - np.pi/2
                        elif Lines[i].angle> np.pi and Lines[i].angle< np.pi*3/2:
                            Angle = Lines[i].angle - np.pi/2
                        elif Lines[i].angle> np.pi*3/2:
                            Angle = Lines[i].angle - np.pi*3/2
                        else:
                            Angle = 0
                        #print(Angle)
                        Total_Angle = Total_Angle + Angle

                        '''
                        if Angle < np.pi/2:
                            Total_Acute_Angle = Total_Acute_Angle + Angle
                            Angle_Counter[0] += 1
                        elif Angle > np.pi/2:
                            Total_Obtuse_Angle = Total_Obtuse_Angle + Angle
                            Angle_Counter[1] += 1
                        elif Angle == np.pi/2:
                            Total_Right_Angle = Total_Right_Angle + Angle
                            Angle_Counter[2] += 1
                        '''
                    except:
                        pass
                Total_Angle = Total_Angle/Angles
                    
                if Top_pos[1] != 0 and Top_neg[1] != 0:
                    Total_Top = (Top_pos[0]/Top_pos[1] + Top_neg[0]/Top_neg[1])/2
                elif Top_pos[1] == 0:
                    Total_Top = (Top_neg[0]/Top_neg[1])
                elif Top_neg[1] == 0:
                    Total_Top = (Top_pos[0]/Top_pos[1])
                '''    
                Angles.append(Total_Acute_Angle/Angle_Counter[0])
                Angles.append(Total_Obtuse_Angle/Angle_Counter[1])
                Angles.append(Total_Right_Angle/Angle_Counter[2])
                
                for i in range(3):
                    if Angle_Counter[i] == 1:
                        Angle_Counter[3] -= 1
                    else:
                        pass
                        Total_Angle = Total_Angle + Angles[i]
                Total_Angle = Total_Angle/Angle_Counter[3]
                '''
                
                cv2.circle(process, (round(Total_Top), 0), 2, (0, 0, 255), 2)

            else:
                Total_Top = center[0]
                Line_Distance = (Updown_Deadzone[0]+Updown_Deadzone[1])/2
                Total_Angle = np.pi/2
                Length_Deviation = 0

            '''
            if Total_Top <center[0] - 30:
                print('Move Right')
            elif Total_Top > center[0] - 30 and Total_Top<center[0] + 30:
                print("Don't Move")
            else:
                print('Move Left')

            
            if Total_Angle > np.pi/2 - 0.2 and Total_Angle < np.pi/2 + 0.2:
                print("Don't turn")
            elif Total_Angle > np.pi/2 + 0.2:
                print('Turn Left')
            elif Total_Angle < np.pi/2 - 0.2:
                print('Turn Right')

            if Line_Distance > 100:
                print("Go Higher")
            elif Line_Distance<70:
                print("Go Lower")
            else:
                print("Height OK")
            print('\n\n\n\n\n\n')
            '''

            '''
            #Strafe_Power = Length_Deviation/(width/2)
            Yaw_Power =(Total_Top-width//2)/(width//2)
            Updown_Power = 0
            if Line_Distance > 150:
                Updown_Power = (150-Line_Distance)/100
                if Updown_Power > 1:
                    Updown_Power = 1
            elif Line_Distance < 100:
                Updown_Power = (100-Line_Distance)/100
            
            Message = (Strafe_Power,Drive_Power,Yaw_Power,Updown_Power,0,0) #Strafe, drive, yaw, updown, 0, 0
            '''
           
            if Total_Top > center[0] - Strafe_Deadzone and Total_Top<center[0] + Strafe_Deadzone:
                Total_Top = width/2
            Strafe_Power = (Total_Top-width/2)/(width/2)
            if Strafe_Power > 1:
                Strafe_Power = 1
            elif Strafe_Power < -1:
                Strafe_Power = -1

            if Total_Angle > np.pi/2 - Yaw_Deadzone and Total_Angle < np.pi/2 + Yaw_Deadzone:
                Total_Angle = np.pi/2
            Yaw_Power = (-Total_Angle+np.pi/2)/(np.pi/2)

            if Line_Distance < Updown_Deadzone[1] and Line_Distance>Updown_Deadzone[0]:
                Line_Distance = max_line_distance/2
            elif Line_Distance<=Updown_Deadzone[0]:
                Line_Distance = Line_Distance*((max_line_distance/2)/Updown_Deadzone[0])
            elif Line_Distance >= Updown_Deadzone[1]:
                Line_Distance = ((Line_Distance - Updown_Deadzone[1])*((max_line_distance/2)/(max_line_distance-Updown_Deadzone[1])))+max_line_distance/2
            Updown_Power = (Line_Distance-max_line_distance/2)/(max_line_distance/2)
            if Updown_Power > 1:
                Updown_Power = 1
            elif Updown_Power < -1:
                Updown_Power = -1

            #Value Modifiers
            Drive_Power = self.drive_power          #0-1
            Strafe_Power = PowerFunction(Strafe_Power, self.strafe_mod)
            Yaw_Power = PowerFunction(Yaw_Power, self.yaw_mod)
            Updown_Power = PowerFunction(Updown_Power, self.updown_mod)

            if self.show:
                cv2.imshow('frame',frame)
                cv2.imshow('process', process)

            Powers = [Strafe_Power,Drive_Power,Yaw_Power,Updown_Power,0,0] #Strafe, drive, yaw, updown, 0, 0
            #print(Powers)
            cv2.waitKey(1)
            #pub.sendMessage("transectline", message = Powers)
            #a = [1, 2, 3, 4, 5, 6]
            #pub_to_manager("control-movement", message = ("transectline", Powers))
            pub.sendMessage("control-movement", message = ("transectline", Powers))
        else:
            if self.captureON == True:
                self.cap.release()
                cv2.destroyAllWindows()
                self.captureON = False
        


#cap.release()
#cv2.destroyAllWindows()
