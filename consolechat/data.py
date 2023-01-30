import json
from datetime import datetime


__all__ = ['sftp']


class Protocol:
    @staticmethod
    def send_data(json_data: dict) -> str:
        return json.dumps(json_data)

    @staticmethod
    def receive_data(bytes_data: str) -> dict:
        return json.loads(bytes_data)

    @staticmethod
    def connection_message(client_name: str) -> dict:
        _data.set_attr(f"{client_name} entrou da sala.", header="conn", sender="server")
        return _data.data

    @staticmethod
    def disconnection_message(client_name: str) -> dict:
        _data.set_attr(f"{client_name} saiu da sala.", header="disconn", sender="server")
        return _data.data

    @staticmethod
    def convert_json_to_data(json_data: dict) -> dict:
        _data.set_attr(json_data["body"], header=json_data["header"], sender=json_data["sender"])
        return _data.data

    @staticmethod
    def create_data(body: str, header: str = None, sender: str = None) -> dict:
        if header is None or sender is None:
            raise Exception('Neither \"header\" or \"sender\" can\'t be empty.')
        _data.set_attr(body, header=header, sender=sender)
        return _data.data


class Data:
    def __init__(self, *body: list, header: str = None, sender: str = None):
        self._header = header
        self._sender = sender

        self._body = body[0] if body else ''

        self._time: str = str()

    def set_attr(self, body, sender, header):
        self._body = body
        self._header = header
        self._sender = sender

        self._set_timestamp()

    def _set_timestamp(self) -> None:
        actual_time = datetime.now()
        self._time = actual_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_time(self) -> str:
        return self._time

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
        return {"time": self._time, "header": self.header, "sender": self.sender, "body": self.body}

    def __str__(self):
        return f'time: {self._time}, header: {self.header}, sender: {self.sender} , body: {self.body}'

    def __repr__(self):
        return f"Data({self._time}, {self.header}, {self.sender}, {self.body})"


'''
Create a singleton-like object of the "Data" class,
to be used internally by this module only.
'''
_data = Data()

'''
Create a singleton-like object of the "Protocol" class,
to be used externally through the app.
'''
sftp = Protocol()
