from cmath import sin
import socket
import time
import signal

TIME_SLEEP = 0.1

_MAX_BUFFER_SIZE = 1024


class SlaveRobot(object):
    def __init__(self):
        self.slave_socket = None
        self.ip = '0.0.0.0'
        self.port = 8600
        self.master_msg = ''
        self.keep_live = True

        # robot
        self.cart_pose_str = '0,0,0,0,0,0'  # unit: um
        self.joints = '0,0,0,0,0,0'

        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

        self.connect_to_master()
        self.waiting_master_msg()

    def connect_to_master(self):
        self.slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slave_socket.connect((self.ip, self.port))
        time.sleep(TIME_SLEEP)
        # must send joints first when robot connect click
        self.send_msg(self.joints)  # uncomment when port is not 8500
        print('==== connect success ====')
    
    def shutdown(self, *args):
        print('shutting down...')
        if self.slave_socket:
            self.slave_socket.shutdown(socket.SHUT_RD)
        self.keep_live = False

    def send_msg(self, body, status=0):
        """
        master_msg format:
        CRBT,4,44,48
        CRBT,op,req,checksum=op+req\r

        send_msg format:
        OPID_CUR_POS=op=4 / req=random / res=0(success) / checksum
        ?, op, req, res, 4, 5, 6, 7, 8, 9, checksum

        :param body:
        :param status:
        :return:
        """
        time.sleep(TIME_SLEEP)
        if not self.master_msg:
            self.slave_socket.sendall(b'connecting')
            return

        crbt, op, req, *_ = self.master_msg.split(',')
        checksum = int(op) + int(req) + int(status) + sum([int(float(num)) for num in body.split(',')])
        msg = '?,{op},{req},{status},{body},{sum}\r'.format(
            op=op, req=req, status=status, body=body,
            sum=checksum
        )
        self.slave_socket.sendall(msg.encode())
        print('\033[1;36mmsg send: {}\033[0m'.format(msg))

    def waiting_master_msg(self):
        print('==== waiting for master msg ====')
        while self.keep_live:
            time.sleep(0.2)
            if self.slave_socket:
                self.handle_master_msg_and_response()

    def handle_master_msg_and_response(self):
        raw_master_msg = self.slave_socket.recv(_MAX_BUFFER_SIZE)
        if not raw_master_msg:
            return
        
        self.master_msg = raw_master_msg.decode()
        print('\033[1;33mmsg recieved: {}\033[0m'.format(self.master_msg))

        if self.master_msg.startswith('CRBT,4,'):
            self.handle_get_cartpose()

        elif self.master_msg.startswith('CRBT,12,'):
            self.handle_get_joints()

        elif self.master_msg.startswith('CRBT,6,'):
            self.handle_set_cart_movel()

        else:
            self.handle_custom_msg()
    
    def handle_get_cartpose(self):
        self.send_msg(self.cart_pose_str)

    def handle_set_cart_movel(self):
        crbt, op, req, *cart_pose_list, checksum = self.master_msg.split(',')
        self.cart_pose_str = ','.join(cart_pose_list)  # um
        self.send_msg(self.cart_pose_str)
            
    def handle_get_joints(self):
        self.send_msg(self.joints)

    def handle_custom_msg(self):
        time.sleep(TIME_SLEEP)
        self.slave_socket.sendall(('respond from slave server: ' + str(self.master_msg)).encode())

robot = SlaveRobot()

