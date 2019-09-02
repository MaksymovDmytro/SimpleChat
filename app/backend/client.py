import socket

from app.backend.settings import *


class Client:
    """IPv4 TCP client implementation"""
    username = None
    connection = None

    def __init__(self, username: str = 'Incognito'):
        self.username = username

    def start_client(self, address: tuple = ADDRESS):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect(address)
        except ConnectionRefusedError:
            print('Connection refused by server! Server may be down.')
            self.connection = None
            return False
        self.connection.sendall(to_b(self.username))
        server_response = self.connection.recv(1024).decode(ENC)
        if "connected" in server_response:
            return True

    def send_message(self, message):
        self.connection.sendall(to_b(message))

    def receive_message(self):
        return self.connection.recv(1024).decode(ENC)



