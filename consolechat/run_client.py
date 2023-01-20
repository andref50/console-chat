import os
import sys
import socket
import threading

from gui import ClientUI, colors, MSG_TOKEN_DECORATOR
from data import sftp


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
            raw_data = client.recv(1024).decode('ascii')
            json_data = sftp.receive_data(raw_data)
            data = sftp.convert_json_to_data(json_data)

            if data["header"] == 'handshake':
                handshake = sftp.create_data('', header='handshake', sender=nickname)
                client.send(sftp.send_data(handshake).encode('ascii'))
            else:
                print(f"{MSG_TOKEN_DECORATOR[data['header']] if data['sender'] != nickname else colors.BOLD}"
                      f"{data['sender'] if data['sender'] != nickname else 'Você'}: {data['body']}"
                      f"{colors.ENDC}")

        except Exception as e:
            print(e)
            client.close()
            sys.exit()


def write():
    while True:
        try:
            message = input("\n> ")
            json_message = sftp.create_data(message, header="msg", sender=nickname)
            packet = sftp.send_data(json_message)
            client.sendall(packet.encode('ascii'))
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
