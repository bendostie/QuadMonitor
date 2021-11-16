import socket
import threading
ip_address = "10.65.1.226"
port = 81

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_address, port))
server.listen()
while True:
    print("Waiting for connection")
    connection, client = server.accept()
 
    try:
        print("Connected to client IP: {}".format(client))
         
        # Receive and print data 32 bytes at a time, as long as the client is sending something
        while True:
            data = connection.recv(32)
            print("Received data: {}".format(data))
 
            if not data:
                break
 
    finally:
        connection.close()