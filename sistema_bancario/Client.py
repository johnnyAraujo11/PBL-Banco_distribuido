import socket
import json
from servers import SERVERS
 
# Codigo responsável por fazer uma conexão tcp, realizar uma conexão e enviar uma msg codificada

class Client_TCP: 
    def __init__(self, host='localhost', port_TCP=8080):
            self.host = host
            self.port = port_TCP
            self.port_TCP = port_TCP
            self.data_payload = 2048 

        
       
    def send_mensage(self, msg): 
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port_TCP))
            
            s.send(msg.encode())
            
            # Aguarda a resposta do servidor
            data = s.recv(1024)
            if data :
                print(f"Mensagem do cliente: {data.decode()}")
            
            # Fecha a conexão com o servidor
            s.close()
            return data.decode()
        
    
