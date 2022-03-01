from curses import raw
from http import server
import socket
import time

_MAX_BUFFER_SIZE = 1024


class Server:
    def __init__(self) -> None:
        self.server_socket = None
        self.ip = '0.0.0.0'
        self.port = 8600
        self.keep_alive = True
        self.create_server_socket()
        self.waiting_client_msg()

    def create_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(30)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        
        self.server_socket.listen()


        self.server_socket, _ = self.server_socket.accept()
        raw_msg = self.server_socket.recv(_MAX_BUFFER_SIZE)
        if raw_msg and raw_msg.decode() == 'connecting':
            self.server_socket.sendall(b'==== connect success ====')

    def waiting_client_msg(self):
        print('==== waiting for master msg ====')
        while self.keep_alive:
            time.sleep(0.2)
            if self.server_socket:
                self.handle_master_msg_and_response()

    def send_msg(self, msg):
        print('\033[1;36mmsg send: {}\033[0m'.format(msg))
        self.server_socket.sendall(msg.encode())

    def handle_master_msg_and_response(self):
        raw_client_msg = self.server_socket.recv(_MAX_BUFFER_SIZE)
        if not raw_client_msg:
            return
        client_msg = raw_client_msg.decode()
        print('\033[1;33mmsg recieved: {}\033[0m'.format(client_msg))

        self.send_msg('response from server -> ' + client_msg)

server = Server()