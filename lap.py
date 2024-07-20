import datetime 
import matplotlib.pyplot as plt 

class Lap:
    def __init__(self, lapno, laptime, coordinates):
        self.lapno = lapno
        self.laptime = laptime  
        self.coordinates = coordinates 
                
    # __repr__ function for logging purposes 
    def __repr__(self):
        if not self.lapno == 0:

            return f"Lapno: {self.lapno}, Laptime: {self.laptime}, Coordinates: {self.coordinates}"
                 
        else:
            return "No Lap recorded:" 