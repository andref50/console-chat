import os
from utils.utils import separator


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

    def _set_ui(self, header_title, width, height, color):
        self.header_title, self.width, self.height, self.color = header_title, width, height, color

        # set console size (x, y)
        cmd = f'mode {self.width},{self.height}'
        os.system(cmd)

        # set console color (ANSI)
        color = f'color {self.color}'
        os.system(color)

    def start(self, header_title, width, height, color):
        self._set_opsys()
        self._set_ui(header_title, width, height, color)

    def clear_screen(self):
        os.system(self.os_commands['CLEAR_SCREEN'])

    def header(self, ):
        pass
