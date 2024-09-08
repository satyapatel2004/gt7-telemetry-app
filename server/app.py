from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S') 

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow connections from http://localhost:3000

# Initialize SocketIO with gevent async mode
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", async_mode='gevent')

lap_data_store = []  # In-memory storage for received lap data

@socketio.on('lap_data')
def handle_lap_data(data):
    print(f"Received lap data: {data}")
    lap_data_store.append(data)  # Store the lap data
    socketio.emit('lap_data', data)  # Emit the lap data event to all clients

@socketio.on('throttle_data')
def handle_throttle_data(data):
    print(f"Received throttle data: {data}")
    app.logger.info("receiving throttle")
    socketio.emit('throttle_data', data)  # Emit the throttle data event to all clients

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('lap_data', lap_data_store)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True)