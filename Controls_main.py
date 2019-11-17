from threading import Timer
import yaml
from ModuleLoader import Loader
from Gamepad_Normalize import Gamepad #
from Thruster_Profile import FormulaApply #
from Thruster_Message import Thruster #

'''
gp = Gamepad()
gp.start(10000)
fa = FormulaApply()
fa.start(10000)
'''
#Loader.loadfrom("Gamepad_Normalize", "Gamepad", "gp", "10000")
#Loader.loadfrom("Thruster_Profile", "FormulaApply", "fa","10000")
Loader.load_controls(10000, 10000)
Loader.load_all('config.yaml')
#Loader.load_byName("ThrusterFL", 'config.yaml', 10)
#FL = Thruster('ThrusterFL', 0x011, False)
#FL.start(10)
'''
FR = Thruster('ThrusterFR', 0x012, False)
FR.start(10)
BL = Thruster('ThrusterBL', 0x013, False)
BL.start(10)
BR = Thruster('ThrusterBR', 0x014, False)
BR.start(10)
UL = Thruster('ThrusterUL', 0x015, False)
UL.start(10)
UR = Thruster('ThrusterUR', 0x016, False)
UR.start(10)
'''
#def printinterval(i):
    #print(i)
    #Timer(1, printinterval, [i+1]).start()

#Timer(1, printinterval, [1]).start()
