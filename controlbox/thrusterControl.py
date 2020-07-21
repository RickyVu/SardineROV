
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
TLposition = np.array((verticalDist[0], verticalDist[1], verticalDist[2]))
TRposition = np.array((-verticalDist[0], verticalDist[1], verticalDist[2]))

FLthrust = np.array((sin, sin, 0))
FRthrust = np.array((-sin, sin, 0)) # thrust direction
BLthrust = np.array((sin, -sin, 0))
BRthrust = np.array((-sin, -sin, 0))
TLthrust = np.array((0, 0, 1))
TRthrust = np.array((0, 0, 1))

def thrusterPreset(absPosition, thrustDirect):
    position = np.subtract(absPosition, CG)
    torque = np.cross(position, thrustDirect)
    return np.concatenate((thrustDirect, torque)).reshape(6,1)


def movementListener(self):

    FL = thrusterPreset(FLposition, FLthrust)
    FR = thrusterPreset(FRposition, FRthrust)
    BL = thrusterPreset(BLposition, BLthrust)
    BR = thrusterPreset(BRposition, BRthrust)
    TL = thrusterPreset(TLposition, TLthrust)
    TR = thrusterPreset(TRposition, TRthrust)

    thruster = [FL, FR, BL, BR, TL, TR]

    T = np.concatenate((thruster), axis=1)

    Tinv = np.linalg.pinv(T)
    output = Tinv.dot(exResult)
    return output

exResult = np.array((0,0,0,0,1,0)).reshape(6,1) #strafe, drive, updown, tiltFR, tiltLR, yaw
print(movementListener(exResult))
