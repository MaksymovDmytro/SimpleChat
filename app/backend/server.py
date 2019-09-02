import socket

from threading import Thread

from app.backend.settings import *


class Chat:
    """IPv4 TCP server implementation"""
    sock = None
    client_connections = dict()
    max_connections = 5

    def __init__(self, address: tuple = ADDRESS):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(self.max_connections)

    def run(self):
        """Creates client threads that read incoming messages and boradcast it to all existing connections"""
        while True:
            client, address = self.sock.accept()
            client_thread = Thread(target=self._serve_client, args=(client, address))
            client_thread.daemon = True
            client_thread.start()

    def _serve_client(self, client: socket.socket, address: str):
        """Listens to client sockets, reads messages and broadcast them to other clients"""
        # First message should always contain username
        username = client.recv(1024).decode(ENC)
        self.client_connections[client] = {
            'username': username,
            'address': address,
        }
        self._broadcast(f'{username} connected')
        while True:
            msg = client.recv(1024).decode(ENC)
            if msg:
                self._broadcast(f'{username}: {msg}', client)
            else:
                self._broadcast(f"{username} disconnected.", client)
                del self.client_connections[client]
                client.close()
                break

    def _broadcast(self, msg, client=None):
        """Sends message to all existing connections"""
        # If client param  is specified it will be excluded from broadcast
        for connection in self.client_connections:
            if connection != client:
                connection.sendall(to_b(msg))


if __name__ == '__main__':
    chat = Chat()
    chat.run()
