import os
from canvas import Canvas

UNICODE_ARROWS = '←↑→↓↔↕↨'

# Define box constants
BORDER_STYLE = ('single', 'double', 'dash', 'dot')
TITLE_H_ALIGNMENT = ('left', 'center', 'right')


def first(elements):
    return elements[0]


class Widget:
    def __init__(self, name: str, canvas: Canvas, width: int = None, height: int = None, px: int = 0, py: int = 0):

        self.name = name
        self.canvas = canvas

        self.min_width = 4
        self.min_height = 4

        self.max_width = self.canvas.width
        self.max_height = self.canvas.height - 2

        # Validates box size, set to terminal size if greater than terminal bounds
        self.width = min(max(width, self.min_width), self.max_width) if width is not None else self.max_width
        self.height = min(max(height, self.min_height), self.max_height) if height else self.max_height

        self.x: int = px
        self.y: int = py

    def area(self):
        return self.x + 1, self.y + 1, self.width - 1, self.height - 1


class Box(Widget):
    def __init__(self, name, canvas, border_style: str = 'single', **kwds) -> None:
        super().__init__(name, canvas, **kwds)

        self.box: list = []

        self.top_line: list = []
        self.middle_line: list = []
        self.bottom_line: list = []

        # Set border style: single or double , default is single
        self.border_style: str = border_style if border_style in BORDER_STYLE else first(BORDER_STYLE)

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
            self.down_left = '╚'
            self.down_right = '╝'
        elif self.border_style == 'dash':
            self.line = '-'
            self.column = '|'
            self.top_left = '+'
            self.top_right = '+'
            self.down_left = '+'
            self.down_right = '+'
        elif self.border_style == 'dot':
            self.line = '.'
            self.column = '.'
            self.top_left = '.'
            self.top_right = '.'
            self.down_left = '.'
            self.down_right = '.'

        # Define a ASCII code dict() for background color and text color
        self.bg_colors = {
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
        self.text_colors = {
            'black': '\u001b[30m',
            'red': '\u001b[31;1m',
            'green': '\u001b[32;1m',
            'yellow': '\u001b[33;1m',
            'blue': '\u001b[34;1m',
            'magenta': '\u001b[35;1m',
            'cyan': '\u001b[36;1m',
            'white': '\u001b[37;1m',
            'reset': '\u001b[0m',
            'bold': '\u001b[1m',
            'underline': '\u001b[4m'
        }

        self.text_color: str = str()
        self.box_color: str = str()
        self.color_reset = self.bg_colors['reset']
        self.colors = (self.text_color, self.box_color, self.color_reset)

    def print_at(self, text, row, col):
        max_row = min(row, self.canvas.height)
        max_col = min(col + len(text), self.canvas.width)

        for i in range(len(text)):
            self.box[max_row][max_col + i] = text[i]

    def _draw_box(self) -> None:
        pass


class TitledBox(Box):
    def __init__(self,
                 name: str,
                 canvas: Canvas,
                 title: str = None,
                 title_padding: int = 0,
                 title_h_align: str = 'right',
                 width: int = None,
                 **kwds
                 ):
        super().__init__(name, canvas, **kwds)

        self.title_padding = title_padding
        self.title = f'{" " * self.title_padding}{title}{" " * self.title_padding}'

        self.min_width = len(self.title) + 12
        self.width = min(max(width, self.min_width), self.max_width) if width is not None else self.max_width

        # Set horizontal and vertical title alignment
        self.title_h_align = title_h_align if title_h_align in TITLE_H_ALIGNMENT else first(TITLE_H_ALIGNMENT)

        self.draw_box()

    def draw_box(self) -> None:
        self.top_line = list(self.top_left + self.line * (self.width - 2) + self.top_right)
        self.middle_line = list(self.column + ' ' * (self.width - 2) + self.column)
        self.bottom_line = list(self.down_left + self.line * (self.width - 2) + self.down_right)

        self.box = [self.top_line] + ([self.middle_line] * self.height) + [self.bottom_line]

        half_len = self.width // 2 - (len(self.title) // 2) - 2

        if self.title_h_align == 'left':
            for i, c in enumerate(self.title):
                self.top_line[i + 4] = c

        elif self.title_h_align == 'center':
            for i, c in enumerate(self.title):
                self.top_line[i + half_len] = c

        elif self.title_h_align == 'right':
            for i, c in enumerate(self.title[::-1]):
                self.top_line[-i + ~4] = c

    def _update(self):
        self._draw_box()


os.system('cls')

app_canvas = Canvas()

box = TitledBox(
    name='caixa-de-texto1',
    canvas=app_canvas,
    title='BATE PAPO UOL',
    title_padding=1,
    title_h_align='left',
    border_style='double',
    height=8,
    width=80,
    py=20
    )

box2 = TitledBox(
    name='caixa-de-texto2',
    canvas=app_canvas,
    title='BATE PAPO UOL',
    title_padding=1,
    title_h_align='center',
    border_style='single',
    height=8,
    width=80,
    px=50
    )


app_canvas.add_element(box)
app_canvas.add_element(box2)
app_canvas.draw()


