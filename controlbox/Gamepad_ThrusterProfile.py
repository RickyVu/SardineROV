from pubsub import pub
from Gamepad_Normalize import Gamepad
from threading import Timer

#constants
Functions = ('X**5 - X**3 + X', '(X**5+X)/2')
def PowerFunction(A, B):
    X = A
    return eval(Functions[B])


class Thrusters:
    def __init__(self,Power, TL, TR, BL, BR):
        self.T1 = Power * TL
        self.T2 = Power * TR
        self.T3 = Power * BL
        self.T4 = Power * BR
        self.T_All = (self.T1, self.T2, self.T3, self.T4)

def Combine(X, Y, Z):
    Total = [0, 0, 0, 0]
    for i in range(0, 4):
        Total[i] = PowerFunction(Normalize(X[i], Y[i], Z[i]), 1)
    return tuple(Total)

def Listener1(arg1):
    StrafePower, DrivePower, YawPower, Updown = arg1

    
    def Normalize(X, Y, Z):
        if X == 0 and Y == 0 and Z == 0:
            return 0
        else:
            Magnitude = abs(X) + abs(Y) + abs(Z)
            return (X+Y+Z)/Magnitude

    Strafe = Thrusters(StrafePower, 1, -1, 1, -1)
    Drive = Thrusters(DrivePower, -1, -1, 1, 1)
    Yaw = Thrusters(YawPower, 1, -1, -1, 1)

    FinalTuple = Combine(Strafe.T_All, Drive.T_All, Yaw.T_All)
    print('Final Answer' , FinalTuple)

pub.subscribe(Listener1, 'movement')
gp = Gamepad()
gp.start(10000)
