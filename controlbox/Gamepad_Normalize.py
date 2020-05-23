# constants
DeadZone_ThresholdL = 0.08
DeadZone_ThresholdR = 0.1
Normalize_Constant = 32768
Normalize_Constant_Z = 256
Directional_BTN = {"BTN_NORTH", "BTN_WEST", "BTN_SOUTH", "BTN_EAST"}

ProfileDict = {'ABS_HAT0Y-1': 'A',
               'ABS_HAT0X-1': 'B',
               'ABS_HAT0X1': 'C',
               'ABS_HAT0Y1': 'D'}

# variables
previous_message = (2, 2, 2, 2, 2, 2)

from threading import Timer
import time
import threading
from inputs import get_gamepad
from pubsub import pub
from ModuleBase import Module
from HTTP_Connectors import HTTP_Handler

def normalize(X, constant = Normalize_Constant):
    if X < 0:
        return (X/constant)
    else:
        return (X/(constant-1))

def deadzoneleft(X):
    if X <(DeadZone_ThresholdL) and X > (-DeadZone_ThresholdL):
        return 0
    else:
        return X
def deadzoneright(X):
    if X <(DeadZone_ThresholdR) and X > (-DeadZone_ThresholdR):
        return 0
    else:
        return X

class Gamepad(Module):
    def __init__(self):
        pub.subscribe(self.__south_listener, 'TransectLine')
        self.drive = 0
        self.strafe = 0
        self.yaw = 0
        self.updown = 0
        self.tilt_front = 0
        self.tilt_back = 0
        self.control_invert = False
        self.movement_message = (0,0,0,0,0,0)
        self.profile_change = 'A'
        self.active = [True, False, False]  #Analog, South, West
        self.handler = HTTP_Handler(1234)
        self.HTTP_thread = threading.Thread(target = self.HTTP_listener)
        self.http_thread_start = True
        self.HTTP_thread.start()

    def __south_listener(self, Message):
        if self.active[1] == True:          
            if self.control_invert == True:
                for i in range(len(Message)):
                    if i != 3:
                        Message[i] = -1*Message[i]
            movement_message = Message
            pub.sendMessage('movement', arg1=movement_message)
            #print(self.movement_message)

    def HTTP_listener(self):
        time.sleep(0.5)
        while True:
            if self.handler.data != None and self.active[2] == True:
                #print("")
                turn_calibration = float(self.handler.get_data()[:4])
                self.movement_message = (0, 0, turn_calibration, 0, 0, 0)
                #print(self.movement_message)
                #pub.sendMessage('movement', arg1=self.movement_message)
            
   
    def run(self):
        #global previous_message
        #global movement_message
        events= get_gamepad()
        analogcode = None
        for event in events:
            if self.active[0]:
                analogcode = event.code[0:6]
                if (analogcode == "ABS_X"):
                    self.strafe = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_Y"):
                    self.drive = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_RX"):
                    self.yaw = deadzoneright(normalize(event.state))
                elif (analogcode == "ABS_RY"):
                    self.updown = deadzoneright(normalize(event.state))             
                elif (analogcode == "ABS_Z"):
                    self.tilt_back = (-1)*normalize(event.state, Normalize_Constant_Z)
                elif (analogcode == "ABS_RZ"):
                    self.tilt_front = normalize(event.state, Normalize_Constant_Z)

                if self.control_invert == False:
                    self.movement_message = (self.strafe, self.drive, self.yaw, self.updown, self.tilt_front, self.tilt_back)
                else:
                    self.movement_message = (-self.strafe, -self.drive, -self.yaw, self.updown, -self.tilt_front, -self.tilt_back)
                pub.sendMessage('movement', arg1=self.movement_message)

            hatcode = event.code[0:8]
            controlcode = event.code

            if controlcode == 'BTN_TL' and event.state != 0:
                self.control_invert = not self.control_invert
            
            if (hatcode == "ABS_HAT0") and (event.state != 0):
                self.profile_change = ProfileDict[str(event.code)+str(event.state)]

            if (controlcode == "BTN_SOUTH") and (event.state == 1):
                self.active[1] = not self.active[1]

            if (controlcode== "BTN_WEST") and (event.state ==1):
                self.active[2] = not self.active[2]
                if self.active[2] == True:
                    self.handler.send_continue()
                else:
                    self.handler.send_stop()
                    #self.handler.disconnect()                

            if (controlcode in Directional_BTN) and (event.state == 1):
                if self.active[0] == False:
                    self.active[0] = True
                    for i in range(1, len(self.active)):
                        self.active[i] = False
                else:
                     self.active[0] = False

                    
            pub.sendMessage('profile', profile = self.profile_change)
            pub.sendMessage('show_transectline', show_transectline = self.active[1])       
            pub.sendMessage('control_invert', control_inverted = self.control_invert)
