from ModuleBase import Module
import socket                
import cv2
import numpy as np
from pubsub import pub

class Simulation_Link(Module):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)          
        port = 1234        
        self.s.connect(("::1", port, 0, 0)) 

    def run(self):
        failed = True
        while failed:   
            try:  
                size = int(self.s.recv(6).decode("utf-8"))
                failed = False
            except:
                pass
        total = 0
        data = b''
        while total<size:
            receive = self.s.recv(1024)
            data += receive
            total+= len(receive)

        if data!= None:
            nparr = np.frombuffer(data, np.uint8)
            np_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            pub.sendMessage("image_array", np_img)

