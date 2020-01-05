from pubsub import pub
from Gamepad_Normalize import Gamepad
from threading import Timer
from ModuleBase import Module
import time
#constants
Strafe = (1, -1, 1, -1)
Drive = (-1, -1, 1, 1)
Yaw = (1, -1, -1, 1)

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
    def __init__(self, max_percentage=100, formula_modifier=30, activate = 1):
        pub.subscribe(self.movementListener, 'movement')
        pub.subscribe(self.controlListener, 'controls')
        self.max_percentage = int(max_percentage)/100
        self.formula_modifier = int(formula_modifier)
        self.activate = int(activate)
        self.profile_change = 1
        
    def run(self):
        pass
    
    def movementListener(self,arg1):
        if self.profile_change == self.activate:
            StrafePower, DrivePower, YawPower, Updown = arg1
            StrafePower = PowerFunction(StrafePower, self.formula_modifier) #formula modify increase, curve increase
            DrivePower = PowerFunction(DrivePower, self.formula_modifier)
            YawPower = PowerFunction(YawPower, self.formula_modifier)
            UpdownPower = PowerFunction(Updown, self.formula_modifier)
            FinalList = SetThruster(StrafePower, DrivePower, YawPower)
            pub.sendMessage('ThrusterFL', power = FinalList[0]*self.max_percentage)
            pub.sendMessage('ThrusterFR', power = FinalList[1]*self.max_percentage)
            pub.sendMessage('ThrusterBL', power = FinalList[2]*self.max_percentage)
            pub.sendMessage('ThrusterBR', power = FinalList[3]*self.max_percentage)
            pub.sendMessage('ThrusterUL', power = UpdownPower*self.max_percentage)
            pub.sendMessage('ThrusterUR', power = UpdownPower*self.max_percentage)
        #print(FinalList[0])
        #print(DrivePower)

    def controlListener(self, control):
        self.profile_change = control #1 or -1
'''
if __name__ == '__main__':
    gp =Gamepad()
    gp.start(10000)
    fa = FormulaApply()
    fa.start(10000)  
    #print(SetThruster(0,1,0)==[-1,-1,1,1])
'''
