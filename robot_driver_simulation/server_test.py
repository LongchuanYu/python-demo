import socket
import time

_MAX_BUFFER_SIZE = 1024


class ServerTest:
    def __init__(self) -> None:
        self.master_socket = None
        self.ip = '0.0.0.0'
        self.port = 8600
        self.create_master_socket()

    def create_master_socket(self):
        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master_socket.bind((self.ip, self.port))
        self.master_socket.listen()

        # accept会阻塞，但是不会从消息队列里面pop东西，只有执行recv才会pop。
        self.master_socket, slave_addr = self.master_socket.accept()
        msg = self.master_socket.recv(_MAX_BUFFER_SIZE)
        time.sleep(1)
        # self.master_socket.sendall(b'connected')  # uncomment when port is not 8600

    def get_cart_pose(self):
        self.master_socket.sendall(b'CRBT,4,65,69')
        recv_msg = self.master_socket.recv(_MAX_BUFFER_SIZE)
        print(recv_msg.decode())

    def set_cart_movel(self):
        self.master_socket.sendall(b'CRBT,6,99,433000,0,791000,0,90,0,1224195')
        recv_msg = self.master_socket.recv(_MAX_BUFFER_SIZE)
        print(recv_msg.decode())

    def send_custom_msg(self, msg):
        self.master_socket.sendall(msg.encode())
        recv_msg = self.master_socket.recv(_MAX_BUFFER_SIZE)
        print(recv_msg.decode())

    def recv_msg(self):
        recv_msg = self.master_socket.recv(_MAX_BUFFER_SIZE)
        print(recv_msg.decode())



def main():
    q = False
    server = ServerTest()
    while not q:
        cmd = input('1:get_cartpose 2:set_cart_movel other: custom msg> ')
        if cmd == 'q':
            return

        if cmd == '1':
            server.get_cart_pose()
        elif cmd == '2':
            server.set_cart_movel()
        elif cmd == '3':
            server.recv_msg()
        else:
            server.send_custom_msg(cmd)

if __name__ == '__main__':
    main()
