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
        self.max_rate = 0.02
        self.output_power = 0

    def run(self): #calculate rate, save in pub_data, then pub it
        rate = 1.3 * self.interval
        #rate = (self.target_power - self.current_power)*self.interval
        #if abs(rate)>self.max_rate:
        #    rate = (rate/abs(rate)) * self.max_rate
        #self.current_power = self.current_power + rate
        difference = self.target_power - self.current_power
        if abs(difference)>rate:
            self.current_power = self.current_power + difference/abs(difference)*rate
        else:
            self.current_power = self.current_power + difference
        if abs(self.current_power)>1:
            self.output_power = self.current_power/abs(self.current_power)
        else:
            self.output_power = self.current_power


        #Set to range of -32768 to 32767
        if self.output_power>=0:
            self.output_power= int(self.output_power*32767)
        else:
            self.output_power= int(self.output_power*32768)

        if self.invert == "True":
            self.output_power *= -1

        #if self.output_power>0:
        #    self.output_power = self.output_power * 0.45

        pub_data= (self.address, int(self.output_power))


        # pub_data = (self.address, int(self.target_power * 32767))

        #print(pub_data)
        pub.sendMessage('Thruster Power Output', pub = pub_data)
        pub.sendMessage(str(self.name)+'_Widget', output = pub_data[1]/32768)

            
    def __listener(self, power): #Set target power
        self.target_power = power
        #print(self.target_power)


if __name__ == '__main__':
    import time
    import CAN_Handler
    can = CAN_Handler.CAN_Handler()
    can.start(1)
    tm = Thruster("ThrusterBL", "0x017", "False")
    tm.start(20)
    pub.sendMessage("ThrusterBL", power=0.4)
    time.sleep(5)
    pub.sendMessage("ThrusterBL", power=0)
