import socket
from _thread import * # type: ignore

class Server:
    def __init__(self, server):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_users = {}
        self.keep_running = True

    def start_server(self):
        #server = "192.168.0.95"
        #server = "10.81.9.86"
        port = 5555

        try:
            self.s.bind((self.server, port))

        except OSError as e:
            if e.winerror == 10049:
                print("Can't start server. Check server address. \nIt should be the exact same as your local IP address.")
                exit()
        try:
            self.s.listen()
            print("Server started... \nWaiting for connection...")
        except:
            print("Can't start server. Check server address.")
            exit()

    def threaded_client(self, conn):
        #conn.send(str.encode("Connected"))
        reply = ""
        checking = True
        while checking:
            try:
                data = conn.recv(2048)
                reply = data.decode("utf-8")
                keys = self.connected_users.keys()

                if not data:
                    print("Disconnected")
                    break
                else:
                    if reply.find("!") > -1:
                        for name in keys:
                            if name == reply.lstrip("!"):
                                conn.close()
                            
                        self.connected_users[reply.lstrip("!")] = conn
                        print(reply.lstrip("!") + " connected")
                        
                    if reply.find("@") > -1:
                        del self.connected_users[reply.lstrip("@")]
                        print(reply.lstrip("@") + " disconnected")

                    print("Received: " + reply)
                    print("Sending : " + reply)

                conn.sendall(str.encode(reply))

            except:
                break

    def get_connected_users(self):
        return self.connected_users
    
    def stop(self):
        self.s.close()
        self.keep_running = False

    def run(self):
        while self.keep_running:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            start_new_thread(self.threaded_client, (conn,))

if __name__ == "__main__":
    main_server = Server("192.168.0.95")
    main_server.start_server()
    main_server.run()
    
