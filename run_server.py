import os
import sys
import socket
import threading
import pyfiglet

if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar os argumentos: host (no formato '127.0.0.1') e porta (int).")
    sys.exit()


class UI:
    def __init__(self, main_server):
        self.server = main_server
        self.width = int()
        self.height = int()
        self.color = str()
        self.opr_sys = os.name
        self.os_commands = {}

    def set_opsys(self):
        if self.opr_sys == 'nt':
            self.os_commands = {
                'CLEAR_SCREEN': 'cls'
            }
        else:
            self.os_commands = {
                'CLEAR_SCREEN': 'clear'
            }

    def set_ui(self, width, height, color):
        self.width, self.height, self.color = width, height, color

        #set console size (x, y)
        cmd = f'mode {self.width},{self.height}'
        os.system(cmd)

        # set console color (ANSI)
        color = f'color {self.color}'
        os.system(color)

    def start(self, width, height, color):
        self.set_opsys()
        self.set_ui(width, height, color)

    def header(self):
        ascii_banner = pyfiglet.figlet_format("CHAT SERVER")
        print(ascii_banner)
        print(f"Connected at {self.server.host}:{self.server.port}")
        print(f"Active clients: {len(self.server.clients)}")
        print('-' * 64)

    def clear_screen(self):
        os.system(self.os_commands['CLEAR_SCREEN'])

    def active_clients(self):
        columns = [' #', 'Name', 'IP']
        print(f'{columns[0]} | {columns[1]:<40} | {columns[2]}')
        for index, client in enumerate(self.server.clients):
            print(f'{index + 1:2} | {client.name:<40} | {client.addr[0]}:{client.addr[1]}')
        print('-' * 64)

    def update(self):
        self.clear_screen()
        self.header()
        self.active_clients()


class Server:
    def __init__(self, shost, sport):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = shost
        self.port = sport

        # holds all connected clients
        self.clients = list()

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
        self.broadcast(f"{client.name} connected.")

    def disconnect_client(self, c):
        self.clients.remove(c)
        c.close_connection()
        ui.update()
        self.broadcast(f"\n{c} left the room.")
        print(f"\n{c} left the room.")

    def handle(self, client):
        while True:
            try:
                message = client.receive()
                self.broadcast(message)
            except Exception as e:
                print(e)
                self.disconnect_client(client)
                break


class Client:
    def __init__(self, client, addr, name):
        self.client = client
        self.addr = addr
        self.name = name

    def close_connection(self):
        self.client.close()

    def receive(self):
        self.client.recv(1024).decode('ascii')

    def __repr__(self):
        return self.name


def run():
    while True:
        ui.update()
        client, adress = server.accept_connection()
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        new_client = Client(client, adress, nickname)
        server.connect_client(new_client)


server = Server(host, port)
server.start()

ui = UI(server)
ui.start(150, 40, '3E')

run()
