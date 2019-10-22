from pubsub import pub
from Gamepad_Normalize import Gamepad
from threading import Timer
from ModuleBase import Module
#constants
Strafe = (1, -1, 1, -1)
Drive = (-1, -1, 1, 1)
Yaw = (1, -1, -1, 1)
Functions = ('X**5 - X**3 + X', '(X**5+X)/2', '(X**5 + X**3 +X)/3', '1/30*((31**X)-1) if X>=0 else -1/30*((31**(-1*X))-1)','X')
'''
def PowerFunction(A, B):
    X = A
    return eval(Functions[B])
'''

def PowerFunction(A, B):
    X = A
    if X >=0:
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
        
    def run(self):
        pass
    
    def movementListener(self,arg1):
        StrafePower, DrivePower, YawPower, Updown = arg1
        StrafePower = PowerFunction(StrafePower, 30)
        DrivePower = PowerFunction(DrivePower, 30)
        YawPower = PowerFunction(YawPower, 30)
        FinalList = SetThruster(StrafePower, DrivePower, YawPower)
        #print(FinalList)
        #print(DrivePower)
        pub.sendMessage('ThrusterFL', power = FinalList[0])
        pub.sendMessage('ThrusterFR', power = FinalList[1])
        pub.sendMessage('ThrusterBL', power = FinalList[2])
        pub.sendMessage('ThrusterBR', power = FinalList[3])
        
'''
if __name__ == '__main__':
    gp = Gamepad()
    gp.start(10000)  
    #print(SetThruster(0,1,0)==[-1,-1,1,1])
'''
'''
if __name__ == '__main__':
    print('test')
    Gamepad().start(10000)
    FormulaApply().start(1)
'''


'''
import Gamepad_ThrusterOrder as ThrusterOrder
ThrusterFL = ThrusterOrder.Thruster("ThrusterFL", 0x00, False)
ThrusterFR = ThrusterOrder.Thruster("ThrusterFR", 0x01, False)

ThrusterFL.start(10)
ThrusterFR.start(10)
'''
