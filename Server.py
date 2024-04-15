import socket
from _thread import * # type: ignore
import sys

server = "192.168.0.95"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected_users = []

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen()
print("Server started... \nWaiting for connection...")

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

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
