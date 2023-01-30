import os
import sys
import socket
import threading

from data import sftp
from client_ui import client_ui
from decorators import Colors, MSG_TOKEN_DECORATOR
from client_ui_listener import setup_ui_event_handlers


def receive() -> None:
    while True:
        try:
            raw_data = client.recv(1024).decode('ascii')
            json_data = sftp.receive_data(raw_data)
            data = sftp.convert_json_to_data(json_data)

            if data["header"] == 'handshake':
                handshake = sftp.create_data('', header='handshake', sender=nickname)
                json_handshake = sftp.send_data(handshake)
                client.send(json_handshake.encode('ascii'))
            else:
                print(f"{MSG_TOKEN_DECORATOR[data['header']] if data['sender'] != nickname else Colors.BOLD}"
                      f"{data['sender'] if data['sender'] != nickname else 'Você'}: {data['body']}"
                      f"{Colors.ENDC}")

        except Exception as e:
            print(e)
            client.close()
            sys.exit()


def write() -> None:
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

    # Used to force win terminal(cmd) accept ANSI colors.
    os.system("")

    if len(sys.argv) == 3:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
    else:
        print(f"{Colors.WARNING}\n"
              "* Uso:\n"
              "> run_client.py xxx.xxx.xxx.xxx YYYY, onde:\n\n"
              "     xxx.xxx.xxx.xxx: endereço IP\n"
              f"                YYYY: porta{Colors.WARNING}")
        sys.exit()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("Tentando conectar ao servidor...")
        client.connect((host, port))

    except ConnectionRefusedError:
        print(f"\n{Colors.FAIL}Não foi possível conectar ao servidor {host}:{port}.\n"
              f"Verifique se o endereço e porta estão corretos e tente novamente.")
        client.close()
        sys.exit()

    clientui = client_ui

    setup_ui_event_handlers()

    nickname = input("Nickname: ")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
