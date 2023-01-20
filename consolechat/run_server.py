import os
import sys
import socket
import threading

from logger import Logger
from gui import ServerUI
from data import DataProtocol as protocol
from data import Data

# Used to force win terminal(cmd) accept ANSI colors.
os.system("")


if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar os argumentos: host (no formato '127.0.0.1') e porta (int).")
    sys.exit()


class Server:
    def __init__(self, shost, sport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # logger object
        self._logger = Logger(max_events=10, max_log_messages=100)

        # holds all connected clients
        self._clients = list()

    @property
    def clients(self):
        return self._clients

    @property
    def logger(self):
        return self._logger

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

    def broadcast(self, message):
        self._logger.log_message(message)
        for c in self.clients:
            c.client.sendall(message.encode('ascii'))

    def accept_connection(self):
        return self.server.accept()

    def connect_client(self, client):
        self.clients.append(client)

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

        connection_message = protocol.connection_data(client.name)
        data = protocol.send_data(connection_message)
        self._logger.log_event(data)
        self.broadcast(data)
        ui.update()

    def disconnect_client(self, client):
        self.clients.remove(client)
        client.close_connection()

        disconnection_message = protocol.disconnection_data(client.name)
        data = protocol.send_data(disconnection_message)
        self._logger.log_event(data)
        self.broadcast(data)
        ui.update()

    def handle(self, client):
        while True:
            try:
                message = client.receive()
                self.broadcast(protocol.send_data(message))
            except Exception as e:
                self.disconnect_client(client)
                break
            ui.update()


class Client:
    def __init__(self, client, addr, name):
        self.client = client
        self.addr = addr
        self.name = name

    def close_connection(self):
        self.client.close()

    def receive(self):
        return protocol.receive_data(self.client.recv(1024))

    def __repr__(self):
        return self.name


# the app main loop
def run():
    while True:
        ui.update()

        client, adress = server.accept_connection()
        handshake = Data(header="handshake", sender="server")
        client.send(protocol.send_data(handshake.data).encode('ascii'))
        nickname = protocol.receive_data(client.recv(1024).decode('ascii'))
        new_client = Client(client, adress, nickname["sender"])

        server.connect_client(new_client)


if __name__ == "__main__":
    server = Server(host, port)
    server.start()

    ui = ServerUI(server)
    ui.start(150, 40)

    run()
