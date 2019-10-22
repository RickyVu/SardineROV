from pubsub import pub
from Gamepad_Normalize import Gamepad
from Gamepad_ThrusterProfile2 import FormulaApply
from Gamepad_ThrusterOrder import Thruster
from threading import Timer

gp = Gamepad()
gp.start(10000)
fa = FormulaApply()
fa.start(10000)


FL = Thruster('ThrusterFL', 0x011, False)
FL.start(10)
FR = Thruster('ThrusterFR', 0x012, False)
FR.start(10)
BL = Thruster('ThrusterBL', 0x013, False)
BL.start(10)
BR = Thruster('ThrusterBR', 0x014, False)
BR.start(10)

#def printinterval(i):
    #print(i)
    #Timer(1, printinterval, [i+1]).start()

#Timer(1, printinterval, [1]).start()
