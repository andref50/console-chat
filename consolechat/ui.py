import os


class UI:
    """
    Defines the ui used by the server_ui and client_ui classes.
    """

    def __init__(self):
        self.width = int()
        self.height = int()
        self.color = str()
        self.opr_sys = os.name
        self.os_commands = {}
        self.header_title = str()

        self._set_opsys()

    def _set_opsys(self):
        if self.opr_sys == 'nt':
            self.os_commands = {
                'CLEAR_SCREEN': 'cls'
            }
        else:
            self.os_commands = {
                'CLEAR_SCREEN': 'clear'
            }

    def _set_ui(self, width, height):
        self.width, self.height = width, height

        # set console size (x, y)
        cmd = f'mode {self.width},{self.height}'
        os.system(cmd)

    def _clear_screen(self):
        os.system(self.os_commands['CLEAR_SCREEN'])

    def start(self, width, height):
        self._set_ui(width, height)

    def header(self):
        pass

    def update(self):
        pass
