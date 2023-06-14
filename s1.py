from flask import Flask, render_template, request
import lamport 
import requests
from servers import SERVERS
import time
import bank
import threading as td
import schedule


class Server():
    
    def __init__(self):
        self.server_confirm = 0
   

        self.check_run_process = False
        self.num_bank = 2
        self.pos = 0
        self.process_list = []
        self.lamport = lamport.LamportClock(self.num_bank)
        self.name_server = 'server-0'
        self.app = Flask(__name__)
        td.Thread(target=self.check_confirm).start()

        @self.app.route("/")
        def page_initial():
            return render_template('index.html')

        '''
        Envia solicitações para todos os outro bancos
        '''
        @self.app.route("/send_msg_to_servers", methods=['POST'])
        def send_msg_to_servers():    
            data_json = {}
            global server_confirm 
            #Incrementa o relógio em 1 na sua posião do vetor
            self.lamport.increment_clock(self.pos)
            
        
            data_json = self.transfom_json(  request.form.get("conta_origem"),
                                request.form.get('conta_destino'),
                                request.form.get('valor'),
                                request.form.get('banco_de'),
                                request.form.get('banco_para'),
                                self.lamport.get_vector_clock(),
                                request.form.get('tipo_operacao'),
                                self.name_server
                                )
                
            self.process_list.append(data_json)
            
            
            self.server_confirm  = self.server_confirm + 1
            
            #Envia a mensagem para todos os outros banco.
            print(self.broadcast(data_json))
            
            return "Enviado a mensagem"                                             
    
    
 
        '''
        Recebe as mensagens enviadas de outros bancos
        '''                
        @self.app.route("/receive_msg_from_server", methods=['POST'])
        def receive_msg():
            data = request.get_json()    
            global server_confirm 
            
            # Atualiza o relógio
            lamport.update_clock(data.get("clock"), self.pos)
        
            print(lamport.get_vector_clock())
            
            #Adicionar a mesagem na fila de processos
            self.process_list.append(data)
            print(self.process_list)

            server_confirm += 1
            self.send_confirm(data.get("sendler"))
            
            print("lista de confirmacao {}".format(server_confirm))
            
            return str(self.pos),200    
    
    
        '''
        Recebe uma solicitação afim e saber se o processo pode ser executado
        '''   
        @self.app.route("/confirm", methods=['POST'])
        def sum_confirm_msg(): 
            global server_confirm
            server_confirm = server_confirm + 1
            return "", 200     
    
    def check_confirm(self):
        while True:
            time.sleep(2)
            print("sddddd")
        
    '''
    Realiza um broadcast informando ao outros bancos que existe uma solicitação
    '''         
    def broadcast(self, data_json):
        global server_confirm 
        response = None
        for i in range(len(SERVERS)):
            srv = SERVERS[i]
            if(self, self.name_server != srv.get("server_name")):
                response = requests.post(self.format_url(srv.get('hostname'), srv.get('port'),'receive_msg_from_server'), json=data_json) 
                if(response.status_code == 200):
                    self.server_confirm =  self.server_confirm + 1 
            
        print("ao receber mensagem a lista de confirmacao {}".format(self.server_confirm))
        return response.text



    '''
    Envia uma mensagem para informar ao outro bancos que confirma a msg recebida e que pode executar o processo 
    '''
    def send_confirm(self, server_sent):
        for i in range(len(SERVERS)):
            srv = SERVERS[i]
            if(self.name_server != srv.get("server_name") and server_sent != srv.get("server_name")):
                print("ue era ara enviar")
                response = requests.post(self.format_url(srv.get('hostname'), srv.get('port'),'/confirm'), json='1') 
    

    '''
    Verifica se é o próprio banco que realizará a execução da operação
    '''
    def is_bank_process(self, server):
        return True if server == self.name_server.split('-')[1] else False

    '''
    Criar um objeto com as informações do processo
    '''
    def transfom_json(self, account_origin, account_destiny, value, bank_ori, bank_destiny, clock, type_operation, sendler):
        return {"account_origin":account_origin,
                "account_destiny":account_destiny,
                "value":value,
                "bank_ori": bank_ori,
                "bank_destiny":bank_destiny,
                "type_operation":type_operation,
                "clock":clock,
                "pos":self.pos,
                "sendler":sendler
                }
        


    '''
    Formata os dados para enviar uma mensagem http
    '''
    def format_url(self, localhost, port,web_page):
        return f'http://{localhost}:{port}/{web_page}'


    '''
    Executa o servidor
    '''
    def run(self, address, port):
        self.app.run(debug=True, host=address,port=port)



    def run_process(self):
        # Outras instruções...
        while True:
            time.sleep(2)
            print("Mensagem a ser impressa")
        
        
if __name__ == '__main__':
    server = Server()
    #t = td.Thread(target=run_process ,daemon=True)
    #t.start()
    server.run(address='localhost', port=50000)  

   
