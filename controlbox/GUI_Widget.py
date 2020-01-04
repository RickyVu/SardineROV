import pygame
import math
from pubsub import pub
from ModuleLoader import Loader
from Thruster_Message import Thruster

class Widget:
    def __init__(self):
        self.Surface_Dimension = (100, 50)
        self.Surface = pygame.Surface(self.Surface_Dimension)
        
    def getDimension(self):
        return (100, 150)

    def surface_return(self):
        self.draw(self.Surface)
        return self.Surface

    def update(self):
        self.Surface.fill((0, 0, 0))
        self.draw(self.Surface)
        Surface_Screen_x, Surface_Screen_y = self.getDimension()
        Surface_Screen = pygame.Surface(self.getDimension())
        Surface_Screen.fill((0, 0, 0))
        Surface_Screen.blit(self.Surface, (0, Surface_Screen_y/3))
        Surface_Screen.blit(self.text_Surface1, (0, Surface_Screen_y*2/3))
        Surface_Screen.blit(self.text_Surface2, (0, 0))
        return Surface_Screen
                
    def draw(self, surface):
        pass

class NodeWidget(Widget):
    def __init__(self):
        super().__init__()
        
    def draw(self, surface):
        super().draw(surface)

class ThrusterWidget(NodeWidget):
    def __init__(self, name):
        super().__init__()
        
        self.GREY =(30, 30, 30)
        self.GREEN = (57, 255, 20)
        self.name = name
        self.r = self.Surface_Dimension[0]//6 #Screen width / number of thrusters
        self.theta1 = -3*math.pi/4
        self.theta2 = 3*math.pi/4
        self.power = 0
        self.dim = self.Surface_Dimension
        self.center = (self.dim[0]//2, self.dim[1]//2)
        self.font_size1 = 12
        self.font_size2 = 12
        
        pub.subscribe(self._power_listener, name)
        
    def draw(self, surface):
        super().draw(surface)
        self._draw_gauge(surface, self.power)
        self._thrust_percentage()
        self._thruster_name()

    def _power_listener(self, power):
        self.power = power
        #print(self.power)
        
    def _draw_gauge(self, surface, power):
        pygame.draw.circle(surface, self.GREY, self.center, round(self.r*1))
        pygame.draw.circle(surface, self.GREEN, self.center,round(self.r*0.3))
        pygame.draw.line(surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta1-math.pi/2)+self.dim[0]/2, self.r*1.2*math.sin(self.theta1-math.pi/2)+self.dim[1]/2), 5)
        pygame.draw.line(surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta2-math.pi/2)+self.dim[0]/2, self.r*1.2*math.sin(self.theta2-math.pi/2)+self.dim[1]/2), 5)
        #Arrow
        ##Gradual color change
        if self.power>0:
            theta = (self.power)*self.theta2
        else:
            theta = (self.power)*-1*self.theta1
        theta0 = theta+ 3*math.pi/4
        GradualColour = (theta0*255)/(6*math.pi/4)
        BLUE_TO_RED = (GradualColour, 0, 255-GradualColour)
        ##Draw arrow
        pygame.draw.line(surface, BLUE_TO_RED, (self.center), (self.r*math.cos(theta-math.pi/2)+self.dim[0]/2, self.r*math.sin(theta-math.pi/2)+self.dim[1]/2), 5)

    def _thrust_percentage(self):
        
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size1)
        if self.power>0:
            text = self.myfont.render(str("{:.1f}".format(self.power*100))+'%', True, (200, 200, 200))
        else:
            text = self.myfont.render(str("{:.1f}".format(self.power*100))+'%', True, (200, 200, 200))
        text_x, text_y = text.get_width()//2, text.get_height()//2
        self.text_Surface1 = pygame.Surface(self.Surface_Dimension)
        #self.text_Surface1.fill((100, 100, 23))
        self.text_Surface1.blit(text, (self.Surface_Dimension[0]//2-text_x, self.Surface_Dimension[1]//2-text_y))
        
    def _thruster_name(self):
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size2)
        text = self.myfont.render(str(self.name), True, (200, 200, 200))
        text_x, text_y = text.get_width()//2, text.get_height()//2
        self.text_Surface2 = pygame.Surface(self.Surface_Dimension)
        #self.text_Surface2.fill((100, 100, 23))
        self.text_Surface2.blit(text, (self.Surface_Dimension[0]//2-text_x, self.Surface_Dimension[1]//2-text_y))
'''
def assemble(self, List):
    x = 0
    y = 0
    y_2 = 0
    y_3 = 0
    for surface in List:
        if surface[1]>=self.width:
            if x == 0 and y == 0:
                print('Not enough horizontal space')
            x=0
            y=y_3
            if y > self.height:
                print('Not enough vertical space')
        self.nodesurface.blit(surface[0], (x, y))
        x = x+surface[1]
        y_2 =surface[2]
        if y_2>y_3:
            y_3 = y_2
'''                
if __name__ == '__main__':
    '''
    TW = ThrusterWidget(15, 'ThrusterFL')
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))
    while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            quit()
            screen.blit(TW.update(),(0,0))

            #print(TW.update())

            pygame.display.flip()
    '''
    print(pygame.font.get_fonts())


