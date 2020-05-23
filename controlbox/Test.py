'''
from pubsub import pub
from ModuleBase import Module


class Thruster(Module):
    def __init__(self, name, address, invert):
        self.name = name
        self.address = address
        self.invert = invert
        pub.subscribe(self.__listener, name)
        self.target_power = 0
        self.current_power = 0
        self.max_rate = 0.5
        self.output_power = 0
        
    def run(self): #calculate rate, set message and send to bus
        rate = (self.target_power-self.current_power)/(self.interval*10) #power needed/interval
        if (rate>self.max_rate): #Prevent rate too large
            rate = self.max_rate
        elif rate<self.max_rate*-1:
            rate = self.max_rate*-1
        self.current_power = rate+self.current_power
        if self.invert == True: #Deal with invert
            self.current_power = self.current_power *-1
        #Set to range of -32768 to 32767
        if self.current_power>=0:
            self.output_power= int(self.current_power*32767)
        else:
            self.output_power= int(self.current_power*32768)
        pub.sendMessage(str(self.name)+'a', power = self.output_power)
        #print(self.current_power)
            
    def __listener(self, power): #Set target power
        self.target_power = power
        #print(self.target_power)

'''
'''
import pygame
pygame.init()
while True:
    Surface = pygame.Surface((400,300))
    Surface.fill((250, 0, 0))
    surface = pygame.Surface((300, 300))
    surface.fill((0, 250, 0))
    surface2 = pygame.Surface((300, 300))
    surface2.fill((0, 0, 250))
    screen = pygame.display.set_mode((1200, 700))
    Surface.blits(blit_sequence = ((surface, (0,0)),(surface2, (200,200))))
    #Surface.blit(surface2, (200, 200))
    screen.blit(Surface, (0, 0))
    pygame.display.flip()
'''
from pubsub import pub
from ModuleBase import Module
from ModuleLoader import Loader

class CAN_Handler(Module):
    def __init__(self):
        pub.subscribe(self.MessageListener, 'Message')
        
    def MessageListener(self, pub):
        print(pub)

    def run(self):
        pass

if '__main__' == '__name__':
    Loader.loadfrom("Gamepad_Normalize", "Gamepad", "gp", "10000")
    Loader.loadfrom("Thruster_Profile", "FormulaApply", "fa", "100")
    Loader.load_byName("ThrusterFL", 'config.yaml', 10)
    Handler = CAN_Handler()
    Handler.start(100)
