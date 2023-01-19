import os
import sys
import json
import socket
import threading

from consolechat.logger import Logger
from consolechat.gui import separator, colors, UI
from consolechat.version import __version__


# Used to force win terminal(cmd) accept ANSI colors.
os.system("")


if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar os argumentos: host (no formato '127.0.0.1') e porta (int).")
    sys.exit()


class ServerUI(UI):
    def __init__(self, running_server):
        super().__init__()
        self.server = running_server
        self.header_title = "Chat server"

    def header(self):
        # ascii_banner = pyfiglet.figlet_format("CHAT SERVER")
        # print(ascii_banner)
        print(f"{self.header_title} {__version__}\n")
        print(f"{colors.OKGREEN}* Conectado em {self.server.host}:{self.server.port}{colors.ENDC}")
        print(f"* Usuários conectados: {len(self.server.clients)}")
        separator(64)

    def active_clients(self):
        columns = [' #', 'Name', 'IP']
        print(f'{columns[0]} | {columns[1]:<40} | {columns[2]}')
        for index, client in enumerate(self.server.clients):
            print(f'{index + 1:2} | {client.name:<40} | {client.addr[0]}:{client.addr[1]}')
        separator(64)

    def print_log_events(self):
        print("\nEvents log:")
        for event in self.server.logger.get_log_events:
            print(f"{colors.WARNING}{event}{colors.ENDC}")

    def print_log_messages(self):
        print("\nMessages log:")
        for message in self.server.logger.get_log_messages:
            print(message)

    def update(self):
        self._clear_screen()
        self.header()
        self.active_clients()
        self.print_log_events()
        self.print_log_messages()


class Server:
    def __init__(self, shost, sport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # logger object
        self.logger = Logger(max_events=10, max_log_messages=100)

        # holds all connected clients
        self.clients = list()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

    def broadcast(self, message):
        json_message_dumps = json.dumps(message)
        self.logger.log_message(json_message_dumps)
        for c in self.clients:
            c.client.sendall(json_message_dumps.encode('ascii'))

    def accept_connection(self):
        return self.server.accept()

    def connect_client(self, client):
        self.clients.append(client)

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

        self.logger.log_event(f"{client.name} entrou na sala.")
        self.broadcast({"header": "conn", "sender": "server", "body": f"{client.name} entrou na sala."})
        ui.update()

    def disconnect_client(self, client):
        self.clients.remove(client)
        client.close_connection()
        disconnection_message = {"header": "disconn", "sender": "server", "body": f"{client.name} saiu da sala."}
        self.logger.log_event(f"{client.name} saiu da sala.")
        self.broadcast(disconnection_message)
        ui.update()

    def handle(self, client):
        while True:
            try:
                message = client.receive()
                print(message)
                self.broadcast(message)
            except Exception as e:
                self.disconnect_client(client)
                break

    def run(self):
        while True:
            ui.update()
            client, adress = server.accept_connection()
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            new_client = Client(client, adress, nickname)
            self.connect_client(new_client)


class Client:
    def __init__(self, client, addr, name):
        self.client = client
        self.addr = addr
        self.name = name

    def close_connection(self):
        self.client.close()

    def receive(self):
        return json.loads(self.client.recv(1024).decode('ascii'))

    def __repr__(self):
        return self.name


server = Server(host, port)
server.start()

ui = ServerUI(server)
ui.start(150, 40)

server.run()
