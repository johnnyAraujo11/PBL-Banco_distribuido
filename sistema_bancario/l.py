import threading

# Classe para representar o relógio lógico

class LamportClock:
    
    def __init__(self, initial_time=0):
        self.time = initial_time
        self.lock = threading.Lock()

    def increment_clock(self):
        with self.lock:
            self.time += 1

    def update_clock(self, other_time):
        with self.lock:
            self.time = max(self.time, other_time) + 1

    def get_time(self):
        with self.lock:
            return self.time
        

