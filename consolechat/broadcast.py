from clients import clients_database


def broadcast(data: str) -> None:
    for c in clients_database.active_clients():
        c.client.sendall(data.encode('ascii'))
