from ModuleLoader import Loader
from GUI_Widget import ThrusterWidget
#from CAN_Handler import CAN_Handler  
import pygame


Loader.load_all('config.yaml')
#Handler = CAN_Handler()
#Handler.start(10)
#Loader.load_byName('ThrusterUR', 'config.yaml',10)
#Loader.load_byName("ThrusterFL", 'config.yaml', 10)
'''
FL = Thruster('ThrusterFL', 0x011, False)
FL.start(10)
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

#Timer(1, printinterval, [1]).start()'
TA = ThrusterWidget(15, 'ThrusterFL')
TB = ThrusterWidget(15, 'ThrusterFR')
TC = ThrusterWidget(15, 'ThrusterBL')
TD = ThrusterWidget(15, 'ThrusterBR')
TE = ThrusterWidget(15, 'ThrusterUL')
TF = ThrusterWidget(15, 'ThrusterUR')


pygame.init()
screen = pygame.display.set_mode((300, 250))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    TA.update(screen, (0,0))
    TB.update(screen, (50,0))
    TC.update(screen, (100,0))
    TD.update(screen, (150,0))
    TE.update(screen, (200,0))
    TF.update(screen, (250,0))

    pygame.display.flip()

