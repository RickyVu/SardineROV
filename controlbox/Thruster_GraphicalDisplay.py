import time
import pygame
from pubsub import pub
from ModuleLoader import Loader
from Test import Thruster

pygame.init()
screen = pygame.display.set_mode((400, 300))
GREY=(192,192,192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
rect = pygame.Rect(150, 100, 60, 60)
FL = 0
FR = 0
BL = 0
BR = 0
UL = 0
UR = 0
Loader.load_controls(10000, 10000)
Loader.load_all('config_test.yaml', 10)
def FLListener(power):
        global FL
        FL = power*25
def FRListener(power):
        global FR
        FR = power*25
def BLListener(power):
        global BL
        BL = power*25
def BRListener(power):
        global BR
        BR = power*25
def ULListener(power):
        global UL
        UL = power*25
def URListener(power):
        global UR
        UR = power*25
pub.subscribe(FLListener, 'ThrusterFLa')
pub.subscribe(FRListener, 'ThrusterFRa')
pub.subscribe(BLListener, 'ThrusterBLa')
pub.subscribe(BRListener, 'ThrusterBRa')
pub.subscribe(ULListener, 'ThrusterULa')
pub.subscribe(URListener, 'ThrusterURa')
        
while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        quit()
        '''
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_KP9]: y -= 3; x += 3
        if pressed[pygame.K_KP1]: y += 3; x -= 3
        if pressed[pygame.K_KP3]: x += 3; y += 3
        if pressed[pygame.K_KP7]: x -= 3; y -= 3
        '''

        screen.fill((0, 120, 200))
        pygame.draw.rect(screen,GREY,rect,3)
        pygame.draw.line(screen, GREY, (150,100), (150-FL, 100-FL),3)
        pygame.draw.line(screen, GREY, (210,100), (210+FR, 100-FR),3)
        pygame.draw.line(screen, GREY, (150,160), (150-BL, 160+BL),3)
        pygame.draw.line(screen, GREY, (210,160), (210+BR, 160+BR),3)
        if int(UL)>=0:
                pygame.draw.circle(screen, RED, (170, 130), int(UL))
        else:
                pygame.draw.circle(screen, GREEN, (170, 130), int(-1*UL))
        if int(UR)>=0:
                pygame.draw.circle(screen, RED, (190, 130), int(UR))
        else:
                pygame.draw.circle(screen, GREEN, (190, 130), int(-1*UL))

        pygame.display.flip()

