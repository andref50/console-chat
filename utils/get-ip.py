import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print(f"Computer name: {hostname}\nComputer adress: {IPAddr}")