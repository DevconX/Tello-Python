import socket
import threading
import time
import traceback

class Tello:
    def __init__(self, local_ip, local_port, imperial=True, command_timeout=.3, tello_ip='192.168.10.1', tello_port=8889):
        self.abort_flag = False
        self.command_timeout = command_timeout
        self.imperial = imperial
        self.response = None
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.tello_address = (tello_ip, tello_port)

        self.socket.bind((local_ip, local_port))

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon=True

        self.receive_thread.start()

    def __del__(self):
        self.socket.close()

    def _receive_thread(self):
        while True:
            try:
                self.response, ip = self.socket.recvfrom(2048)
            except Exception:
                break

    def send_command(self, command):
        self.abort_flag = False
        timer = threading.Timer(self.command_timeout, self.set_abort_flag)
        command = bytearray.fromhex(command)
        print(bytes(command))
        self.socket.sendto(bytes(command), self.tello_address)

        timer.start()

        while self.response is None:
            if self.abort_flag is True:
                raise RuntimeError('No response to command')
        timer.cancel()
        response = self.response.decode('utf-8')
        self.response = None
        return response
    def set_abort_flag(self):
        self.abort_flag = True

#copper = Tello('192.168.10.3',8888)
#copper = Tello('192.168.10.3',8888,tello_port=8889)
#copper.send_command('cc58007c60250000006c95')
#copper.send_command('cc58007c6055000000000cbc')
