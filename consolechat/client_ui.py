from ui import UI
from decorators import Colors

from version import __version__


class ClientUI(UI):
    def __init__(self):
        super().__init__()
        self.header_title = "Chat client"

        self._INIT_WIDTH = 150
        self._INIT_HEIGHT = 40

        self.start(self._INIT_WIDTH, self._INIT_HEIGHT)

        self.update()

    def header(self):
        print(f"\n{self.header_title} {__version__}")
        print(f"{Colors.OKGREEN}Conectado!{Colors.ENDC}\n")

    def update(self):
        self._clear_screen()
        self.header()


client_ui = ClientUI()
