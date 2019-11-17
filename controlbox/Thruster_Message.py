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
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        self.target_power = 0
        self.current_power = 0
        self.max_rate = 0.5
        self.output_power = 0
        
    def run(self): #calculate rate, set message and send to bus
        rate = (self.target_power-self.current_power)/(self.interval*10) #power needed/interval
        if (rate>self.max_rate): #Prevent rate too large
            rate = self.max_rate
        elif rate<self.max_rate*-1:
            rate = self.max_rate*-1
        self.current_power = rate+self.current_power
        if self.invert == True: #Deal with invert
            self.current_power = self.current_power *-1
        #Set to range of -32768 to 32767
        if self.current_power>=0:
            self.output_power= int(self.current_power*32767)
            print(self.current_power)
            #print(self.current_power)
        else:
            self.output_power= int(self.current_power*32768)
            print(self.current_power)
            #print(self.current_power)
        
        print('power', self.output_power)
        msg = can.Message(arbitration_id= self.address,
                          data= [32, self.output_power>>8 & 0xff , self.output_power & 0xff],
                          is_extended_id=False)
        try:
            self.bus.send(msg)
            print("Message sent on {}".format(self.bus.channel_info))
        except can.CanError:
            print("Message NOT sent")
        
            
    def __listener(self, power): #Set target power
        self.target_power = power
        #print(self.target_power)
