import can
from ModuleBase import Module
from can import Message
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.MessageListener, 'Thruster Power Output')
        pub.subscribe(self.EM_TL_Listener, "EM_TL")
        pub.subscribe(self.EM_TR_Listener, "EM_TR")
        #pub.subscribe(self.InputListener, 'control-movement')

    def InputListener(self, message):
        pass
        #print(message)

    def EM_TL_Listener(self, message):
        if message == 1:
            msg = can.Message(arbitration_id = 0x30, data = [48, 16])
            print("Left EM on")
        else:
            msg = can.Message(arbitration_id = 0x30, data = [48,0])
            print("Left EM off")

        try:
            self.bus.send(msg)
        except can.CanError:
            print("message not sent")
    def EM_TR_Listener(self, message):
        if message == 1:
            msg = can.Message(arbitration_id = 0x30, data = [49,16])
            print("Right EM on")
        else:
            msg = can.Message(arbitration_id = 0x30, data = [49,0])
            print("Right EM off")

        try:
            self.bus.send(msg)
        except can.CanError:
            print("message not sent")

    def MessageListener(self, pub):
        #print(pub[0])
        msg = can.Message(arbitration_id= eval(pub[0]),
                         data= [32, pub[1]>>8 & 0xff, pub[1] & 0xff],
                          is_extended_id=False)
#        print(pub[0], pub[1], type(pub[0]))
        #print(pub[0])
        #if int(pub[0]) == 0x01D:
        #    print("CAN Message", pub[0], "message", pub[1])
        try:
            #_ = 0
            self.bus.send(msg)
            #print("Message sent on {}".format(self.bus.channel_info))
        except can.CanError:
            print("Message NOT sent")

    def run(self):
        message = self.bus.recv(1)
#        print(message)


if __name__ == '__main__':
    handler = CAN_Handler()
    handler.start(10)
    import time
    from random import randint
    r = randint
    for i in range(500):
        pub.sendMessage('Thruster Power Output', pub=('0x017', r(4000, 6000)))
        pub.sendMessage('Thruster Power Output', pub=('0x018', i * 20 + 1000))
        pub.sendMessage('Thruster Power Output', pub=('0x01C', i * 20 + 1000))
        time.sleep(0.3)

    pub.sendMessage('Thruster Power Output', pub=('0x017', 0))
    pub.sendMessage('Thruster Power Output', pub=('0x018', 0))
    pub.sendMessage('Thruster Power Output', pub=('0x01C', 0))
    print('stopped')
