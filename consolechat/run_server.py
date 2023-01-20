import os
import sys
import socket
import threading
from typing import Any

from logger import Logger
from gui import ServerUI
from data import sftp

# Used to force win terminal(cmd) accept ANSI colors.
os.system("")

"""
Receive host and port number from command-line
"""
if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar os argumentos: host (no formato '127.0.0.1') e porta (int).")
    sys.exit()


class Server:
    def __init__(
            self,
            shost: str,
            sport: int
    ) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # Logger object: hold all the events that server broadcast
        self._logger = Logger(max_events=100)

        # holds all connected clients
        self._clients = []

    @property
    def clients(self) -> list:
        return self._clients

    @property
    def logger(self) -> Any:
        return self._logger

    def start(self) -> None:
        self.server.bind((self.host, self.port))
        self.server.listen()

    def broadcast(self, message: dict) -> None:
        self._logger.log_event(message)
        packet = sftp.send_data(message)

        for c in self.clients:
            c.client.sendall(packet.encode('ascii'))
        ui.update()

    def accept_connection(self) -> tuple:
        return self.server.accept()

    def connect_client(self, client: Any) -> None:
        self.clients.append(client)

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

        connection_message = sftp.connection_message(client.name)
        self.broadcast(connection_message)

    def disconnect_client(self, client: Any) -> None:
        self.clients.remove(client)
        client.close_connection()

        disconnection_message = sftp.disconnection_message(client.name)
        self.broadcast(disconnection_message)

    def handle(self, client: Any) -> None:
        while True:
            try:
                message = client.receive()
                self.broadcast(message)
            except Exception as e:
                self.disconnect_client(client)
                break


class Client:
    def __init__(
            self,
            client: Any,
            addr: str,
            name: str
    ) -> None:

        self.client = client
        self.addr = addr
        self.name = name

    def close_connection(self) -> None:
        self.client.close()

    def receive(self) -> dict:
        raw_data = self.client.recv(1024).decode('ascii')
        json_data = sftp.receive_data(raw_data)
        data = sftp.convert_json_to_data(json_data)
        return data

    def __repr__(self) -> str:
        return self.name


# the app main loop
def run() -> None:
    ui.update()

    while True:
        client, adress = server.accept_connection()
        handshake = sftp.create_data('', header="handshake", sender="server")
        client.send(sftp.send_data(handshake).encode('ascii'))
        raw_data = sftp.receive_data(client.recv(1024).decode('ascii'))
        json_data = sftp.convert_json_to_data(raw_data)
        nickname = json_data["sender"]
        new_client = Client(client, adress, nickname)

        server.connect_client(new_client)


if __name__ == "__main__":
    server = Server(host, port)
    server.start()

    ui = ServerUI(server)
    ui.start(150, 40)

    run()
