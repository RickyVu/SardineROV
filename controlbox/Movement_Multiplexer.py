from pubsub import pub
from ModuleBase import Module
import time

class Dualplexer(Module):
    def __init__(self, timeout = 0):
        self.sendtime = time.time()
        self.timeout = int(timeout)
        self.can_change = False
        self.active_dict = {"gamepad": True}
        self.last_recv_active = "gamepad"
        pub.subscribe(self.movementlistener, "control-movement")
        pub.subscribe(self.activelistener, "movement_activation")

    #receive string
    def activelistener(self, sender):
        self.last_recv_active = sender
        if self.can_change:
            #Add new node into dict
            if sender not in self.active_dict:
                self.active_dict[sender] = True
            else:
                self.active_dict[sender] = not self.active_dict[sender]
    

            #For exclusion of others 
            for node in self.active_dict.keys():
                if node!= sender:
                    self.active_dict[node] = False

            #set gamepad as active if a node is deactivated
            if not self.active_dict[sender]:
                self.active_dict["gamepad"] = True

            self.can_change = True

                
        for node, value in self.active_dict.items():
            pub.sendMessage("activate_"+node, message = value)

        

    #receive tuple(sender<string>, tuple <6 int> )
    def movementlistener(self, message):
        sender = message[0]
        if sender in self.active_dict:
            if self.active_dict[sender]:
                pub.sendMessage("movement", message= message[1])
                self.sendtime = time.time()


    def run(self):
        if time.time()-self.sendtime>self.timeout:
            self.can_change = True
                
