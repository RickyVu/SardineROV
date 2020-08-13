# constants
DeadZone_ThresholdL = 0.08
DeadZone_ThresholdR = 0.1
Normalize_Constant = 32768
Normalize_Constant_Z = 1024
Directional_BTN = {"BTN_NORTH", "BTN_WEST", "BTN_SOUTH", "BTN_EAST"}
#BTN_TL, BTN_TR {0, 1}

ProfileDict = {'ABS_HAT0Y-1': 'A',
               'ABS_HAT0X-1': 'B',
               'ABS_HAT0X1': 'C',
               'ABS_HAT0Y1': 'D',
               'BTN_THUMB0': 'A',
               'BTN_THUMB1': 'B',
               'BTN_THUMB2': 'C',
               'BTN_THUMB3': 'D'}

# variables
previous_message = (2, 2, 2, 2, 2, 2)

from threading import Timer
import time
import threading
from inputs import get_gamepad
from pubsub import pub
from ModuleBase import Module
import copy
from PubManager import pub_to_manager


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

def half_movement_value_join(negative_value, positive_value):
    return negative_value+positive_value

def half_movement_value_split(full_value):
    if full_value>=0:
        return 0, full_value
    else:
        return full_value, 0


class Gamepad(Module):
    def __init__(self):
        #pub.subscribe(self.south_listener, 'transectline')
        pub.subscribe(self.active_listener, 'activate_controller')
        self.drive = 0
        self.strafe = 0
        self.yaw = 0
        self.tilt = 0
        self.updown1 = 0
        self.updown2 = 0
        self.updown = 0
        self.tilt_front = 0
        self.tilt_back = 0
        self.control_invert = False
        self.movement_message = (0,0,0,0,0,0)
        self.active = True #[True, False, False]  #Analog, South, West
        self.show_transectline = False
        self.thumb_profile_cycle = 0
        self.EM_TL = 0
        self.EM_TR = 0
        #self.handler = HTTP_Handler(1234)
        #self.HTTP_thread = threading.Thread(target = self.HTTP_listener)
        #self.http_thread_start = True
        #self.HTTP_thread.start()

    '''
    def south_listener(self, message):
        #print("south_listener", message)
        new_message = message
        if self.control_invert == True:
            for i in range(len(message)):
                if i != 3:
                    message[i] = -1*message[i]
        pub_to_manager("movement", message = new_message)
        #pub.sendMessage('movement', message = new_message)'''

    def active_listener(self, message):
        self.active = message
        self.movement_message = (0, 0, 0, 0, 0, 0)
        pub.sendMessage("control-movement", message = ("controller", (0, 0, 0, 0, 0, 0)))

    '''
    def HTTP_listener(self):
        time.sleep(0.5)
        while True:
            if self.handler.data != None and self.active[2] == True:
                #print("")
                turn_calibration = float(self.handler.get_data()[:4])
                self.movement_message = (0, 0, turn_calibration, 0, 0, 0)
                #print(self.movement_message)
                #pub.sendMessage('movement', arg1=self.movement_message)'''


    def run(self):
        #global previous_message
        #global movement_message
        events= get_gamepad()
        analogcode = None
        for event in events:
            if self.active:
                analogcode = event.code[0:6]
                if (analogcode == "ABS_X"):
                    self.strafe = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_Y"):
                    self.drive = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_RX"):
                    self.yaw = deadzoneright(normalize(event.state))
                elif (analogcode == "ABS_RY"):
                    self.tilt = (deadzoneright(normalize(event.state)))
                    #print(self.tilt)
                if (analogcode == "ABS_Z"):
                    self.updown1 =  (-1)*normalize(event.state, Normalize_Constant_Z)
                if (analogcode == "ABS_RZ"):
                    self.updown2 = normalize(event.state, Normalize_Constant_Z)

                self.updown = half_movement_value_join(self.updown1, self.updown2)


                if self.control_invert == False:#tfront, tback
                    self.movement_message = (self.strafe, self.drive, self.yaw, self.updown, self.tilt, 0)
                else:
                    self.movement_message = (-self.strafe, -self.drive, self.yaw, self.updown, -self.tilt, 0)
                #pub_to_manager('movement', message = self.movement_message)
                pub.sendMessage("control-movement", message = ("controller", self.movement_message))

        hatcode = event.code[0:8]
        controlcode = event.code
        if controlcode == "BTN_THUMBR" and event.state!=0:
            self.thumb_profile_cycle = (self.thumb_profile_cycle+1)%4
            pub.sendMessage("profile", message = ProfileDict[str(event.code[:-1])+str(self.thumb_profile_cycle)])

        if controlcode == "BTN_THUMBL" and event.state!=0:
            self.thumb_profile_cycle = (self.thumb_profile_cycle-1)%4
            pub.sendMessage("profile", message = ProfileDict[str(event.code[:-1])+str(self.thumb_profile_cycle)])

        if controlcode == 'BTN_TL' and event.state != 0:
            self.EM_TL += event.state
            print(self.EM_TL%2)
            pub.sendMessage("EM_TL", message = self.EM_TL%2)

        if controlcode == 'BTN_TR' and event.state != 0:
            self.EM_TR += event.state
            print(self.EM_TR%2)
            pub.sendMessage("EM_TR", message = self.EM_TR%2)

        if (hatcode == "ABS_HAT0") and (event.state != 0):
            #pub_to_manager('profile', message = ProfileDict[str(event.code)+str(event.state)])
            pub.sendMessage("profile", message = ProfileDict[str(event.code)+str(event.state)])

        if (controlcode == "BTN_SOUTH") and (event.state == 1):
            #pub_to_manager('activate_transectline')
            #pub_to_manager('show_transectline')
            pub.sendMessage("movement_activation", sender = "transectline")
            pub.sendMessage("show_transectline", message = not self.show_transectline)

        if (controlcode == "BTN_WEST") and (event.state == 1):
            self.control_invert = not self.control_invert
            pub.sendMessage("control_invert", message = self.control_invert) #For GUI
            #pub_to_manager('control_invert')

            #pub_to_manager('activate_transectline')
            #pub_to_manager('show_transectline')
            #pub.sendMessage("movement_activation", sender = "something")
            #pub.sendMessage("show_transectline", message = not self.show_transectline)


        '''
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
                    self.active[0] = False'''


if __name__ == "__main__":

    Gamepad = Gamepad()
    Gamepad.start(120)
    def controller_listener(message):
        print(message)
    pub.subscribe(controller_listener,"control-movement")
