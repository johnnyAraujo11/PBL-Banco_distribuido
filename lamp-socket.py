import socket
import threading
import time

# Classe que representa um processo
class Process:
    def __init__(self, process_id, host, port, peers):
        self.process_id = process_id
        self.host = host
        self.port = port
        self.peers = peers
        self.clock = [0] * len(peers)
        self.server_socket = None
        self.client_sockets = {}

    # Função para iniciar o processo
    def start(self):
        # Inicializa o socket do servidor para receber conexões
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        # Cria threads para tratar as conexões recebidas
        listen_thread = threading.Thread(target=self.listen_for_connections)
        listen_thread.start()

        # Cria threads para enviar mensagens aos outros processos
        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

    # Função para tratar as conexões recebidas
    def listen_for_connections(self):
        while True:
            conn, addr = self.server_socket.accept()
            peer_id = self.get_peer_id(addr)

            # Cria uma thread para tratar as mensagens recebidas
            receive_thread = threading.Thread(target=self.receive_message, args=(conn, peer_id))
            receive_thread.start()

            # Armazena a conexão em um dicionário
            self.client_sockets[peer_id] = conn

    # Função para enviar mensagens aos outros processos
    def send_messages(self):
        while True:
            # Aguarda um tempo aleatório antes de enviar uma mensagem
            time.sleep(2)
            
            # Atualiza o relógio lógico antes de enviar a mensagem
            self.update_clock()

            # Envia a mensagem a todos os outros processos
            for peer_id, conn in self.client_sockets.items():
                if peer_id != self.process_id:
                    message = f"Evento do processo {self.process_id}"
                    data = (self.process_id, self.clock, message)
                    conn.sendall(pickle.dumps(data))

    # Função para receber mensagens dos outros processos
    def receive_message(self, conn, peer_id):
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # Decodifica a mensagem recebida
            sender_id, sender_clock, message = pickle.loads(data)

            # Atualiza o relógio lógico com base no relógio recebido
            self.update_clock(sender_clock)

            # Imprime a mensagem recebida e o relógio lógico atualizado
            print(f"Processo {self.process_id} recebeu uma mensagem do processo {sender_id}: {message}")
            print(f"Relógio: {self.clock}")

    # Função para atualizar o relógio lógico
    def update_clock(self, received_clock=None):
        self.clock[self.process_id] += 1

        if received_clock:
            for i in range(len(self.clock)):
                self.clock[i] = max(self.clock[i], received_clock[i]) + 1

    # Função para obter o ID do processo com base no endereço
    def get_peer_id(self, addr):
        for peer_id, peer_info in self.peers.items():
            if peer_info == addr:
                return peer_id

# Função principal
if __name__ == "__main__":
    # Define os IDs, hosts e portas dos processos
    process_info = {
        0: ("localhost", 5000),
        1: ("localhost", 5001),
        2: ("localhost", 5002)
    }

    # Cria instâncias dos processos
    processes = {}
    for process_id, (host, port) in process_info.items():
        peers = {p_id: p_info for p_id, p_info in process_info.items() if p_id != process_id}
        process = Process(process_id, host, port, peers)
        processes[process_id] = process
        
        print(processes)
   
    # Inicia os processos
    for process in processes.values():
        process.start()

    '''# Aguarda até que todos os processos terminem
    for process in processes.values():
        process.server_socket.close()'''
