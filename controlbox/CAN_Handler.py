import can
from ModuleBase import Module
from can import Message
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.MessageListener, 'Thruster Power Output')
        pub.subscribe(self.InputListener, 'control-movement')

    def InputListener(self, message):
        pass
        #print(message)

    def MessageListener(self, pub):
        #print(pub[0])
        msg = can.Message(arbitration_id= eval(pub[0]),
                         data= [32, pub[1]>>8 & 0xff, pub[1] & 0xff],
                          is_extended_id=False)
#        print(pub[0], pub[1], type(pub[0]))
        #print(pub[0])
        if int(pub[0]) == 0x01D:
            print("CAN Message", pub[0], "message", pub[1])
        try:
            #_ = 0
            self.bus.send(msg)
            #print("Message sent on {}".format(self.bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
    
    def run(self):
        pass
        #message = self.bus.recv(1)
#        print(message)

