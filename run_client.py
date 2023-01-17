import os
import sys
import socket
import threading

if len(sys.argv) == 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    print("Usar argumentos: host (no formato '127.0.0.1') e porta (int)")
    sys.exit()

opr_sys = os.name
if opr_sys == 'nt':
    plat_commands = {
        'CLEAR_SCREEN': 'cls'
    }
else:
    plat_commands = {
        'CLEAR_SCREEN': 'clear'
    }

os.system(plat_commands['CLEAR_SCREEN'])

nickname = input("Nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f"Erro de conexão: {e}")
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
