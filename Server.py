import socket
from _thread import * # type: ignore
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected_users = []

def start_server(server):
    #server = "192.168.0.95"
    #server = "10.81.9.86"
    port = 5555

    try:
        s.bind((server, port))

    except socket.error as e:
        str(e)
    try:
        s.listen()
        print("Server started... \nWaiting for connection...")
    except:
        print("Can't start server. Check server address.")
        exit()

def threaded_client(conn):
    #conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                if reply.find("!") > -1:
                    connected_users.append(reply.lstrip("!"))
                    print(reply.lstrip("!") + " connected")
                if reply.find("@") > -1:
                    connected_users.remove(reply.lstrip("@"))
                    print(reply.lstrip("@") + " disconnected")

                print("Received: " + reply)
                print("Sending : " + reply)

            conn.sendall(str.encode(reply))

        except:
            break

def get_connected_users(self):
    return connected_users

def run():
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn,))

if __name__ == "__main__":
    start_server("192.168.0.95")
    run()
    