from pubsub import pub
from ModuleBase import Module
from threading import Timer
import Gamepad_ThrusterOrder as ThrusterOrder
#from Gamepad_Normalize import Gamepad

class Loader():
    def load(frequency, name, module, varclass, address, invert=False):
        exec('import '+module+' as '+varclass) 

        if invert == False:
            exec(name+'='+varclass+'.'+varclass+'("'+name+'",'+address+')')
        else:
            exec(name+'='+varclass+'.'+varclass+'("'+name+'",'+address+','+invert+')')
        if frequency != 0:
            exec(str(name) + ".start(" + str(frequency) + ")")
        else:
            exec(str(name) + ".start")

    def loadfrom(file, module, name, frequency):
        exec("from " + str(file) + " import " + str(module))
        exec(str(name) + " = " + str(module) + "()")
        exec(str(name) + ".start(" + str(frequency) + ")")
    
#import Gamepad_ThrusterOrder as ThrusterOrder
#ThrusterFL = ThrusterOrder.Thruster("ThrusterFL", 0x00, True)
#ThrusterFL.start(1000)






#Loader.load(10000, 'ThrusterFL', 'Gamepad_ThrusterOrder', 'Thruster', '0x01', 'True')
#Loader.load(0, 'ThrusterFR', 'Gamepad_ThrusterOrder', 'Thruster', '0x02', 'False')

#t = ThrusterOrder.Thruster("ThrusterName", address=0x01, invert=False)

#Loader.loadfrom("Gamepad_Normalize", "Gamepad", "gp", "10000")
#Loader.load("Gamepad", "gp", "10000")
'''
def Listener(arg1):
    print(arg1)
pub.subscribe(Listener, 'movement')
'''

#Loader.thrusterload("ThrusterFL", "0x00", "10") 
#Loader.thrusterload("ThrusterFR", "0x01", "10")
