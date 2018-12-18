import socket
from threading import Thread

client_socket = socket.socket()
client_socket.connect(('localhost', 2001))

name = input('Enter your name : ')
client_socket.sendall(name.encode())

def receive_data():
    """ Receives data continously
    """
    while True:
        data = client_socket.recv(1000)
        print('server:', data)

def send_data():
    while True:
        user_input = input()
        client_socket.sendall(user_input.encode())
        print('you   :', user_input)


t = Thread(target = receive_data)
t.start()
send_data()
