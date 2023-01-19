import os
import sys
import json
import socket
import threading

from consolechat.gui import UI, colors, MSG_TOKEN_DECORATOR
from consolechat.version import __version__


# Used to force win terminal(cmd) accept ANSI colors.
os.system("")

if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print(f"{colors.WARNING}* Uso: \n   > python run_client.py host (no formato '127.0.0.1') porta (int).{colors.ENDC}")
    sys.exit()


class ClientUI(UI):
    def __init__(self):
        super().__init__()
        self.header_title = "Chat client"

    def header(self):
        print(f"\n{self.header_title} {__version__}")
        print(f"{colors.OKGREEN}Conectado!{colors.ENDC}\n")

    def update(self):
        self._clear_screen()
        self.header()


client_ui = ClientUI()
client_ui.start(150, 40)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f"Console chat {__version__}")
    print("Tentando conectar ao servidor...")
    client.connect((host, port))

except ConnectionRefusedError:
    print(f"\n{colors.FAIL}Não foi possível conectar ao servidor {host}:{port}.\n"
          f"Verifique se o endereço e porta estão corretos e tente novamente.")
    client.close()
    sys.exit()


client_ui.update()
nickname = input("Nickname: ")


def receive():
    while True:
        try:
            data = client.recv(1024).decode('ascii')
            if data == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                message = json.loads(data)
                print(f"{MSG_TOKEN_DECORATOR[message['header']]}"
                      f"{message['sender']}: {message['body']}"
                      f"{colors.ENDC}")
        except Exception as e:
            print(e)
            client.close()
            sys.exit()


def write():
    while True:
        try:
            message = input("\n> ")
            json_message = {"header": "msg", "sender": nickname, "body": message}
            data = json.dumps(json_message).encode('ascii')
            client.sendall(data)
        except Exception as e:
            print(e)
            pass


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
