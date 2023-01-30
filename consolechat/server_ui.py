import sys

from ui import UI
from logger import log
from clients import clients_database
from decorators import Colors, separator

from version import __version__


HEADER_TITLE = "Chat server"
INIT_WIDTH = 150
INIT_HEIGHT = 40


class ServerUI(UI):
    def __init__(self):
        super().__init__()
        self.header_title = HEADER_TITLE

        self.host = str(sys.argv[1])
        self.port = int(sys.argv[2])

        self._WIDTH = INIT_WIDTH
        self._HEIGHT = INIT_HEIGHT

        # start the server
        self.start(self._WIDTH, self._HEIGHT)

        self.update()

    def header(self):
        print(f"{self.header_title} {__version__}\n")
        print(f"{Colors.OKGREEN}* Conectado em {self.host}:{self.port}{Colors.ENDC}")
        print(f"* Usuários conectados: {len(clients_database)}")
        separator(64)

    @staticmethod
    def active_clients():
        columns = [' #', 'Name', 'IP']
        print(f'{columns[0]} | {columns[1]:<40} | {columns[2]}')
        for index, client in enumerate(clients_database.active_clients()):
            print(f'{index + 1:2} | {client.name:<40} | {client.addr[0]}:{client.addr[1]}')
        separator(64)

    @staticmethod
    def print_log_events(max_to_show=5):
        print("\nEvents log (last 10):")
        filtered_list = [e for e in log.get_log_events if e["header"] != "msg"]
        for event in filtered_list[-max_to_show:]:
            print(f"{Colors.WARNING}{event}{Colors.ENDC}")

    @staticmethod
    def print_log_messages(max_to_show=4):
        print("\nMessages log (last 10):")
        filtered_list = [e for e in log.get_log_events if e["header"] == "msg"]
        for message in filtered_list[-max_to_show:]:
            print(message)

    def update(self):
        self._clear_screen()
        self.header()
        self.active_clients()
        self.print_log_events(max_to_show=10)
        self.print_log_messages(max_to_show=10)


server_ui = ServerUI()
