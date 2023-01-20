import json


class DataProtocol:
    @staticmethod
    def send_data(raw_data):
        return json.dumps(raw_data)

    @staticmethod
    def receive_data(json_data):
        return json.loads(json_data)

    @staticmethod
    def connection_data(client_name):
        return Data(f"{client_name} entrou da sala.", header="conn", sender="server").data

    @staticmethod
    def disconnection_data(client_name):
        return Data(f"{client_name} saiu da sala.", header="disconn", sender="server").data

    @staticmethod
    def make_data(data):
        return Data(data["body"], header=data["header"], sender=data["sender"])


class Data(object):
    def __init__(self, *body: str, header: str = None, sender: str = None):
        if header is None or sender is None:
            raise Exception('data object cant be empty')
        else:
            self._header = header
            self._sender = sender
        if body:
            self._body = body[0]
        else:
            self._body = ''

    @property
    def header(self):
        return self._header

    @property
    def sender(self):
        return self._sender

    @property
    def body(self):
        return self._body

    @property
    def data(self):
        return self.__str__()

    def __str__(self):
        return {"header": self.header, "sender": self.sender, "body": self.body}

    def __repr__(self):
        return f"Data({self.header}, {self.sender}, {self.body})"
