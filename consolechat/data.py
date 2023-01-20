import json


class Protocol:
    @staticmethod
    def send_data(json_data: dict) -> str:
        return json.dumps(json_data)

    @staticmethod
    def receive_data(bytes_data: str) -> dic:
        return json.loads(bytes_data)

    @staticmethod
    def connection_data(client_name: str) -> dict:
        _data.set_attr(f"{client_name} entrou da sala.", header="conn", sender="server")
        return _data.data

    @staticmethod
    def disconnection_data(client_name: str) -> dict:
        _data.set_attr(f"{client_name} saiu da sala.", header="disconn", sender="server")
        return _data.data

    @staticmethod
    def convert_json_to_data(json_data: dict) -> dict:
        _data.set_attr(json_data["body"], header=json_data["header"], sender=json_data["sender"])
        return _data.data

    @staticmethod
    def create_data(body: str, header: str = None, sender: str = None) -> dict:
        if header is None or sender is None:
            raise Exception('data object cant be empty')
        _data.set_attr(body, header=header, sender=sender)
        return _data.data


class Data:
    def __init__(self, body: list = '', header: str = None, sender: str = None):
        self._header = header
        self._sender = sender
        if body:
            self._body = body[0]
        else:
            self._body = ''

    def set_attr(self, body, sender, header):
        self._body = body
        self._header = header
        self._sender = sender

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
        return {"header": self.header, "sender": self.sender, "body": self.body}

    def __str__(self):
        return f'header: {self.header}, sender: {self.sender} , body: {self.body}'

    def __repr__(self):
        return f"Data({self.header}, {self.sender}, {self.body})"


_data = Data()
sftp = Protocol()
