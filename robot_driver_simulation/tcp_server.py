# Copyright (c) XYZ Robotics Inc. - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential


import socket
from threading import Lock

_MAX_BUFFER_SIZE = 1024

class TcpServer(object):


    def __init__(self, ip, port):
        """
        Args:
            ip(str): 
            port(uint):
        """
        self._ip_addr = (ip, port)
        self._server_socket = None
        self._client_scoket = None
        self._client_addr = None
        self._client_mutex = Lock()


    def close_socket(self):
        """ close server socket and client socket
        """
        with self._client_mutex:
            if self._client_scoket is not None:
                self._client_scoket.close()
        if self._server_socket is not None:
            self._server_socket.close()

    def create_client(self):
        """ wait for client to connect
        """
        print("Creating client...")
        self._server_socket.listen(1)
        with self._client_mutex:
            print("Accepting connect from robot...")
            self._client_scoket, self._client_addr = self._server_socket.accept()
            print("Accepted connect from {}".format(self._client_addr))

    def close_client(self):
        """ close client
        """
        print("close client socket...")
        with self._client_mutex:
            if self._client_scoket is not None:
                self._client_scoket.close()
                self._client_scoket = None

    def create_server(self):
        """ create server socket and accept client connection 
        """
        print("Creating server socket...")
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(self._ip_addr)
        self._server_socket.listen(1)
        print("Accepting connect from robot...")
        self._client_scoket, self._client_addr = self._server_socket.accept()
        print("Accepted connect from {}".format(self._client_addr))


    def send_and_recv(self, msg, timeout=5):
        """ send msg to robot and recv reply
        Args:
            msg(str): msg for sending to robot
            timeout(float): timeout should be positive. unit second
        Return:
            recv_msg(str): reply msg from robot
        """
        with self._client_mutex:
            self._client_scoket.sendall(msg.encode())
            self._client_scoket.settimeout(timeout)
            recv_msg = self._client_scoket.recv(_MAX_BUFFER_SIZE)
        return recv_msg
