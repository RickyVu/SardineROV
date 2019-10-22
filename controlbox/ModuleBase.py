# Functional Modules
import time
from threading import Thread
from threading import Event

# https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval/48709380#48709380
class Interval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=Event()
        thread=Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

class Module:
    def __init__(self):
        self._running = False
        pass
    
    def run(self):
        pass

    def start(self, freq=1):
        self._running = True
        self.interval = 1/freq
        self.thread = Interval(self.interval, self.run)

    def stop(self):
        if self._running:
            self.thread.cancel()
        self._running = False
