import socket
import File
from Server import Server
import threading
import struct

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
            if e.winerror == 10061 or e.winerror == 10057:
                print("Server not found...")
                print("Check server address or check \"Run Server?\"")
                raise OSError("Server not found...")
            elif e.winerror == 10049 or e.winerror == 10060:
                print("Can't start server. Check server address. \nIt should be the exact same as your local IP address.")
                raise OSError("Server1")
            elif e.winerror == 10003:
                print(str(e))
                return
            elif e.errno == 11001:
                print("Non existant server address")
                raise OSError("Server not found...")
            else:
                print(e)
                return

        except Exception as e:
            print(e)
            raise OSError("Server1")

    def get_connected_users(self):
        self.client.send(str.encode("*"))
        return self.client.recv(2048).decode()

    def disconnect(self):
        try:
            self.client.send(str.encode("@" + self.username))
            self.client.close()
        except:
            print("Could not close client connection to server.")
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except OSError as e:
            if e.winerror == 10053:
                print("Could not connect to server...")
                print("User already exists!")
                print("Also, you can't send stuff to \"Select a User\"")
                self.disconnect()
                raise OSError("Could not connect to server...")
    
    def send_file(self, filename):
        try:
            with open(filename, "rb") as f:
                while read_bytes := f.read(1024):
                    self.client.sendall(read_bytes)
            #return self.client.recv(2048).decode()
        except OSError as e:
            if e.winerror == 10053:
                print("Could not connect to server...")
                print("User already exists!")
                self.disconnect()
                raise OSError("Could not connect to server...")    

    def receive_file_size(self):
        # This funcion makes sure that the bytes which indicate
        # the size of the file that will be sent are received.
        # The file is packed by the client via struct.pack(),
        # a function that generates a bytes sequence that
        # represents the file size.
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        received_bytes = 0
        stream = bytes()
        while received_bytes < expected_bytes:
            chunk = self.client.recv(expected_bytes - received_bytes)
            stream += chunk
            received_bytes += len(chunk)
        filesize = struct.unpack(fmt, stream)[0]
        return filesize

    def receive_file(self, filename):
        # First read from the socket the amount of
        # bytes that will be received from the file.
        filesize = self.receive_file_size()
        # Open a new file where to store the received data.
        with open(filename, "wb") as f:
            received_bytes = 0
            # Receive the file data in 2048-bytes chunks
            # until reaching the total amount of bytes
            # that was informed by the client.
            while received_bytes < filesize:
                chunk = self.client.recv(2048)
                if chunk:
                    f.write(chunk)
                    received_bytes += len(chunk)        
    def listen(self):
        try:
            return self.client.recv(2048).decode()
        except:
            return ""

if __name__ == "__main__":
    n = Network("Ethan", "192.168.0.95")
    print(n.send("Hello"))
    print(n.send("Working"))
    n.disconnect()