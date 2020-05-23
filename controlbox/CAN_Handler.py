import can
from ModuleBase import Module
from can import Message
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.MessageListener, 'Message')

    def MessageListener(self, pub):
        msg = can.Message(arbitration_id= eval(pub[0]),
                         data= [32, pub[1]>>8 & 0xff, pub[1] & 0xff],
                          is_extended_id=False)
        print(pub[0], pub[1])
        try:
            #print("TestTestTest")
            #print(pub)
            self.bus.send(msg)
            print("Message sent on {}".format(self.bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
    
    def run(self):
        #print("Test2Test2Test2")
        message = self.bus.recv(1)
        print(message)

