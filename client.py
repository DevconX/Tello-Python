import cv2
import base64
from socketIO_client import SocketIO, BaseNamespace
import numpy as np
import time
from PIL import Image
from threading import Thread, ThreadError
import io

img_np = None
# change port and IP
socketIO = SocketIO('http://192.168.0.102', 8020)
live_namespace = socketIO.define(BaseNamespace, '/live')

def receive_events_thread():
    socketIO.wait()

def on_camera_response(*args):
    global img_np
    img_bytes = base64.b64decode(args[0]['data'])
    img_np = np.array(Image.open(io.BytesIO(img_bytes)))

live_namespace.on('camera_update', on_camera_response)
receive_events_thread = Thread(target=receive_events_thread)
receive_events_thread.daemon = True
receive_events_thread.start()

while True:
    try:
        cv2.imshow('cam',img_np)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    except:
        continue
