from multiprocessing import Process, Lock


class Alg_Lamport():
    
    def __init__(self, num_banks) -> None:
        
        # Vetor de relógios lógicos
        self.clock = [0] * num_banks
        
        # Cria um objeto Lock para sincronização
        self.lock = Lock()
        self.list_process = []

    # Função para atualizar o relógio lógico
    def update_clock(self, process_id):
        # Incrementa o relógio lógico do processo em 1
        self.clock[process_id] += 1


    # Função que representa um processo
    def process(self, process_id, lock):
        # Simula alguma operação
        # Neste exemplo, vamos simplesmente atualizar o relógio 5 vezes
        for _ in range(5):
            # Seção crítica
            with lock:
                # Atualiza o relógio lógico
                self.update_clock(process_id)
                # Imprime o relógio atualizado
                print(f"Processo {process_id}: {self.clock}")
            # Fim da seção crítica



# Função principal
if __name__ == "__main__":
    
    lamp = Alg_Lamport(3)
    
    

    for i in range(3):
        lamp.list_process.append( Process(target=lamp.process, args=(i, lamp.lock)).start())
        
                         
    # Aguarda até que todos os processos terminem
    for p in lamp.list_process:
       
        p.join()