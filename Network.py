import socket
import File
from Server import Server
import threading

class Network:
    def __init__(self, username, server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        #self.server = "192.168.0.95"
        #self.server = "10.81.9.86"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.username = username
        self.main_server = None
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode("!" + self.username))
            return self.client.recv(2048).decode()
        except OSError as e:
            if e.winerror == 10061:
                print("Websocket not found...")
                print("Creating Websocket...")
                self.main_server = Server(self.server)
                self.main_server.start_server()
                x = threading.Thread(target = self.main_server.run, args = ())
                x.start()
                self.connect()
            else:
                print(e)

        except Exception as e:
            print(e)

    def disconnect(self):
        try:
            self.client.send(str.encode("@" + self.username))
            self.client.close()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

if __name__ == "__main__":
    n = Network("Ethan", "192.168.0.95")
    print(n.send("Hello"))
    print(n.send("Working"))
    n.disconnect()