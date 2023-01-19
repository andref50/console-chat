import os


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
    'msg': colors.OKBLUE
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
