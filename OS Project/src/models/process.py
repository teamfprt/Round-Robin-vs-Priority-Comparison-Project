class Process:
    def __init__(self, pid: int, arrival: int, burst: int, priority: int = 0, quantum: int = 0):
        self.id = pid
        self.burst = burst
        self.remaining = burst
        self.start = None
        self.arrival = arrival
        self.priority = priority
        self.completion = 0
        self.quantum = quantum