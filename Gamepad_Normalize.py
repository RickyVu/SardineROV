# constants
DeadZone_ThresholdL = 0.06
DeadZone_ThresholdR = 0.08
Normalize_Constant = 32768

# variables
movement_message = (0, 0, 0, 0)
previous_message = (2, 2, 2, 2)

from threading import Timer
from inputs import get_gamepad
from pubsub import pub
from ModuleBase import Module

def normalize(X):
    if X < 0:
        return (X/Normalize_Constant)
    else:
        return (X/(Normalize_Constant-1))

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
   
    def run(self):
        global previous_message
        global movement_message
        events= get_gamepad()
        for event in events:
            analogcode = event.code[0:6]
            if (analogcode == "ABS_X"):
                self.strafe = deadzoneleft(normalize(event.state))
            elif (analogcode == "ABS_Y"):
                self.drive = deadzoneleft(normalize(event.state))
            elif (analogcode == "ABS_RX"):
                self.yaw = deadzoneright(normalize(event.state))
            elif (analogcode == "ABS_RY"):
                self.updown = deadzoneright(normalize(event.state))
        movement_message = (self.strafe, self.drive, self.yaw, self.updown)
                
        if previous_message != movement_message:
            pub.sendMessage('movement', arg1=movement_message)
            previous_message = movement_message

