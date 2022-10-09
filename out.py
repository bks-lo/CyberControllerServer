import socket
import threading
import json

class TcpServer:
    def __init__(self):
        self.port=2233#���ö˿�
        self.HEAD_LEN=8
        self.tcpServerSocket=socket.socket()#����socket����
        hostname= socket.gethostname()#��ȡ����������
        sysinfo = socket.gethostbyname_ex(hostname)
        hostip=sysinfo[2][2]
        self.tcpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#�ö˿ڿ��Ը���
        self.tcpServerSocket.bind((hostip,self.port))#����ַ���׽��ְ󶨣����׽���Ҫ���Ǵ�δ���󶨹���
        self.tcpServerSocket.listen(5)#�����¼����Ŷӵȴ�connect�������Ŀ

    def set_receive_listener(self,receive_listener):
        self.receive_listener = receive_listener
    def server(self):
        while True:
            print("�ȴ�����")
            self.clientSocket, addr = self.tcpServerSocket.accept()
            print ('���ӵ�ַ��', addr)
            if self.connected_listener:
                self.connected_listener()
            while True:
                try:
                    head_data=self.clientSocket.recv(self.HEAD_LEN)
                    if not len(head_data)==8:
                        print("bad package!head_data len:",head_data)
                        self.restart()
                        return
                    body_len = self.get_length_from_head_data(head_data)
                    body_data = self.clientSocket.recv(body_len)
                    if not body_len==len(body_data):
                        print("bad package!body_len:",body_len)
                        self.restart()
                        return
                    data_type = self.get_type_from_head_data(head_data)

                    if data_type == 1:#test/json data
                        text = body_data.decode()
                        print(text)
                        if not text:
                            break
                        if self.receive_listener