from pubsub import pub
from Gamepad_Normalize import Gamepad
from threading import Timer
from ModuleBase import Module
import time
import numpy as np
import math

#constants
sin = math.sin(math.radians(45))
CG = np.array((0, 0, 0))
horizontalDist = [sin,sin,0] # FR x,y,z unit:m
verticalDist = [0,1,1] # TF x,y,z unit:m

FLposition = np.array((-horizontalDist[0], horizontalDist[1], horizontalDist[2]))
FRposition = np.array((horizontalDist[0], horizontalDist[1], horizontalDist[2])) # position x,y,z
BLposition = np.array((-horizontalDist[0], -horizontalDist[1], horizontalDist[2]))
BRposition = np.array((horizontalDist[0], -horizontalDist[1], horizontalDist[2]))
TFposition = np.array((verticalDist[0], verticalDist[1], verticalDist[2]))
TBposition = np.array((verticalDist[0], -verticalDist[1], verticalDist[2]))

FLthrust = np.array((sin, sin, 0))
FRthrust = np.array((-sin, sin, 0)) # thrust direction
BLthrust = np.array((sin, -sin, 0))
BRthrust = np.array((-sin, -sin, 0))
TFthrust = np.array((0, 0, 1))
TBthrust = np.array((0, 0, 1))

def PowerFunction(A, B):
    if A >=0:
        return 1/B*(((B+1)**A)-1)
    else:
        return -1/B*(((B+1)**-A)-1)

def thrusterPreset(absPosition, thrustDirect):
    position = np.subtract(absPosition, CG)
    torque = np.cross(position, thrustDirect)
    return np.concatenate((thrustDirect, torque)).reshape(6,1)

FL = thrusterPreset(FLposition, FLthrust)
FR = thrusterPreset(FRposition, FRthrust)
BL = thrusterPreset(BLposition, BLthrust)
BR = thrusterPreset(BRposition, BRthrust)
TF = thrusterPreset(TFposition, TFthrust)
TB = thrusterPreset(TBposition, TBthrust)

thruster = [FL, FR, BL, BR, TF, TB]
T = np.concatenate((thruster), axis=1)

class FormulaApply(Module):
    def __init__ (self, max_percentage = 100, formula_modifier = 30, activate = 'A'):
        pub.subscribe(self.movementListener, 'control-movement')
        pub.subscribe(self.profileListener, 'profile')
        self.max_percentage = int(max_percentage)/100
        self.formula_modifier = float(formula_modifier)
        self.activate = activate
        self.profile_change = 'A'

    def run(self):
        pass

    def movementListener(self,message):
        if self.profile_change == self.activate:

            StrafePower, DrivePower, YawPower, Updown, Tilt_F, Tilt_B = message[1]
            #print(message[1])
            StrafePower = PowerFunction(StrafePower, self.formula_modifier)
            DrivePower = PowerFunction(DrivePower, self.formula_modifier)
            YawPower = PowerFunction(YawPower, self.formula_modifier)
            UpdownPower = PowerFunction(Updown, self.formula_modifier)
            Tilt_FB = Tilt_F + Tilt_B
            Tilt_FB = PowerFunction(Tilt_FB, self.formula_modifier)
            Tilt_LR = 0

            exResult = np.array((StrafePower, DrivePower, UpdownPower, Tilt_FB, Tilt_LR, YawPower))
            exResult = exResult.reshape(6,1)

            Tinv = np.linalg.pinv(T)
            finalList = Tinv.dot(exResult)
            #print(finalList)

            pub.sendMessage('ThrusterFL', power = finalList[0]*self.max_percentage)
            pub.sendMessage('ThrusterFR', power = finalList[1]*self.max_percentage)
            pub.sendMessage('ThrusterBL', power = finalList[2]*self.max_percentage)
            pub.sendMessage('ThrusterBR', power = finalList[3]*self.max_percentage)
            pub.sendMessage('ThrusterTF', power = finalList[4]*self.max_percentage)
            pub.sendMessage('ThrusterTB', power = finalList[5]*self.max_percentage)

    def profileListener(self, message):
        self.profile_change = message #A, B, C, D
