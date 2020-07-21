import socket                
import pickle
from pubsub import pub
from ModuleBase import Module

#--------------------------------------------------------------
#Add a header (tuples, photos) before sending
#Allow receive of photo AND pickle dumped data
#Allow send to simulation
#--------------------------------------------------------------


def recv_photo(socket):
    failed = True
    while failed:   
        try:  
            size = int(socket.recv(6).decode("utf-8"))
            failed = False
        except:
            pass
    total = 0
    data = b''
    while total<size:
        receive = socket.recv(1024)
        data += receive
        total+= len(receive)
    return data

class HTTP_Client(Module):
    def __init__(self, port, simulation=False):
        pub.subscribe(self.send_listener, "activate_transectline")
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)          
        self.port = int(port)      
        self.connected = False
        self.simulation = eval(simulation)

    def run(self):
        if not self.connected:
            self.s.connect(("::1", self.port, 0, 0)) 
            self.connected = True
        else:
            try:
                recv_bytes = self.s.recv(1024)
                recv_unpickled = pickle.loads(recv_bytes)
                pub.sendMessage("control-movement", message = recv_unpickled[1])
                #try:
                    #Photo in encoded, control-movement is not
                    #recv_message = self.s.recv(1024).decode("utf-8")
                    #pub.sendMessage("simulation_photo", message = recv_photo(self.s))
                    
                #except:
                    #sender, movement = recv_message
                    #pub.sendMessage("movement", message = (sender,eval(movement)))


            except:
                self.connected = False

    def send_listener(self, message):
        if self.connected:
            try:
                if message == True:
                    self.s.send(b"activate")
                else:
                    self.s.send(b"deactivate")
            except:
                self.connected = False



                
