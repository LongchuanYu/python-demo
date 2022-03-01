from pydoc import cli
import socket
import time

TIME_SLEEP = 0.1
_MAX_BUFFER_SIZE = 1024


class Client:
    def __init__(self) -> None:
        self.client_socket = None
        self.ip = '0.0.0.0'
        self.port = 8600
        self.keep_live = True

        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)
        self.client_socket.connect((self.ip, self.port))
        time.sleep(TIME_SLEEP)
        self.client_socket.sendall(b'connecting')
        print(self.client_socket.recv(_MAX_BUFFER_SIZE).decode())

    def shutdown(self, shut_code):
        try:
            self.client_socket.shutdown(shut_code)
        except Exception as e:
            print(e)


    def send_msg(self, msg):
        print('\033[1;36mmsg send: {}\033[0m'.format(msg))
        self.client_socket.sendall(msg.encode())

    def recv_msg(self):
        try:
            recv_msg = self.client_socket.recv(_MAX_BUFFER_SIZE)
            print('\033[1;33mmsg recieved: {}\033[0m'.format(recv_msg.decode()))
        except socket.timeout:
            print('time out')
            pass

    def send_and_recv(self, msg):
        print('\033[1;36mmsg send: {}\033[0m'.format(msg))
        self.client_socket.sendall(msg.encode())
        try:
            recv_msg = self.client_socket.recv(_MAX_BUFFER_SIZE)
            print('\033[1;33mmsg recieved: {}\033[0m'.format(recv_msg.decode()))
        except socket.timeout:
            print('time out')
            pass

    def server_side_control(self):
        self.send_msg('ssc')



def main():
    q = False
    client = Client()
    while not q:
        inputs = input('> ')
        cmd, params = inputs.split(' ', 1) if len(inputs.split(' ', 1)) > 1 else [inputs, '']
        if cmd == 'q':
            return
        if cmd == 's':
            client.send_msg(params)
        elif cmd == 'r':
            client.recv_msg()
        elif cmd == 'sr':
            client.send_and_recv(params)
        elif cmd == 'close':
            client.shutdown(params)
        elif cmd == 'ssc':
            client.server_side_control()


if __name__ == '__main__':
    main()
