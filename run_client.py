import sys
import socket
import threading
from UI import *


if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar argumentos: host (no formato '127.0.0.1') e porta (int)")
    sys.exit()


class ClientUI(UI):
    def __init__(self):
        super().__init__()

    def header(self):
        print(self.header_title)


client_ui = ClientUI()
client_ui.start("CHAT SERVER", 150, 40, '3E')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("Console chat 0.1.0")
    print("Tentando conectar ao servidor...")
    client.connect((host, port))
except ConnectionRefusedError:
    print(f"\nNão foi possível conectar ao servidor {host}:{port}.\n"
          f"Verifique se o endereço e porta estão corretos e tente novamente.")
    client.close()
    sys.exit()

nickname = input("Nickname: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            client.close()
            sys.exit()


def write():
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode('ascii'))
        except:
            pass


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
