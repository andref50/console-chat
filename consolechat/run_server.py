import os
import sys
import socket
import threading

from data import sftp
from server_ui import server_ui
from events import event_handler
from decorators import Colors
from clients import clients_database

from log_listener import setup_log_event_handlers
from broadcast_listener import setup_broadcast_event_handlers
from server_ui_listener import setup_ui_event_handlers


class Server:
    """
    The class responsible for handling all new connections and messages.
    """

    def __init__(
            self,
            shost: str,
            sport: int
    ) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # Clients database object: holds all connected clients
        self._clients_database = clients_database

        self.server_ui = server_ui

    @property
    def clients(self) -> list:
        return self._clients_database.active_clients()

    def start(self) -> None:
        self.server.bind((self.host, self.port))
        self.server.listen()

    def accept_connection(self) -> tuple:
        return self.server.accept()

    def connect_client(self, client) -> None:
        self._clients_database.add_client(client)

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

        # Post a "client connected to server event" to event handler object
        event_handler.post_event("connect-client", client)

        #
        # TO-DO: remove this method from here, it needs to be server-independet
        #
        # ui.update()

    def disconnect_client(self, client) -> None:
        self._clients_database.remove_client(client)
        client.close_connection()

        # Post a "client disconnected from server event" to event handler object
        event_handler.post_event("disconnect-client", client)

        #
        # TO-DO: remove this method from here, it needs to be server-independet
        #
        # ui.update()

    def handle(self, client) -> None:
        while True:
            try:
                message = client.receive()
                event_handler.post_event("message", message)
            except Exception as e:
                self.disconnect_client(client)
                break


class Client:
    """
    The Client object
    """

    def __init__(
            self,
            client,
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


def run() -> None:
    """
    The app main loop
    """

    while True:
        client, adress = server.accept_connection()

        handshake = sftp.create_data('', header="handshake", sender="server")
        handshake_json = sftp.send_data(handshake)
        client.send(handshake_json.encode('ascii'))

        raw_data = sftp.receive_data(client.recv(1024).decode('ascii'))
        json_data = sftp.convert_json_to_data(raw_data)

        nickname = json_data["sender"]
        new_client = Client(client, adress, nickname)
        server.connect_client(new_client)


if __name__ == "__main__":

    # Force windows terminal(cmd) accept ANSI commands.
    os.system("")

    # Receive host and port number from command-line
    if len(sys.argv) == 3:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
    else:
        print(f"{Colors.WARNING}\n"
              "* Uso:\n"
              "> run_server.py xxx.xxx.xxx.xxx YYYY, onde:\n\n"
              "     xxx.xxx.xxx.xxx: endereço IP\n"
              f"                YYYY: porta{Colors.WARNING}")
        sys.exit()

    # Start server, ui, event handler and run the app.
    server = Server(host, port)
    server.start()

    setup_log_event_handlers()
    setup_broadcast_event_handlers()
    setup_ui_event_handlers()

    run()
