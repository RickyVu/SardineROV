# constants
DeadZone_ThresholdL = 0.06
DeadZone_ThresholdR = 0.08
Normalize_Constant = 32768
Normalize_Constant_Z = 256

ProfileDict = {'ABS_HAT0Y-1': 'A',
               'ABS_HAT0X-1': 'B',
               'ABS_HAT0X1': 'C',
               'ABS_HAT0Y1': 'D'}

# variables
movement_message = (0, 0, 0, 0, 0, 0)
previous_message = (2, 2, 2, 2, 2, 2)

from threading import Timer
from inputs import get_gamepad
from pubsub import pub
from ModuleBase import Module

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
        self.drive = 0
        self.strafe = 0
        self.yaw = 0
        self.updown = 0
        self.tilt_front = 0
        self.tilt_back = 0
        self.profile_change = 'A'
   
    def run(self):
        global previous_message
        global movement_message
        events= get_gamepad()
        for event in events:
            analogcode = event.code[0:6]
            hatcode = event.code[:8]
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

            elif (hatcode == "ABS_HAT0") and (event.state != 0):
                self.profile_change = ProfileDict[str(event.code)+str(event.state)]

        movement_message = (self.strafe, self.drive, self.yaw, self.updown, self.tilt_front, self.tilt_back)
        pub.sendMessage('controls', control = self.profile_change)
                
        if previous_message != movement_message:
            pub.sendMessage('movement', arg1=movement_message)
            previous_message = movement_message

