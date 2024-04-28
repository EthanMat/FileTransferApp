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
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.send(str.encode("!" + self.username))
            return self.client.recv(2048).decode()
        except OSError as e:
            if e.winerror == 10053:
                print("Could not connect to server...")
                print("User already exists!")
            elif e.winerror == 10061 or e.winerror == 10057:
                print("Server not found...")
                print("Check server address or check \"Run Server?\"")
                raise OSError("Server not found...")
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