import socket

class Network:
    def __init__(self, username):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.95"
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
        except:
            pass

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

n = Network("Ethan")
print(n.send("Hello"))
print(n.send("Working"))
n.disconnect()