# -*- coding:utf-8 -*-
import sys
import time
import signal
import socket
import select
import tkinter

from tkinter import *
from threading import Thread

class client():
    """ This class initializes client socket
    """

    def __init__(self, server_ip = '0.0.0.0', server_port = 8081):
        
        if len(sys.argv) != 3: 
            print("Correct usage: script, IP address, port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])
                    
        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_ip, self.server_port))

        self.client_name = input('Enter your NAME : ')
        #self.client_password = input('Enter your PASSWORD : ')
        
        #self.client_info = {}
        #self.client_info['client_name'] = self.client_name
        #self.client_info['client_password'] = self.client_password
        self.client_socket.sendall(self.client_name.encode())

    def receive_data(self):
        """ Receives data continously
        """
        print('Starting receive thread')
        while True:
            self.data = self.client_socket.recv(1000)
            print('server:', self.data)
            
    def send_data(self):
        """ This method sends the message to the server
        """
        while True:
            self.send_message = input()
            self.client_socket.sendall(self.send_message.encode())
            print('you   :', self.send_message)

s = client()
t = Thread(target = s.receive_data)
t.start()
s.send_data()
