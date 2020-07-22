import pygame
import math
from pubsub import pub
from ModuleBase import Module
from Thruster_Message import Thruster

class Widget:
    def __init__(self, size, assemble_dict= None):
        self.Surface_Dimension = size
        self.Surface = pygame.Surface(self.Surface_Dimension)
        if assemble_dict == None:
            self.assemble_dict = {}
        else:
            self.assemble_dict = assemble_dict
        self.font_size = 12
        self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size)
        self.WHITE = (255, 255, 255)
        self.GREY =(30, 30, 30)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 226, 242)
        
    @property    
    def dimension(self):
        return self.Surface_Dimension
    @property
    def width(self):
        return self.Surface_Dimension[0]
    @property
    def height(self):
        return self.Surface_Dimension[1]

    #WORK IN PROGRESS
    def __add__(self, arg: 'Widget Object'): #Created widget with size and coordinates
        assemble_dict = {}
        self.update()
        arg.update()
        tallest = 0
        if arg.height > self.height:
            tallest = arg.height
        else:
            tallest = self.height
        
        for tuples, location in self.assemble_dict.items():
            assemble_dict[tuples] = location
        for tuples, location in arg.assemble_dict.items():
            assemble_dict[tuples] = (self.width, 0)
        return Widget((self.width+arg.width, tallest), assemble_dict)
    
    def _assemble(self, instruct_tuple):
        widest, height = 0, 0
        num_items = 0
        for instance in instruct_tuple:
            num_items += 1
            height += instance.get_height()
            if widest < instance.get_width():
                widest = instance.get_width()
        _Surface = pygame.Surface((widest, height))
        y= 0
        for instance in instruct_tuple:
            _Surface.blit(instance, (0, y))
            y+= instance.get_height()#/num_items#self.height//num_items
        return _Surface

    def _draw(self, instruct_dict):
        for subbox, subbox_loc in instruct_dict.items():
            self.Surface.blit(self._assemble(subbox), subbox_loc)

    def update(self):
        self._draw(self.assemble_dict)
        #print(self.assemble_dict)
        return self.Surface

    def font_render(self, dimension, string, args:'range_and_render_info'): #Input format: self.dimension,string, args = [((num1, num2),(True,COLOUR, None)),((20, None),(True, self.GREEN, None))])  
        _Surface = pygame.Surface(dimension)
        x = 0
        y = 0
        for Range, Render in args:
            _Text = self.myfont.render(string[Range[0]:Range[1]], Render[0], Render[1], Render[2])
            _Surface.blit(_Text, (x, y))
            x = x + _Text.get_width()
        return _Surface

    def text_mid_align(self,text_Surface,text): #return text surface
        text_x, text_y = text.get_width()//2, text.get_height()//2
        text_Surface.blit(text, (text_Surface.get_width()//2-text_x, text_Surface.get_height()//2-text_y))
        return text_Surface



        
class StatusWidget(Widget):
    def __init__(self, size):
        super().__init__(size)
        self.ctrl_inv_Surface_dim = (self.width, self.height/3)
        self.ctrl_inv_Surface = pygame.Surface(self.ctrl_inv_Surface_dim)
        self.control_invert = str(False)
        
        self.profile_Surface_dim = (self.width, self.height/3)
        self.profile_Surface = pygame.Surface(self.profile_Surface_dim)
        self.profile = 'A'
        
        self.transect_line_Surface_dim = (self.width, self.height/3)
        self.transect_line_Surface = pygame.Surface(self.transect_line_Surface_dim)
        self.show_transectline = str(False)
        
        self.font_size = 12
        pub.subscribe(self._control_listener, 'control_invert')
        pub.subscribe(self._profile_listener, 'profile')
        pub.subscribe(self._transect_listener, 'activate_transectline')

    def _control_listener(self, message):
        self.control_invert = str(message)

    def _profile_listener(self, message):
        self.profile = str(message)

    def _transect_listener(self, message):
        self.show_transectline= str(message)
        
    def _control_invert(self):
        self.ctrl_inv_Surface.fill((0,0,0))
        #self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size)
        if self.control_invert ==  'True':
            #text = self.myfont.render(f'Front/Back Inverted: {self.control_invert}', True, self.GREEN)
            text = self.font_render(self.dimension,f'Front/Back Inverted: {self.control_invert}', args = [((0, 20),(True,self.WHITE, None)),((20, None),(True, self.GREEN, None))])                                                                                
        else:
            text = self.font_render(self.dimension,f'Front/Back Inverted: {self.control_invert}', args = [((0, 20),(True,self.WHITE, None)),((20, None),(True, self.RED, None))])
        self.ctrl_inv_Surface.blit(text, (0,0))
        return self.ctrl_inv_Surface

    def _profile(self):
        self.profile_Surface.fill((0, 0, 0))
        if self.profile == 'A':
            text = self.font_render(self.dimension,f'Activated Profile: {self.profile}', args = [((0, 18),(True,self.WHITE, None)),((18, None),(True, self.YELLOW, None))])
        elif self.profile == 'B':
            text = self.font_render(self.dimension,f'Activated Profile: {self.profile}', args = [((0, 18),(True,self.WHITE, None)),((18, None),(True, self.BLUE, None))])
        elif self.profile == 'C':
            text = self.font_render(self.dimension,f'Activated Profile: {self.profile}', args = [((0, 18),(True,self.WHITE, None)),((18, None),(True, self.RED, None))])
        elif self.profile == 'D':
            text = self.font_render(self.dimension,f'Activated Profile: {self.profile}', args = [((0, 18),(True,self.WHITE, None)),((18, None),(True, self.GREEN, None))])
        self.profile_Surface.blit(text, (0,0))
        return self.profile_Surface

    def _transect_line(self):
        self.transect_line_Surface.fill((0,0,0))
        #self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size)
        if self.show_transectline ==  'True':
            #text = self.myfont.render(f'Front/Back Inverted: {self.control_invert}', True, self.GREEN)
            text = self.font_render(self.dimension,f'Activated Transect Line: {self.show_transectline}', args = [((0, 25),(True,self.WHITE, None)),((25, None),(True, self.GREEN, None))])                                                                                
        else:
            text = self.font_render(self.dimension,f'Activated Transect Line: {self.show_transectline}', args = [((0, 25),(True,self.WHITE, None)),((25, None),(True, self.RED, None))])
        self.transect_line_Surface.blit(text, (0,0))
        return self.transect_line_Surface


    def update(self):
        self.assemble_tuple = (self._profile(),self._control_invert(), self._transect_line())
        self.assemble_dict[self.assemble_tuple] = (0, 0)
        self._draw(self.assemble_dict)
        return self.Surface                                                                                                                                                                                                                                                 







class ThrusterWidget(Widget):
    def __init__(self, size, thruster_name):
        super().__init__(size)
        self.gauge_Surface_dim = (self.width, self.height/2)
        self.gauge_Surface = pygame.Surface(self.gauge_Surface_dim)
        self.percentage_Surface_dim = (self.width, self.height/4)
        self.percentage_Surface = pygame.Surface(self.percentage_Surface_dim)
        self.name_Surface_dim = (self.width, self.height/4)
        self.name_Surface = pygame.Surface(self.name_Surface_dim)
        self.thruster_name = thruster_name
        self.power = 0
        self.r = self.gauge_Surface_dim[0]//6 #Surface / number of thrusters
        self.theta1 = -3*math.pi/4
        self.theta2 = 3*math.pi/4
        self.center = (round(self.gauge_Surface_dim[0]/2), round(self.gauge_Surface_dim[1]/2))
        self.font_size = 12
        pub.subscribe(self._power_listener,thruster_name+"_Widget")

    def _power_listener(self, output):
        self.power = output
        
    def _thruster_gauge(self):
        self.gauge_Surface.fill((0, 0, 0))
        pygame.draw.circle(self.gauge_Surface, self.GREY, self.center, round(self.r*1))
        pygame.draw.circle(self.gauge_Surface, self.GREEN, self.center,round(self.r*0.3))
        pygame.draw.line(self.gauge_Surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta1-math.pi/2)+self.gauge_Surface_dim[0]/2, self.r*1.2*math.sin(self.theta1-math.pi/2)+self.gauge_Surface_dim[1]/2), 5)
        pygame.draw.line(self.gauge_Surface, self.GREEN, self.center, (self.r*1.2*math.cos(self.theta2-math.pi/2)+self.gauge_Surface_dim[0]/2, self.r*1.2*math.sin(self.theta2-math.pi/2)+self.gauge_Surface_dim[1]/2), 5)
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
        pygame.draw.line(self.gauge_Surface, BLUE_TO_RED, (self.center), (self.r*math.cos(theta-math.pi/2)+self.gauge_Surface_dim[0]/2, self.r*math.sin(theta-math.pi/2)+self.gauge_Surface_dim[1]/2), 3)
        #power = self.FL_power
        return self.gauge_Surface

    def _thruster_percentage(self):
        #self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size1)
        self.percentage_Surface.fill((0,0,0))
        if self.power>0:
            text = self.myfont.render(str("{:.1f}".format(self.power*100))+'%', True, (200, 200, 200))
        else:
            text = self.myfont.render(str("{:.1f}".format(self.power*100))+'%', True, (200, 200, 200))
        self.text_mid_align(self.percentage_Surface,text)
        return self.percentage_Surface
        
    def _thruster_name(self):
        self.name_Surface.fill((0,0,0))
        #self.myfont = pygame.font.SysFont('Comic Sans MS', self.font_size2)
        text = self.myfont.render(str(self.thruster_name), True, (200, 200, 200))
        self.text_mid_align(self.name_Surface,text)
        return self.name_Surface

    def update(self):
        self.assemble_tuple = (self._thruster_name(),self._thruster_gauge(),self._thruster_percentage())
        self.assemble_dict[self.assemble_tuple] = (0, 0)
        self._draw(self.assemble_dict)
        return self.Surface   




        

#######################################

class GUI(Module):
    def __init__(self, screen_width, screen_height):
        self.on = True
        if self.on:
            pygame.init()
            self.control_invert = False
            self.screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
            self.a = StatusWidget((200, 70))
            self.b = StatusWidget((200, 90))
            self.FL = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterFL')
            self.FR = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterFR')
            self.BL = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterBL')
            self.BR = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterBR')
            self.UF = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterUF')
            self.UB = ThrusterWidget((int(screen_width)//6, 100), 'ThrusterUB')
            self.Thrusters = self.FL+self.FR+self.BL+self.BR+self.UF+self.UB
            self.ab = self.a+self.b
            self.display_list = [self.Thrusters, self.a]
            self.update_list = [self.FL, self.FR, self.BL, self.BR, self.UF, self.UB, self.a]
            print('################')

    def run(self):
        if self.on:
            self.screen.fill((0, 0, 0))
            x = 0
            y = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
                     #quit()
            for objects in self.display_list:
                #print(objects.assemble_dict)
                self.screen.blit(objects.update(), (x,y))
                y = y + objects.height
            for objects in self.update_list:
                objects.update()
            pygame.display.flip()
