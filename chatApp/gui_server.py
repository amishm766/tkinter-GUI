import sys
import socket
import logging
import traceback
import pandas as pd
from threading import Thread

class Server():
    """ This class initializes the server class
    """
    def __init__(self, server_ip = '', server_port = 8081):
        """ This method initializes class Server
        """
        if len(sys.argv) != 3: 
            print("Correct usage: script, IP address, port number")
            self.server_ip = server_ip
            self.server_port = server_port
        else:
            self.server_ip = str(sys.argv[1]) 
            self.server_port = int(sys.argv[2])

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()
        print('Server object created')

        self.clients_file = '/home/pi/Documents/projects/gui/chatApp/client.csv'
        self.client_data = pd.read_csv(self.clients_file, encoding = 'utf8')

        self.connection_file = '/home/pi/Documents/projects/gui/chatApp/connection.csv'
        self.connection_data = pd.read_csv(self.connection_file, encoding = 'utf8')

    def client_task(self, client_name, client_conn, client_addr):
        global clients
        try:
            while True:
                message = ''
                self.data = client_conn.recv(1000) 
                message = '{} : {}'.format(client_name, self.data.decode())
                if self.data.decode():
                    [self.connection_data.ix[client, 'clients_connection'].sendall(message.encode())  for client in list(self.connection_data.clients_name) if client != client_name] 
                    print(message)
                else:
                    #print('Length :', len(list(self.connection_data.clients_name)))
                    if client_name in list(self.connection_data.clients_name):
                        self.connection_data.ix[client_name, 'clients_connection'].close()
                        self.connection_data = self.connection_data.drop([client_name], axis = 0)
                        self.connection_data.to_csv(self.connection_file)
                        print("Client'" ,client_name, "' has left the chatroom")
                    if len(list(self.connection_data.clients_name)) == 0:
                        print('No clients connected')
                    
        except OSError as error:
            print()
        except Exception as e:
            pass        
        except KeyboardInterrupt:
            pass
        
    def connect(self):
        while True:
            conn, addr = s.server_socket.accept()
            print('fetching login credentials from user')
            self.client_login_info = conn.recv(1000).decode()
            self.name =  self.client_login_info.split(',')[0]
            self.password =  self.client_login_info.split(',')[1]
            print('Got a connection from NAME :', self.name, 'and', 'PASSWORD :', self.password)
            self.name_index = s.client_data[s.client_data['client_name'] == self.name].index.tolist()
            self.registered_clients_list = s.client_data.client_name.tolist()
            if self.name in self.registered_clients_list:
                self.client_password = s.client_data.client_password.get_value(self.name_index[0])
                if self.client_password == self.password:
                    self.Ack_message = 'Confirmed'
                    conn.sendall(self.Ack_message.encode())
                    print('Registered User:', self.name_index)
                    self.connection_data = self.connection_data.ix[:, ['clients_name', 'ip_address', 'clients_connection']]
                    self.connection_data.ix[self.name, ['clients_name', 'ip_address', 'clients_connection']] = (self.name, addr[0], conn) 
                    self.connection_data.to_csv(self.connection_file)   
                    t = Thread(target=self.client_task,args=(self.name,conn,addr))
                    t.start()
                else:
                    print('Invalid password')
                    conn.close()
                    continue
            else:
                print('Invalid name')
                conn.close()
                continue
                
def log_file():
    logger = logging.getLogger('Server_logger')
    fh = logging.FileHandler('/home/pi/Documents/projects/gui/chatApp/Server.log')
    fh.setLevel(logging.DEBUG)
    ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(ff)
    logger.addHandler(fh)
    logger.error('The program is starting...')
    

if __name__ == '__main__':           
    try:
        global s
        s = None
        log_file()
        s = Server()
        s.connect()

    except Exception as exception:
        print('Exception Occured :', sys.exc_info(), end = '\n')
        traceback.print_exc()
        
    except FileNotFoundError as er:
        print("The file you wanted to open doesn't exist")
        logger.exception(er)

    except KeyboardInterrupt:
        pass

    finally:
        if s is not None:
            #[print(s.connection_data.ix[client, 'clients_connection'])  for client in list(s.connection_data.clients_name)] 
            s.server_socket.close()
            print('Server closed')
        else:
            print('Server not created, shutting down ...')

