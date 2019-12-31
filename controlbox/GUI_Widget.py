import pygame
import math
from pubsub import pub
from ModuleLoader import Loader
from Thruster_Message import Thruster
#Loader.load_all('config.yaml')
'''
class Widget:
    def __init__(self, screenwidth, screenheight):
        self.screenwidth = width
        self.screenheight = height
        self.screen = pygame.display.set_mode((width, height))
    def getdimension():
        pass
    def update():
        return self.screen

class NodeWidget(Widget):
    def __init__(self, nodewidth, nodeheight):
        screenwidth = nodewidth*3
        screenheight = nodeheight *2
        self.nodesurface = pygame.Surface((nodewidth,nodeheight))
        self.surfaces = []
        super().__init__(screenwidth, screenheight)


    def assemble(self, nodesurface, surface):
        #find the size
        for surface in self.surfaces:
            self.nodesurface.blit(surface, (x, y))
        super().screen.blit(nodesurface,(0,0))
'''
'''
List = []

class Widget:
    def __init__(self, screenwidth, screenheight, surface):
        self.width = screenwidth
        self.height = screenheight
        self.Surface = surface

    def screen_setup(self):
        self.screen = pygame.Surface((self.width,self.height))
        self.screen.fill((0, 0, 0))
        
    def getdimension(self):
        pass
    
    def update(self):
        self.screen.blit(self.Surface, (10, 10))
        return self.screen

class NodeWidget():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodesurface = pygame.Surface((self.width,self.height))

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
                
    def nodereturn(self):
        return nodesurface
    
class ThrusterWidget():
    def __init__(self, power, r, theta1, theta2):
        self.GREY =(30, 30, 30)
        self.GREEN = (57, 255, 20)
        self.Surface = pygame.Surface((400,300))
        self.Surface.fill((0, 0, 0))
        self.r = r
        self.theta1 = theta1
        self.theta2 = theta2
        self.power = 0
        

    def draw_gauge(self):
        pygame.draw.circle(self.Surface, self.GREY, (195, 150), 100)
        pygame.draw.circle(self.Surface, self.GREEN, (195, 150), 5)
        pygame.draw.line(self.Surface, self.GREEN, (195, 150), (self.r*1.2*math.cos(self.theta1-math.pi/2)+195,self.r*1.2*math.sin(self.theta1-math.pi/2)+150),5)
        pygame.draw.line(self.Surface, self.GREEN, (195, 150), (self.r*1.2*math.cos(self.theta2-math.pi/2)+195,self.r*1.2*math.sin(self.theta2-math.pi/2)+150),5)
        if self.power>0:
            theta = (self.power/32767)*(3*math.pi)/4
        else:
            theta = (self.power/32768)*(3*math.pi)/4
        theta0 = theta+ 3*math.pi/4
        GradualColour = (theta0*255)/(6*math.pi/4)
        pygame.draw.line(self.Surface, (GradualColour, 0, 255-GradualColour), (195, 150), (self.r*math.cos(theta-math.pi/2)+195,self.r*math.sin(theta-math.pi/2)+150),3)
        List = List + [self.Surface, 400, 300]
'''
class Widget:
    def __init__(self):
        self.Surface = pygame.Surface(self.getDimension())
        
    def getDimension(self):
        return (50,50)

    def surface_return(self):
        self.draw(self.Surface)
        return self.Surface

    def update(self, screen, coordinate):
        screen.blit(self.surface_return(), coordinate)
        screen.blit(self.text_Surface, (coordinate[0],coordinate[1]+50))
        
    def draw(self, surface):
        pass

class NodeWidget(Widget):
    def __init__(self):
        super().__init__()
        
    def draw(self, surface):
        super().draw(surface)

class ThrusterWidget(NodeWidget):
    def __init__(self, r, name, theta1 = -3*math.pi/4, theta2 = 3*math.pi/4):
        super().__init__()
        
        self.GREY =(30, 30, 30)
        self.GREEN = (57, 255, 20)
        self.Surface.fill((0, 0, 0))
        self.r = r
        self.theta1 = theta1
        self.theta2 = theta2
        self.power = 0
        self.dim = self.getDimension()
        self.center = (round(self.dim[0]/2), round(self.dim[1]/2))
        
        pub.subscribe(self._power_listener, name+'_Widget')
        
    def draw(self, surface):
        super().draw(surface)
        self._draw_gauge(surface, self.power)
        self._thrust_percentage()

    def _power_listener(self, output):
        self.power = output
        #print(self.power)
        
    def _draw_gauge(self, surface, power):
        pygame.draw.circle(surface, self.GREY, self.center, round(self.r*1.2))
        pygame.draw.circle(surface, self.GREEN, self.center,round(self.r*0.3))
        pygame.draw.line(surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta1-math.pi/2)+self.dim[0]/2, self.r*1.2*math.sin(self.theta1-math.pi/2)+self.dim[1]/2), 5)
        pygame.draw.line(surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta2-math.pi/2)+self.dim[0]/2, self.r*1.2*math.sin(self.theta2-math.pi/2)+self.dim[1]/2), 5)
        #Arrow
        ##Gradual color change
        if self.power>0:
            theta = (self.power/32767)*(3*math.pi)/4
        else:
            theta = (self.power/32768)*(3*math.pi)/4
        theta0 = theta+ 3*math.pi/4
        GradualColour = (theta0*255)/(6*math.pi/4)
        BLUE_TO_RED = (GradualColour, 0, 255-GradualColour)
        ##Draw arrow
        pygame.draw.line(surface, BLUE_TO_RED, (self.center), (self.r*math.cos(theta-math.pi/2)+self.dim[0]/2, self.r*math.sin(theta-math.pi/2)+self.dim[1]/2), 5)

    def _thrust_percentage(self):
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 20)
        if self.power>0:
            self.text_Surface = self.myfont.render(str("{:.1f}".format(self.power*100/32767))+'%', True, (200, 200, 200))
        else:
            self.text_Surface = self.myfont.render(str("{:.1f}".format(self.power*100/32768))+'%', True, (200, 200, 200))
            
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


