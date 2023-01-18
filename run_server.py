import sys
import socket
import threading
from UI import *

# import pyfiglet

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

    def header(self):
        # ascii_banner = pyfiglet.figlet_format("CHAT SERVER")
        # print(ascii_banner)
        print(self.header_title + '\n')
        print(f"Conectado em {self.server.host}:{self.server.port}")
        print(f"Usuários conectados: {len(self.server.clients)}")
        separator(64)

    def active_clients(self):
        columns = [' #', 'Name', 'IP']
        print(f'{columns[0]} | {columns[1]:<40} | {columns[2]}')
        for index, client in enumerate(self.server.clients):
            print(f'{index + 1:2} | {client.name:<40} | {client.addr[0]}:{client.addr[1]}')
        separator(64)

    def print_log_events(self):
        for e in self.server.get_log_events():
            print(e)

    def update(self):
        self.clear_screen()
        self.header()
        self.active_clients()
        self.print_log_events()


class Server:
    def __init__(self, shost, sport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # holds all connected clients
        self.clients = list()

        # log a history of # last events
        self._max_log_events = 4
        self._log_event = list()

    def log_events(self, event):
        if len(self._log_event) == self._max_log_events:
            self._log_event.pop(0)
        self._log_event.append(event)

    def get_log_events(self):
        return self._log_event

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

    def broadcast(self, message):
        for c in self.clients:
            c.client.send(message.encode('ascii'))

    def accept_connection(self):
        return self.server.accept()

    def connect_client(self, client):
        self.clients.append(client)

        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

        print(f"{client.name} connected.")
        self.broadcast(f"{client.name} entrou na sala.")

    def disconnect_client(self, c):
        self.clients.remove(c)
        c.close_connection()
        self.broadcast(f"\n{c} saiu da sala.")
        self.log_events(f"{c} left the room.")
        ui.update()

    def handle(self, client):
        while True:
            try:
                message = client.receive()
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
        return self.client.recv(1024).decode('ascii')

    def __repr__(self):
        return self.name


server = Server(host, port)
server.start()

ui = ServerUI(server)
ui.start("CHAT SERVER", 150, 40, '3E')

server.run()
