import datetime 

class Lap:
    def __init__(self, lapno, laptime):
        self.lapno = lapno
        self.laptime = laptime  
        
    def __repr__(self):
        if not self.lapno == 0:
            return f"Lap number: {self.lapno}, laptime = {self.laptime}"    
        else:
            return "No Lap recorded:"