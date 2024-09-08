import logging 
import socket
from datetime import timedelta
from threading import Thread
from typing import List, Callable
import time 
import struct 
import queue
import matplotlib.pyplot as plt
import numpy as np 
import socketio 
from PIL import Image
from lap import * 
from data import Data 
import requests 
from salsa20 import *  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class GT7Comms(Thread):
    """ Sets up the communication between the Playstation and the Computer """
    def __init__(self, send_port=33739, receive_port=33740, playstation_ip="255.255.255.255", lap_callback: Callable[[Lap], None] = None):
        super().__init__()
        self.send_port = send_port
        self.receive_port = receive_port
        self.playstation_ip = playstation_ip
        self.daemon = True
        self._shall_run = True
        self.package_number = 0
        self.laps = []
        self.current_lap = 0
        self.last_process_time = time.time() 
        self.current_lap_coordinates = [] 
        self.xy_interval = 0.1
        self.lap_callback = lap_callback
        self.connected = False 
        
        self.sio = socketio.Client() #initialize the socket.IO client
        self.sio.connect('http://127.0.0.1:5000') #connect to the flask server (hence this program is a client)
        

    def _send_hb(self, socket):
        send_data = 'A'
        socket.sendto(send_data.encode('utf-8'), (self.playstation_ip, self.send_port))
        
    def _processxy_(self):
        if not self.current_data.is_paused:
            x = self.current_data.position_x 
            y = self.current_data.position_z
            z = self.current_data.position_y 
            
            braking = self.current_data.brake
            throttle = self.current_data.throttle 
            
            return (x,y,z, braking, throttle)     
        
    def _carspeed(self):
        if not self.current_data.is_paused:
            car_speed = self.current_data.car_speed 
    
    def _process_data(self):
        current_time = time.time()
        if current_time - self.last_process_time >= self.xy_interval: #only logging xy coordinates at a certain (small) interval. 
            throttle = self.current_data.throttle 
            
            if self.current_data.tyre_slip_ratio_FL:
                front_slip = self.current_data.tyre_
                self.send_to_server(f)
 
            logging.info("sending throttle")
            self.send_to_server(throttle, 'throttle') 
            
            xytuple = self._processxy_()
            
            if xytuple:
                self.current_lap_coordinates.append(xytuple) 
            
            self.last_process_time = current_time
        
        
        if self.current_data.current_lap > self.current_lap: #A new lap has been started 
            logging.info(f"Current Lap: {self.current_data.current_lap}")
            new_lap = Lap(self.current_lap, self.current_data.last_lap, self.current_lap_coordinates) 
            
            if not new_lap.lapno == 0:
                self.laps.append(new_lap)
                self.current_lap_coordinates = [] 
            
        
            self.current_lap = self.current_data.current_lap     
            
            if self.lap_callback:
                self.lap_callback(new_lap)  
                
            self.send_lap_to_server(new_lap) 
                
    #utility function that will send a single data type to the flask server. 
    def send_throttle_to_server(self, throttle):
        throttle_data = {'throttle' : throttle} 
        self.sio.emit('throttle_data', throttle_data) 
        
    def send_to_server(self, data, type):
        data = {f'{type}' : data}
        self.sio.emit(f'{type}_data', data)  
                
    def send_lap_to_server(self, lap): 
        lap_data = {
            'lapno': lap.lapno,
            'laptime': lap.laptime,
            'coordinates': lap.coordinates
        }
        
        self.sio.emit('lap_data', lap_data) 
        
                
                
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(('0.0.0.0', self.receive_port))
            self._send_hb(s)

            while self._shall_run:
                self.connected = True 
                data, address = s.recvfrom(4096)
                self.package_number += 1

                if self.package_number > 100:
                    self._send_hb(s)
                    self.package_number = 0

                ddata = salsa20_dec(data)
                
                if len(ddata) > 0 and struct.unpack('i', ddata[0x70:0x70 + 4])[0] > 0:
                    self.current_data = Data(ddata) 
                    self._process_data() 
                

    def stop(self):
        self._shall_run = False
    

# data stream decoding
def salsa20_dec(dat):
    try:
        key = b'Simulator Interface Packet GT7 ver 0.0'
        # Seed IV is always located here
        oiv = dat[0x40:0x44]
        iv1 = int.from_bytes(oiv, byteorder='little')
        # Notice DEADBEAF, not DEADBEEF
        iv2 = iv1 ^ 0xDEADBEAF
        iv = bytearray()
        iv.extend(iv2.to_bytes(4, 'little'))
        iv.extend(iv1.to_bytes(4, 'little'))
        ddata = Salsa20_xor(dat, bytes(iv), key[0:32])
        magic = int.from_bytes(ddata[0:4], byteorder='little')
        if magic != 0x47375330:
            return bytearray(b'')
        return ddata
    except Exception as e:
        logging.info("ERROR")
        

if __name__ == "__main__":
    def new_lap_callback(lap):
        lap_queue.put(lap)  # Put the new lap into the queue
    
    lap_queue = queue.Queue()  # Create a queue for lap data
    gt7comms = GT7Comms(lap_callback=new_lap_callback)
    gt7comms.start()
    
    laps = []
    
    if not gt7comms.connected:
        logging.info(f"Not connected.")
    
    try:
        while gt7comms.is_alive:
            try:
                new_lap = lap_queue.get(timeout=1)  #Wait to retrieve new lap with a timeout of 1 
                gt7comms.connected = True 
                
                
                logging.info(f"New Lap created! {new_lap.lapno}")
                if(new_lap and new_lap.coordinates):                    
                    new_lap.add_image() 
                    laps.append(new_lap) 
                    logging.info(f"LAPTIME: {new_lap.laptime}")      
                     
            except queue.Empty:
                continue
    except KeyboardInterrupt:
        gt7comms.stop()
        gt7comms.join()