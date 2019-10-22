from pubsub import pub
from ModuleBase import Module
import can
from can import Message

class Thruster(Module):
    def __init__(self, name, address, invert):
        self.name = name
        self.address = address
        self.invert = invert
        pub.subscribe(self.__listener, name)
        
    def run(self):
        pass
    def __listener(self, power):
        bustype = 'socketcan'
        channel = 'can0'
        bus = can.interface.Bus(channel=channel, bustype=bustype)
        if self.invert== False:
            if power>=0:
                power = power*32767
            else:
                power = power*32768
            msg = can.Message(arbitration_id= self.address,
                                  data= [(int(power)>>8)&(0xFF), int(power)&(0xFF)],
                                  is_extended_id=False)
        else:
            if power>=0:
                power = power*-32768
            else:
                power = power*-32767
            msg = can.Message(arbitration_id= self.address,
                                  data= [int(power>>8)&(0xFF), int(power)&(0xFF)],
                                  is_extended_id=False)
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Message NOT sent")


'''
bustype = 'socketcan'
channel = 'vcan0'

def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
        bus.send(msg)

    time.sleep(1)

producer(10)
'''

