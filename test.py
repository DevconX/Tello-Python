import socket
import threading
import time
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video.bind(('192.168.10.3', 6038))

## threading
# h264 = []
#
# def receive_video():
#     global h264
#     while True:
#         data, addr = sock_video.recvfrom(10000)
#         print(len(data))
#         h264.append(data[2:])
#
# receive_thread = threading.Thread(target=receive_video)
# receive_thread.daemon=True
# receive_thread.start()
#
# #sock.sendto('land'.encode('utf-8'), ('192.168.10.1',8889))
# command = bytearray.fromhex('9617')
# sock.sendto(b'conn_req:'+bytes(command), ('192.168.10.1',8889))
# sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
# sock.sendto(bytes(bytearray.fromhex('cc600027682000000004fd9b')), ('192.168.10.1',8889))
# time.sleep(3)
# sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
# time.sleep(3)
# sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
# time.sleep(3)
# print(len(h264[0]))

## sequential
h264 = []
command = bytearray.fromhex('9617')
sock.sendto(b'conn_req:'+bytes(command), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc600027682000000004fd9b')), ('192.168.10.1',8889))

try:
    while True:
        data, addr = sock_video.recvfrom(10000)
        print(len(data))
        h264.append(data[2:])
except KeyboardInterrupt:
    pass

sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))

try:
    while True:
        data, addr = sock_video.recvfrom(10000)
        print(len(data))
        h264.append(data[2:])
except KeyboardInterrupt:
    pass


print(len(h264[0]))
with open('test.p','wb') as fopen:
    pickle.dump(h264, fopen)
with open('test.h264','wb') as fopen:
    fopen.write(b''.join(h264))
