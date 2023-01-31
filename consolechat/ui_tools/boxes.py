import os


class Box:
    def __init__(
            self,
            title: str = None,
            title_align: str = 'right',
            title_position: str = 'inline',
            text: str = None,
            width: int = None,
            height: int = None,
            border_style: str = 'single',
            background: bool = False,
            color: str = 'black'
    ) -> None:

        # Get terminal window size
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = os.get_terminal_size()

        # Validates box size, set to terminal size if greater than terminal bounds
        self.width = width if width and width < self.TERMINAL_WIDTH else self.TERMINAL_WIDTH - 2
        self.height = height if height and height< self.TERMINAL_HEIGHT else self.TERMINAL_HEIGHT - 5

        # The box title, if any
        self.title = title
        # Set tile alignment: left, center or right
        self.title_align = title_align if title_align in ('left', 'center', 'right') else 'left'

        self.title_position = title_position if title_position in ('above', 'inline', 'below') else 'inline'

        if self.title is not None and self.title_align == 'center' and self.title_position == 'inline':
            self.corr_num = self._title_correct_lenght_char()
            self.half_len: int = 0

        # The text that will be displayed, if any
        self.text = text if text else ''

        # Set border style: single or double , default is single
        self.border_style = border_style if border_style in ('single', 'double') else 'single'

        # Bool
        self.background = background

        # Define box padding, default is 1
        self.padding = 1

        self.top_line: str = ''
        self.middle_line: str = ''
        self.bottom_line: str = ''

        # Box style chars
        if self.border_style == 'single':
            self.line = '─'
            self.column = '│'
            self.top_left = '┌'
            self.top_right = '┐'
            self.down_left = '└'
            self.down_right = '┘'
        elif self.border_style == 'double':
            self.line = '═'
            self.column = '║'
            self.top_left = '╔'
            self.top_right = '╗'
            self.down_left = '╙'
            self.down_right = '╝'

        self.bg_char = '░' if self.background else ' '

        self.colors = {
            'white': '\u001b[47m',
            'black': '\u001b[40m',
            'red': '\u001b[41m',
            'green': '\u001b[42m',
            'yellow': '\u001b[43m',
            'blue': '\u001b[44m',
            'magenta': '\u001b[45m',
            'cyan': '\u001b[46m',
            'reset': '\u001b[0m'
        }

        self.bg_color = self.colors[color] if color in self.colors else self.colors['black']
        self.bg_color_reset = self.colors['reset']

    def draw_box(self) -> None:
        if self.title is not None:
            self.half_len = int(self.width / 2) - int(len(self.title) / 2) - 2
            if self.title_align == 'left':
                self.top_line = f' {self.top_left}{self.line * 4} {self.title} {self.line * (self.width - len(self.title) - 8)}{self.top_right}'
            elif self.title_align == 'center':
                self.top_line = f' {self.top_left}{self.line * self.half_len} {self.title} {self.line * (self.half_len - self.corr_num)}{self.top_right}'
            elif self.title_align == 'right':
                self.top_line = f' {self.top_left}{self.line * (self.width - len(self.title) - 8)} {self.title} {self.line * 4}{self.top_right}'
        else:
            self.top_line = f' {self.top_left}{self.line * (self.width - 2)}{self.top_right}'
        self.middle_line = f' {self.column}{self.bg_color}{self.bg_char * (self.width - 2)}{self.bg_color_reset}{self.column}'
        self.bottom_line = f' {self.down_left}{self.line * (self.width - 2)}{self.down_right}'

        print(self.top_line)
        for x in range(self.height):
            print(self.middle_line)
        print(self.bottom_line)
        message = f'Oiiiii gente, como vai?'
        print(f'\u001b[{self.height}A\u001b[3C{message}')
        print(f'\u001b[{self.height}B')

    def _title_correct_lenght_char(self) -> int:
        corr = 0
        if (self.width + len(self.title)) % 2 != 0:
            if len(self.title) % 2 == 0:
                corr = - 1
            else:
                corr = 1
        return corr


os.system('')
box = Box(title='CAIXA DE TEXTO DA THAIS', title_align='left', border_style='single', height=20, color='white')

box.draw_box()
