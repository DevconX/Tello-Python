import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video.bind(('192.168.10.3', 6038))
#sock.sendto('land'.encode('utf-8'), ('192.168.10.1',8889))
command = bytearray.fromhex('9617')
sock.sendto(b'conn_req:'+bytes(command), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
h264 = []

for i in range(720):
    data, addr = sock_video.recvfrom(10000)
    print(data[2:],len(data),i)
    h264.append(data[2:])

with open('file.h264','wb') as fopen:
    fopen.write(b''.join(h264))
