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
horizontalDist = [0.168,0.176,0] # FR x,y,z unit:m
verticalDist = [0,0.182,0.97] # TF x,y,z unit:m
Scale_Constants = (1.714, 1.714,  0.58, 2, 0.22, 0)# strafe, drive, yaw, updown, tiltFB, tiltLR
Backward_Thrust = 1.65
Thruster_Scale = [3,3,3,3,2.65,2.65]

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

            StrafePower, DrivePower, YawPower, UpdownPower, Tilt_FB, Tilt_LR = message

            print('Gamepad in :', StrafePower, DrivePower, YawPower, UpdownPower, Tilt_FB, 0)

            StrafePower = PowerFunction(StrafePower, self.formula_modifier)
            DrivePower = PowerFunction(DrivePower, self.formula_modifier)
            YawPower = PowerFunction(YawPower, self.formula_modifier)
            UpdownPower = PowerFunction(UpdownPower, self.formula_modifier)
            TIlt_FB = PowerFunction(Tilt_FB, self.formula_modifier)

            print('Power function in :', StrafePower, DrivePower, YawPower, UpdownPower, Tilt_FB, 0)

            StrafePower *= Scale_Constants[0]
            DrivePower *= Scale_Constants[1]
            YawPower *= Scale_Constants[2]
            UpdownPower *= Scale_Constants[3]
            Tilt_FB *= Scale_Constants[4]

            print('Scaled in :', StrafePower, DrivePower, YawPower, UpdownPower, Tilt_FB, 0)


            exResult = np.array((StrafePower, DrivePower, UpdownPower, Tilt_FB, Tilt_LR, YawPower))
            exResult = exResult.reshape(6,1)

            Tinv = np.linalg.pinv(T)
            finalList = Tinv.dot(exResult)

            print('psuedoinv out:' , finalList)

            for counter in range(6):
                #finalList[counter, 0] /= Thruster_Scale[counter]
                if finalList[counter, 0] < 0:
                    finalList[counter, 0] *= Backward_Thrust
            print('Normalize out: ', finalList)

            if max(abs(finalList)) > 1:
                for counter in range(6):
                    finalList[counter, 0] /= max(abs(finalList))

            print('truncate out: ', finalList)
            pub.sendMessage('ThrusterFL', power = finalList[0][0]*self.max_percentage)
            pub.sendMessage('ThrusterFR', power = finalList[1][0]*self.max_percentage)
            pub.sendMessage('ThrusterBL', power = finalList[2][0]*self.max_percentage)
            pub.sendMessage('ThrusterBR', power = finalList[3][0]*self.max_percentage)
            pub.sendMessage('ThrusterUF', power = finalList[4][0]*self.max_percentage)
            pub.sendMessage('ThrusterUB', power = finalList[5][0]*self.max_percentage)

    def profileListener(self, message):
        self.profile_change = message #A, B, C, D

class __Test_Case_Single__(Module):
    """docstring for ."""

    def run(self):
        pub.sendMessage('control-movement', message = (0,1,1,0,0,0))


if __name__ == "__main__":
    ThrusterPower = FormulaApply()
    ThrusterPower.start(1)
    __Test_Case_Single__ = __Test_Case_Single__()
    __Test_Case_Single__.start(1)
