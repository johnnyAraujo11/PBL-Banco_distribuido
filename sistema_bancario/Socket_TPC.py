import socket 
import threading

from Client import Client_TCP
import json
from time import sleep
from servers import SERVERS
import l


class Server_Bank():
    
    def __init__(self, name, host='localhost', port_TCP=8080):
        self.name = name
        self.host = host
        self.port_TCP = port_TCP
        self.data_payload = 2048 
        
        self.list_response= []
        self.lamport = l.LamportClock(1)
        
        self.transaction_list = []

        
    def connect(self):
        try:
            self.con_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_address = (self.host, self.port_TCP)
            self.con_socket.bind(self.server_address)
            self.con_socket.listen()
            
            print ("Starting up echo server TCP on:{} port:{}".format(self.host,self.port_TCP, self.host))
            threading.Thread(target=self.client_connect_TCP).start()
          
        except:
            print("Fail when starting the server")

            
    '''
    Função que aguarda a conexão de clientes.
    '''
    def client_connect_TCP(self):
            while True:
                print ("Waiting to receive message from client")
                client, address = self.con_socket.accept()
                client_thread = threading.Thread(target=self.received_mensage, args=(client, address), daemon=True)
                client_thread.start()
    
    
    
                
    '''
    Recebe clientes e suas respectivas mensagens http
    '''
    def received_mensage(self, client, addr):
        print("New connection by {}".format(addr))
        
        data = client.recv(1024)
        
        if data:
            #Atualiza o relógio do server 
            self.lamport.update_clock(2)
            
            print(data)
            #Adiciona o processo na lista
            
            self.type_msg(data.decode())
            
        client.close()      
        print("Close connection")


    '''
    Função chamada quando um banco deseja se comunicar com outros servidores
    '''
    def broadcast_server(self, msg):
        # ideal aqui é ter uma thread que irá criar várias conexões com os servidores
    
        for i in range(len(SERVERS)):
            
           if(self.name != SERVERS[i].get("server_name")):
                c = Client_TCP(SERVERS[i].get("localhost"), port_TCP=SERVERS[i].get("port"))
                self.list_response.append(c.send_mensage(msg))    
                sleep(1)                                   
                
        print("lista de resposta: {}".format(self.list_response))
         
        
    def type_msg(self, msg):
        msg = json.loads(msg)       
       
        if(msg.get('process')):
            print(" é um processo. {}".format( msg.get('process')))
            
            #Adiciona no set
            print(msg)
            
            return '1'
        
        else:
            # Executa se não for uma resposta sobre o processo 
            return '0'