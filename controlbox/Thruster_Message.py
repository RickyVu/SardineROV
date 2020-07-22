from pubsub import pub
from ModuleBase import Module

class Thruster(Module):
    def __init__(self, name, address, invert):
        self.name = name
        self.address = str(address)
        self.invert = eval(invert)
        pub.subscribe(self.__listener, name)
        self.target_power = 0
        self.current_power = 0
        self.output_power = 0
        self.max_rate = 0.05
    def run(self): #calculate rate, save in pub_data, then pub it
        if self.invert:
            self.current_power *= -1
        difference = (self.target_power - self.current_power)*self.interval
        #self.max_increment = 5 * self.interval
        #difference = self.target_power - self.current_power
        '''
        if abs(difference) > self.max_increment:
            self.current_power = self.current_power + (self.max_increment*difference/abs(difference))
        else:
            self.current_power = self.current_power + difference
        '''
        if abs(difference)> self.max_rate:
            difference = (difference/abs(difference))*self.max_rate
        self.current_power = self.current_power + difference
        #if abs(self.current_power)>1:
        #    self.current_power = self.current_power/abs(self.current_power)


        #Set to range of -32768 to 32767
        if self.output_power>=0:
            self.output_power= int(self.current_power*32767)
        else:
            self.output_power= int(self.current_power*32768)

        pub_data= (self.address, self.output_power)
        # Message Topic: Thruster/0a/Power
        #if self.name == "ThrusterUB":
        #    print(self.address, self.output_power)
        pub.sendMessage('Thruster Power Output', pub = pub_data)
        pub.sendMessage(str(self.name)+'_Widget', output = pub_data[1]/32768)
#        print(power)
#        print(pub_data)
        

            
    def __listener(self, power): #Set target power
        self.target_power = power
        #pub_data = (self.address, int(power*32767))
        #pub.sendMessage("Thruster Power Output", pub = pub_data)
        #pub.sendMessage(str(self.name)+"_Widget", output = int(pub_data[1]))
        #print(pub_data)
        #if self.name == "ThrusterUB":
        #    print(self.target_power)

    
