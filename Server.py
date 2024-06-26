import socket
import json
from _thread import * # type: ignore

class Server:
    def __init__(self, server):
        self.server = server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_users = {}
        self.keep_running = True
        self.receiving_client = ""

    def start_server(self):
        #server = "192.168.0.95"
        #server = "10.81.9.86"
        port = 5555

        try:
            self.s.bind((self.server, port))

        except OSError as e:
            if e.winerror == 10049 or e.winerror == 10060:
                # print("Can't start server. Check server address. \nIt should be the exact same as your local IP address.")
                # pass
                raise OSError("Server1")
        try:
            self.s.listen()
            print("Server started... \nWaiting for connection...")
        except:
            raise OSError("Server2")
            # print("Can't start server. Check server address.")
            # pass

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
                                raise OSError("User already exists...")
                            
                        self.connected_users[reply.lstrip("!")] = conn
                        print(reply.lstrip("!") + " connected")
                        
                    elif reply.find("@") > -1:
                        del self.connected_users[reply.lstrip("@")]
                        print(reply.lstrip("@") + " disconnected")
                        conn.close()
                        break
                        #return OSError(10003, "User already exists...")
                    
                    elif reply.find("*") > -1:
                        users = ""
                        for name in keys:
                            users += name + " "
                        conn.send(str.encode(users))
                        continue

                    elif reply.find("^") > -1:
                        self.receiving_client = reply.lstrip("^")
                        self.connected_users[self.receiving_client].send(str.encode(str(conn) + " is sending you files"))
                        conn.send(str.encode("Request sent"))
                        continue

                    elif reply.find("C:") > -1:
                        self.connected_users[self.receiving_client].send(str.encode(reply))
                        conn.send(str.encode("Sent"))
                        continue

                    print("Received: " + reply)
                    print("Sending : " + reply)

                conn.sendall(str.encode(reply))

            except:
                print("An error happened in the server. Good luck with that.")
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
    ip = input("What is the server ip? ")
    main_server = Server(ip)
    main_server.start_server()
    main_server.run()
