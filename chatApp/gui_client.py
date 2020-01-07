# -*- coding:utf-8 -*-
import sys
import time
import signal
import socket
import select
import tkinter
import logging
import threading
import traceback
import subprocess

from tkinter import *
from threading import Thread

class Client():
    """ This class initializes client socket
    """

    def __init__(self, server_ip = '0.0.0.0', server_port = 8081):
        """ This method initializes class Client() 
        """
        if len(sys.argv) != 3: 
            print("Correct usage: script, IP address, Port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])
        try:    
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            
        except socket.error as error:
            print('Could not open socket due to :', error)

    def receive_data(self):
        """ Receives data continously
        """
        try:
            while True:
                self.data = self.client_socket.recv(1000).decode()
                if self.data and (self.data != 'Confirmed'):
                    app.msg_list.insert(END, self.data)
                    print(self.data)
                    
                elif self.data == 'Confirmed':
                    print('Received confirmaion from server')

                else:
                    #app.login_top.destroy()
                    #self.client_socket.close()
                    break
                    
        except KeyboardInterrupt:
            pass
        
        except Exception as exception:
            print('Exception Occured in receive_data :', sys.exc_info(), end = '\n')
            traceback.print_exc()
            #continue
        
    def send_data(self, event = None):
        """ This method sends the message to the server
        """
        try:
            self.send_message = app.text_box.get()
            self.client_socket.sendall(self.send_message.encode())
            print('you   :', self.send_message)

            # Insert message to the last of the listbox
            app.msg_list.insert(END, "<You > : {}".format(str(self.send_message)))
            app.text_box.delete(0, END)
            app.my_msg.set('')
            
        except KeyboardInterrupt:
            pass
        
        except Exception as exception:
            print('Exception Occured in send_data :', sys.exc_info(), end = '\n')
            traceback.print_exc()
                        
class App(Client):
    """ This class creates a python app
    """
    def __init__(self):
        self.login_top = Tk()
        self.login_top.title("Login page")
        self.password_text = StringVar()
        self.username_entry = Entry(self.login_top, bd = 5)
        self.password_entry = Entry(self.login_top, textvariable = self.password_text, bd = 5, show = '*')
        self.username_label = Label(self.login_top, text = "Username")
        self.password_label = Label(self.login_top, text = "Password")
    
    
    def login(self):
        try:
            self.username_label.grid(row = 0, column = 0)
            self.password_label.grid(row = 1, column = 0)
            self.username_entry.grid(row = 0, column = 1)
            self.password_entry.grid(row = 1, column = 1)
            
            self.client_name = ''
            self.client_password = ''
            send_button = Button(self.login_top, text = 'submit', command = lambda args = (self.client_name, self.client_password) : self.chatApp())   # chatApp(*args)
            self.password_entry.bind("<Return>", s.send_data)
            send_button.grid(row = 2, column = 1)
            
        except KeyboardInterrupt:
            pass
            
        except Exception as exception:
            print('Exception Occured in login:', sys.exc_info(), end = '\n')
            traceback.print_exc()
            
    def chatApp(self, client_name = "", client_password = ""):
        try:
            self.client_name = self.username_entry.get()
            #self.client_name = self.password_text.get()
            self.client_password = self.password_entry.get()
            self.client_login_info = '{},{}'.format(self.client_name, self.client_password)
            print(self.client_login_info)
            s.client_socket.sendall(self.client_login_info.encode())
            print('Sent login data to server',self.client_login_info)
            time.sleep(0.2)
            if s.data == 'Confirmed':
                self.chatAppGUI()
                self.chat_top.mainloop()
            else:
                self.signUpGUI()
                
        except KeyboardInterrupt:
            pass
                
        except Exception as exception:
            print('Exception Occured in chatApp:', sys.exc_info(), end = '\n')
            traceback.print_exc()
            
    def chatAppGUI(self):
        self.login_top.destroy()
                
        # Create a new Screen named chat_top
        self.chat_top = Tk()
        self.chat_top.title('chatApp')
        self.chat_top.geometry('500x500')

        # Create a message frame to contain other widgets
        self.msg_frame = Frame(self.chat_top, relief=SUNKEN)
        self.msg_frame.pack()

        # Create a scrollbar widget
        self.scrollbar = Scrollbar(self.msg_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Create a listbox to store multiple line text
        self.msg_list = tkinter.Listbox(self.msg_frame, height=30, width=60, yscrollcommand=self.scrollbar.set)
        self.my_msg = StringVar()
        self.msg_list.pack(side=LEFT, fill=BOTH)  # expand = True

        self.scrollbar.config(command = self.msg_list.yview)
                
        # Create a text box and a send button
        self.text_box = Entry(self.chat_top, bd = 5)
        self.text_box.bind("<Return>", s.send_data)
        self.text_box.place(x = 250, y = 470)

        # Create a button named send and bind it to sendMessage()
        self.send_button = Button(self.chat_top, text = 'send', command= lambda event = 0 :s.send_data(event))
        self.send_button.place(x = 430, y = 470)
                
        # Create menu bar
        self.menubar = Menu(self.chat_top)
                        
        # Create File as Menu in menu bar
        self.filemenu = Menu(self.menubar, tearoff = 0)
                
        # Add options to File menu
        self.filemenu.add_command(label="Chat", command = self.donothing)
        self.filemenu.add_command(label = "Online", command = self.online)

        self.filemenu.add_separator()

        #self.filemenu.add_command(label = "Exit", command = self.chat_top.destroy)
        self.filemenu.add_command(label = "Exit", command = self.onExit)

        self.menubar.add_cascade(label = "File", menu = self.filemenu)

        # Add menubar to the top level here chatTop
        self.chat_top.config(menu = self.menubar)
    
    def onExit(self,event = None):
        """ This method is called when user chooses to exit
        """
        self.chat_top.destroy()
            
    def signUpGUI(self):
        pass

    def donothing(self):
        """ Does nothing but creates a new window with a button
        """
        filewin = Toplevel()
        button1 = Button(filewin, text="Do nothing button")
        button1.pack()

    def online(self):
        """ After a user chooses to see online people in the chatroom
        """
        self.online_top = Toplevel()
        self.online_top.title("Online")

        
        self.online_top.mainloop()  
        
if __name__ == '__main__':
    try:
        global t, app, lock
        
        s = Client()
        app =App()
        lock = threading.Lock() 
        lock.acquire()
        t = Thread(target = s.receive_data)
        #t.deamon = False
        t.start()
        app.login()
        app.login_top.mainloop()
        
    except KeyboardInterrupt:
        pass
    
    except Exception as exception:
        print('Exception Occured :', sys.exc_info())
        traceback.print_exc()
        #continue
        
    finally:
        if s is not None:
            s.client_socket.close()
            lock.release()
            print('closed client socket')
        else:
            print('Server not created, shutting down ...')
