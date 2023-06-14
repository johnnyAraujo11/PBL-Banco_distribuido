import threading

# Classe para representar o relógio lógico

class LamportClock:
    
    def __init__(self, num=0):
        self.num = num
        self.vector = [0] * num
        

    def increment_clock(self,pos ):
        self.vector[pos] += 1

    '''
    Recebe dois vetores de relógio
    '''
    def update_clock(self, other_time, pos):
        for i in range(self.num):
            if(pos == i):
                self.vector[i] = max(self.vector[i], other_time[i]) + 1
            else:
                self.vector[i] = max(self.vector[i], other_time[i]) 

    def get_vector_clock(self):
        return self.vector
        
    
