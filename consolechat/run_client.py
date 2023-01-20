import os
import sys
import json
import socket
import threading

from gui import ClientUI, colors, MSG_TOKEN_DECORATOR
from data import DataProtocol as protocol
from data import Data


# Used to force win terminal(cmd) accept ANSI colors.
os.system("")

if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print(f"{colors.WARNING}* Uso: \n   > python run_client.py host (no formato '127.0.0.1') porta (int).{colors.ENDC}")
    sys.exit()


client_ui = ClientUI()
client_ui.start(150, 40)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
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
            received_data = protocol.receive_data(client.recv(1024).decode('ascii'))
            data = protocol.make_data(received_data)
            #data = Data(received_data["body"], header=received_data["header"], sender=received_data["sender"])

            if data.header == 'handshake':
                handshake = Data(header="handshake", sender=str(nickname))
                client.send(protocol.send_data(handshake.data).encode('ascii'))

            else:
                print(f"{MSG_TOKEN_DECORATOR[data.header] if data.sender != nickname else colors.BOLD}"
                      f"{data.sender if data.sender != nickname else 'Você'}: {data.body}"
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


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
