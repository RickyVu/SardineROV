from pubsub import pub
from Gamepad_Normalize import Gamepad
from threading import Timer
from ModuleBase import Module
import time
#constants
Strafe = (1, -1, 1, -1)
Drive = (-1, -1, 1, 1)
Yaw = (-1, 1, 1, -1)

def PowerFunction(A, B):
    if A >=0:
        return 1/B*(((B+1)**A)-1) 
    else:
        return -1/B*(((B+1)**-A)-1) 
        

def Normalize(X, Y, Z):
    Magnitude = abs(X) + abs(Y) + abs(Z)
    if Magnitude == 0:
        return 0
    elif Magnitude >= 1:
        return (X+Y+Z)/Magnitude
    else:
        return X + Y + Z

def SetThruster(S, D, Y):
    List = [0, 0, 0, 0]
    for i in range(0, 4):
        a = Normalize(Strafe[i]*S, Drive[i]*D, Yaw[i]*Y)
        List[i] = a
    return List

class FormulaApply(Module):
    def __init__(self):
        pub.subscribe(self.movementListener, 'movement')
        self.max_limit = 1
        
    def run(self):
        pass
    
    def movementListener(self,arg1):
        StrafePower, DrivePower, YawPower, Updown = arg1
        StrafePower = PowerFunction(StrafePower, 30)
        DrivePower = PowerFunction(DrivePower, 30)
        YawPower = PowerFunction(YawPower, 30)
        UpdownPower = PowerFunction(Updown, 30)
        FinalList = SetThruster(StrafePower, DrivePower, YawPower)
        pub.sendMessage('ThrusterFL', power = FinalList[0]*self.max_limit)
        pub.sendMessage('ThrusterFR', power = FinalList[1]*self.max_limit)
        pub.sendMessage('ThrusterBL', power = FinalList[2]*self.max_limit)
        pub.sendMessage('ThrusterBR', power = FinalList[3]*self.max_limit)
        pub.sendMessage('ThrusterUL', power = UpdownPower*self.max_limit)
        pub.sendMessage('ThrusterUR', power = UpdownPower*self.max_limit)
        #print(FinalList[0])
        #print(DrivePower)
'''
if __name__ == '__main__':
    gp =Gamepad()
    gp.start(10000)
    fa = FormulaApply()
    fa.start(10000)  
    #print(SetThruster(0,1,0)==[-1,-1,1,1])
'''
