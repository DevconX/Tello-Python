from flask import Flask, Response
from flask_socketio import SocketIO, send, emit
from queue import Queue
import base64
import cv2
import numpy as np
from PIL import Image
import io
d = dirname(dirname(abspath(__file__)))

app = Flask(__name__)
app.queue = Queue()
socketio = SocketIO(app)

@socketio.on('connect', namespace='/live')
def test_connect():
    print('Client wants to connect.')
    emit('response', {'data': 'OK'},broadcast=True)

@socketio.on('disconnect', namespace='/live')
def test_disconnect():
    print('Client disconnected')

@socketio.on('livevideo', namespace='/live')
def test_live(message):
    app.queue.put(message['data'])
    emit('camera_update', {'data': app.queue.get()},broadcast=True)

# change port and IP
if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', port = 8020,debug=True)
