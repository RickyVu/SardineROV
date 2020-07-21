import socket
import pickle
import time
from ModuleBase import Module
from pubsub import pub


class HTTP_Client(Module):
    def __init__(self, port, simulation=False):
        pub.subscribe(self.send_listener, "activate")
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)        
        self.port = int(port)      
        self.connected = False
        self.connecting = False
        if type(simulation) == str:
            self.simulation = eval(simulation)
        else:
            self.simulation = simulation

    def connect_reconnect(self):
        if not self.connected:
            self.s.setblocking(True)
            try:
                self.s.connect(("::1", self.port, 0, 0)) 
                self.connected = True
                self.connecting = False
            except:
                print("connecting...")

    def recv(self, size = 1024):
        try:
            self.s.setblocking(1)
            self.recv_bytes = self.s.recv(size)
        except BlockingIOError:
            pass
        except OSError:
            self.connected = False

    def run(self):
        if not self.connecting:
            self.connect_reconnect()
            self.recv()
            pub.sendMessage("activate", message = True)

        #Recv code here#

    def send_listener(self, message):
        if self.connected:
            try:
                if message == True:
                    self.s.send(b"activate")
                else:
                    self.s.send(b"deactivate")
                print("sent")
            except OSError:
                self.connected = False









class HTTP_Server(Module):
    def __init__(self, port, simulation=False):
        pub.subscribe(self.send_listener, "control-movement")
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)            
        self.s.bind(("::1", int(port)))
        self.s.listen()    
        self.connected = False
        self.connecting = False
        self.simulation = simulation
        self.recv_bytes = b""

    def connect_reconnect(self):
        if not self.connected:
            self.s.setblocking(True)
            self.connecting = True
            self.clientsocket, self.address= self.s.accept()
            print(f"Connection from {self.address} has been established")
            self.connected = True
            self.connecting = False

    def recv(self, size = 1024):
        try:
            self.clientsocket.setblocking(1)
            self.recv_bytes = self.clientsocket.recv(size)
            print("recv_bytes in connectors", self.recv_bytes)
        except BlockingIOError:
            print("blocking error")
        except OSError as e:
            print(e)
            self.connected = False
        

    def run(self):
        if not self.connecting:
            self.connect_reconnect()
            self.recv()
            #Recv code here#

    def send_listener(self, message):
        if self.connected:
            try:
                if message == True:
                    self.clientsocket.send(pickle.dumps(message))
                else:
                    self.clientsocket.send(pickle.dumps(message))
            except OSError:
                self.connected = False












'''
class HTTP_Server():
    def __init__(self, PORT, IP = socket.gethostname()):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((IP, PORT))
        self.s.listen(2)
        self.t = threading.Thread(target= self._connect, daemon = True)
        self.data = None
        self.t.start()

    def _connect(self):
        self.clientsocket, self.address= self.s.accept()
        print(f"Connection from {self.address} has been established")
        t1 = threading.Thread(target = self._receive, daemon = True)
        self.recv_loop = True
        t1.start()

    def _reconnect(self):
        self.data = None
        self.recv_loop = False
        self._connect()
        
    def _receive(self):
        while self.recv_loop:
            try:
                msg = self.clientsocket.recv(100)
                #self.data = json.loads(msg)
                self.data = msg.decode("utf-8")
            
            except ConnectionResetError:
                self._reconnect()

    def send_disconnect(self):
        try:
            self.clientsocket.send(bytes("/*disconnect*/", Format))
        except:
            pass

    def send_stop(self):
        try:
            self.clientsocket.send(bytes("/*stop*/", Format))
        except:
            pass

    def send_continue(self):
        try:
            self.clientsocket.send(bytes("/*continue*/", Format))
        except:
            pass

    def disconnect(self):
        self.recv_loop = False

    def get_data(self):
        return self.data
'''
'''
if __name__ == '__main__':
    handler = HTTP_Handler(1234)

    while True:
        if handler.data != None:
            print(handler.get_data())
        #time.sleep(2)
'''
'''
class HTTP_Sender():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.disconnected = True
        self.recv_loop = True
        self.stop = False

    def _connect(self, PORT, IP = socket.gethostname()):
        self.connecting = True
        while self.connecting:
            try:
                self.s.connect((IP, PORT))
                self.connecting = False
                self.disconnected = False
                print('Connected')
                self.receive_thread= threading.Thread(target = self._receive, daemon = True)
            except:
                pass
                #print('Failed to connect, reconnecting...')

    def send(self, msg = ''):
        try:
            if self.stop == False:
                self.s.send(bytes(msg, Format))
            #self.s.send(json.dumps(msg))
        
        except:
            self.s.close()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.disconnected = True
            self.connecting = True
            print('Disconnected...')
            self.connect(self.connect_info)
            

    def connect(self, connect_info):
        self.connect_info = connect_info
        t = threading.Thread(target = self._connect, args = [connect_info], daemon = True)
        t.start()

    def _receive(self):
        while self.recv_loop:
            try:
                msg = self.s.recv(100)
                self.data = msg.decode("utf-8")
                if self.data == "/*disconnect*/":
                    self.disconnect()
                elif self.data == "/*stop*/":
                    self.stop = True
                elif self.data == "/*continue*/":
                    self.continues()
            
            except ConnectionResetError:
                pass#self._reconnect()

    def continues(self):
        self.stop = False

    def disconnect(self):
        self.recv_loop = False
        self.connecting = False
        self.s.close()
'''
'''        
if __name__ == '__main__':
    Sender = HTTP_Sender()
    Sender.connect(1234)
    a = 1
    while True:
        a+=1
        if not Sender.disconnected:
            Sender.send(a)
        #print(a)
        time.sleep(2)
'''
if __name__ == "__main__":
    client = HTTP_Client(1234)
    client.start(1000)
