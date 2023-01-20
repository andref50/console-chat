import os

from version import __version__


def separator(size):
    print('-' * size)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


MSG_TOKEN_DECORATOR = {
    'conn': colors.WARNING,
    'disconn': colors.FAIL,
    'msg': colors.ENDC
}


class UI:
    def __init__(self):
        self.width = int()
        self.height = int()
        self.color = str()
        self.opr_sys = os.name
        self.os_commands = {}
        self.header_title = str()

    def _set_opsys(self):
        if self.opr_sys == 'nt':
            self.os_commands = {
                'CLEAR_SCREEN': 'cls'
            }
        else:
            self.os_commands = {
                'CLEAR_SCREEN': 'clear'
            }

    def _set_ui(self, width, height, color=None):
        #self.color = color
        self.width, self.height = width, height

        # set console size (x, y)
        cmd = f'mode {self.width},{self.height}'
        os.system(cmd)

        # set console color (ANSI)
        # color = f'color {self.color}'
        # os.system(color)

    def start(self, width, height, color=None):
        self._set_opsys()
        self._set_ui(width, height)

    def _clear_screen(self):
        os.system(self.os_commands['CLEAR_SCREEN'])

    def header(self, ):
        pass


class ServerUI(UI):
    def __init__(self, running_server):
        super().__init__()
        self.server = running_server
        self.header_title = "Chat server"

    def header(self):
        # ascii_banner = pyfiglet.figlet_format("CHAT SERVER")
        # print(ascii_banner)
        print(f"{self.header_title} {__version__}\n")
        print(f"{colors.OKGREEN}* Conectado em {self.server.host}:{self.server.port}{colors.ENDC}")
        print(f"* Usuários conectados: {len(self.server.clients)}")
        separator(64)

    def active_clients(self):
        columns = [' #', 'Name', 'IP']
        print(f'{columns[0]} | {columns[1]:<40} | {columns[2]}')
        for index, client in enumerate(self.server.clients):
            print(f'{index + 1:2} | {client.name:<40} | {client.addr[0]}:{client.addr[1]}')
        separator(64)

    def print_log_events(self):
        print("\nEvents log (last 10):")
        for event in self.server.logger.get_log_events[-10:]:
            print(f"{colors.WARNING}{event}{colors.ENDC}")

    def print_log_messages(self):
        print("\nMessages log (last 10):")
        for message in self.server.logger.get_log_messages[-10:]:
            print(message)

    def update(self):
        self._clear_screen()
        self.header()
        self.active_clients()
        self.print_log_events()
        self.print_log_messages()


class ClientUI(UI):
    def __init__(self):
        super().__init__()
        self.header_title = "Chat client"

    def header(self):
        print(f"\n{self.header_title} {__version__}")
        print(f"{colors.OKGREEN}Conectado!{colors.ENDC}\n")

    def update(self):
        self._clear_screen()
        self.header()