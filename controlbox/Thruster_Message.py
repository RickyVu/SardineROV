from pubsub import pub
from ModuleBase import Module

class Thruster(Module):
    def __init__(self, name, address, invert):
        self.name = name
        self.address = str(address)
        self.invert = str(invert)
        pub.subscribe(self.__listener, name)
        self.target_power = 0
        self.current_power = 0
        self.max_rate = 0.2
        self.output_power = 0

    def run(self): #calculate rate, save in pub_data, then pub it
        rate = (self.target_power - self.current_power)*self.interval*1000
        if abs(rate)>self.max_rate:
            rate = (rate/abs(rate)) * self.max_rate
        self.current_power = self.current_power + rate
        
        self.output_power = self.current_power
        if self.invert == 'True': #Deal with invert
            self.output_power = self.current_power*-1


        if abs(self.output_power)>1:
            self.output_power = self.output_power/abs(self.output_power)

        #Set to range of -32768 to 32767
        if self.output_power>=0:
            self.output_power= int(self.output_power*32767)
        else:
            self.output_power= int(self.output_power*32768)

        pub_data= (self.address, self.output_power)
        pub.sendMessage('Thruster Power Output', pub = pub_data)
        pub.sendMessage(str(self.name)+'_Widget', output = self.output_power/32768)


        

            
    def __listener(self, power): #Set target power
        self.target_power = power


    
