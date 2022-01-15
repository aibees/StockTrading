import socket

from module.util.Config import Config


class TCPClient :
    def __init__(self):
        self.configs = Config()
        self.host = self.configs.getConfig('socket_local', 'SOCKET_IP')
        self.port = self.configs.getConfig('socket_local', 'SOCKET_PORT')
        self.sc = None
        print("host : " + self.host)
        print("port : " + self.port)

    def connect(self):
        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sc.connect((self.host, int(self.port)))

    def disconnect(self):
        self.sc = None

    def sendData(self, data):
        encodeData = data.encode()
        self.sc.send(encodeData)

