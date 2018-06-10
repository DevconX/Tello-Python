import socket
import threading
import time
import pickle
import cv2

header = b'\x00\x00\x00\x01gM@(\x95\xa0<\x05\xb9\x00\x00\x00\x01h\xee8\x80'
h264 = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video.bind(('192.168.10.3', 6038))

def receive_video():
    global h264
    while True:
        data, addr = sock_video.recvfrom(2048)
        if len(data[2:]) not in [8,13]:
            h264.append(data[2:])

def run_cam():
    global h264
    while True:
        if sum([int(len(i) < 1000) for i in h264]) == 2:
            print('a')
            with open('temp.h264','wb') as fopen:
                fopen.write(header+b''.join(h264))
            h264 = []
            cap = cv2.VideoCapture('temp.h264')
            while True:
                try:
                    ret, frame = cap.read()
                    cv2.imshow('cam',frame)
                    if cv2.waitKey(30) & 0xFF == ord('q'):
                        break
                except:
                    break

receive_thread = threading.Thread(target=receive_video)
receive_thread.daemon=True
receive_thread.start()
receive_cam_thread = threading.Thread(target=run_cam)
receive_cam_thread.daemon = True
receive_cam_thread.start()

command = bytearray.fromhex('9617')
sock.sendto(b'conn_req:'+bytes(command), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc600027682000000004fd9b')), ('192.168.10.1',8889))
try:
    while True:
        time.sleep(0.1)
        sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
except KeyboardInterrupt:
    pass
