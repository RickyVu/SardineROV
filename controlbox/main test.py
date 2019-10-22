from pubsub import pub
#from normal_test import Gamepad
from threading import Timer
import time

def Listener1(arg1):
    print('listener', arg1)
pub.subscribe(Listener1, 'movement')


#def printinterval(i):
    #print(i)
    #Timer(1, printinterval, [i+1]).start()

#Timer(1, printinterval, [1]).start()
