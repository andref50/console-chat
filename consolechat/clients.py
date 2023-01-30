__all__ = ['clients_database']


class ClientsDatabase:
    def __init__(self):
        self._clients = []

    def add_client(self, client: object) -> None:
        self._clients.append(client)

    def remove_client(self, client: object) -> None:
        self._clients.remove(client)

    def active_clients(self) -> list:
        return self._clients

    def __len__(self):
        return len(self._clients)


clients_database = ClientsDatabase()
