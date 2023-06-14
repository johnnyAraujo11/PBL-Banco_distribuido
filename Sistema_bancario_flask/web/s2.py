from flask import Flask, render_template, request
import lamport 
import requests
from servers import SERVERS
import time
import bank
import threading as td

app = Flask(__name__)






@app.route("/")
def page_initial():
    return render_template('index.html')

'''
Envia solicitações para todos os outro bancos
'''
@app.route("/send_msg_to_servers", methods=['POST'])

def send_msg_to_servers():    
    data_json = {}
    global server_confirm 
    #Incrementa o relógio em 1 na sua posião do vetor
    lamport.increment_clock(pos)
    
   
    data_json = transfom_json(  request.form.get("conta_origem"),
                        request.form.get('conta_destino'),
                        request.form.get('valor'),
                        request.form.get('banco_de'),
                        request.form.get('banco_para'),
                        lamport.get_vector_clock(),
                        request.form.get('tipo_operacao'),
                        name_server
                        )
        
    process_list.append(data_json)
    
      
    server_confirm  = server_confirm + 1
    
    #Envia a mensagem para todos os outros banco.
    print(broadcast(data_json))
     
    return "Enviado a mensagem"                                             
    
    
 
'''
Recebe as mensagens enviadas de outros bancos
'''                
@app.route("/receive_msg_from_server", methods=['POST'])
def receive_msg():
    data = request.get_json()    
    global server_confirm 
    
    # Atualiza o relógio
    lamport.update_clock(data.get("clock"), pos)
   
    print(lamport.get_vector_clock())
    
    #Adicionar a mesagem na fila de processos
    process_list.append(data)
    print(process_list)

    server_confirm += 1
    send_confirm(data.get("sendler"))
    
    print("lista de confirmacao {}".format(server_confirm))
    
    return str(pos),200    
    
    
'''
Recebe uma solicitação afim e saber se o processo pode ser executado
'''   
@app.route("/confirm", methods=['POST'])
def sum_confirm_msg(): 
    global server_confirm
    server_confirm = server_confirm + 1
    print("list con {}".format(server_confirm))
    print(request.get_data())
    return "", 200     
    
         
'''
Realiza um broadcast informando ao outros bancos que existe uma solicitação
'''         
def broadcast(data_json):
    global server_confirm 
    response = None
    for i in range(len(SERVERS)):
        srv = SERVERS[i]
        if(name_server != srv.get("server_name")):
            response = requests.post(format_url(srv.get('hostname'), srv.get('port'),'receive_msg_from_server'), json=data_json) 
            if(response.status_code == 200):
                server_confirm =  server_confirm + 1 
            
    print("ao receber mensagem a lista de confirmacao {}".format(server_confirm))
    return response.text


'''
Envia uma mensagem para informar ao outro bancos que confirma a msg recebida e que pode executar o processo 
'''
def send_confirm(server_sent):
    for i in range(len(SERVERS)):
        srv = SERVERS[i]
        if(name_server != srv.get("server_name") and server_sent != srv.get("server_name")):
            print("ue era ara enviar")
            response = requests.post(format_url(srv.get('hostname'), srv.get('port'),'/confirm'), json='1') 
        

'''
Verifica se é o próprio banco que realizará a execução da operação
'''
def is_bank_process(server):
    return True if server == name_server.split('-')[1] else False

'''
Criar um objeto com as informações do processo
'''
def transfom_json(account_origin, account_destiny, value, bank_ori, bank_destiny, clock, type_operation, sendler):
    return {"account_origin":account_origin,
            "account_destiny":account_destiny,
            "value":value,
            "bank_ori": bank_ori,
            "bank_destiny":bank_destiny,
            "type_operation":type_operation,
            "clock":clock,
            "pos":pos,
            "sendler":sendler
            }
    


'''
Identificar 
'''
def type_request():
    pass



'''
Formata os dados para enviar uma mensagem http
'''
def format_url(localhost, port,web_page):
    return f'http://{localhost}:{port}/{web_page}'


'''
Executa o servidor
'''
def run(name, address, port):
    app.run(debug=True, host=address,port=port)

 

def run_process():
    while server_confirm != len(SERVERS):
        time.sleep(2)
        print("processo não pode ser executado {}".format(server_confirm))
       
       


 
check_run_process = False
num_bank = 2
pos = 1
process_list = []
server_confirm = 0
 
#td.Thread(target=run_process, daemon=True).start()
    
    
lamport = lamport.LamportClock(num_bank)
name_server = 'server-1'
run(name=name_server, address='localhost', port=60000)   
   
   