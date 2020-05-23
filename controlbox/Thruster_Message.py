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

        rate = (self.target_power - self.current_power)/(self.interval*10) #power needed/interval
        if rate>self.max_rate: #Prevent rate too large
            rate = self.max_rate
        if rate<(self.max_rate*-1):
            rate = self.max_rate*-1
        self.current_power = rate + self.current_power
        self.output_power = self.current_power
        if self.invert == 'True': #Deal with invert
            self.output_power = self.output_power*-1

        #Set to range of -32768 to 32767
        if self.output_power>=0:
            self.output_power= int(self.output_power*32767)
        else:
            self.output_power= int(self.output_power*32768)

        #print(self.output_power)

        pub_data= (self.address, self.output_power)
        pub.sendMessage('Message', pub = pub_data)
        pub.sendMessage(str(self.name)+'_Widget', output = self.output_power)
        
            
    def __listener(self, power): #Set target power
        self.target_power = power


    
