from ModuleBase import Module
from pubsub import pub
from threading import Timer

class EM(Module):
    def __init__(self):
        pub.subscribe(self.EM_TL_Listener, "EM_TL")
        pub.subscribe(self.EM_TR_Listener, "EM_TR")

    def EM_TL_Listener(message):
        pass
    def EM_TR_Listener(message):
        pass
