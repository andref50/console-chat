import os
from cursor import Cursor
from text import Text


UNICODE_ARROWS = '←↑→↓↔↕↨'

# Define box constants
BORDER_STYLE = ('single', 'double', 'dash', 'dotted')
TITLE_H_ALIGNMENT = ('left', 'center', 'right')
TITLE_V_ALIGNMENT = ('above', 'inline', 'below')


class Box:
    def __init__(
            self,
            name: str,
            title: str = None,
            title_padding: int = 0,
            title_h_align: str = 'right',
            title_v_align: str = 'inline',
            text_color: str = 'white',
            width: int = None,
            height: int = None,
            border_style: str = 'single',
            background_char: bool = False,
            box_color: str = 'black'
    ) -> None:

        self.id = name

        self.has_title = True if title is not None else False

        self.title_padding = title_padding

        # Box title string, if exists
        self.title: str = f'{" " * self.title_padding}{title}{" " * self.title_padding}'

        # Get terminal window size
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = os.get_terminal_size()

        self.min_height = 4
        self.min_width = 4 if not self.has_title else self._title_len() + 12

        # Validates box size, set to terminal size if greater than terminal bounds
        if not width:
            self.width = self.TERMINAL_WIDTH - 2
        else:
            self.width = width if width > self.min_width else self.min_width

        if not height:
            self.height = self.TERMINAL_HEIGHT - 5
        else:
            self.height = height if self.min_height <= height else 4

        # Create the cursor object that holds cursor position
        self.cursor = Cursor()

        # Set horizontal and vertical title alignment
        self.title_h_align = title_h_align if title_h_align in TITLE_H_ALIGNMENT else TITLE_H_ALIGNMENT[0]
        self.title_v_align = title_v_align if title_v_align in TITLE_V_ALIGNMENT else TITLE_V_ALIGNMENT[0]

        if (
                self.title is not None
                and self.title_h_align == 'center'
                and self.title_v_align == 'inline'
        ):
            self.corr_num = self._title_correct_lenght_char()
            self.half_len = 0

        # Set border style: single or double , default is single
        self.border_style: str = border_style if border_style in BORDER_STYLE else BORDER_STYLE[0]

        # Bool
        self.background = background_char

        # Define box padding, default is 0
        # Not in use for now
        self.padding = 0

        # Create a list of events to display
        self.events = []

        # Define a negative number used for slicing "self._text_elements" list
        # The number is limited by box height
        self._limit_events_to_display = - (self.height - 2)

        # Define box body variables
        self.top_line = ''
        self.middle_line = ''
        self.bottom_line = ''

        # Not in use for now
        self.has_list_mark = True

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
        elif self.border_style == 'dotted':
            self.line = '.'
            self.column = '.'
            self.top_left = '.'
            self.top_right = '.'
            self.down_left = '.'
            self.down_right = '.'

        self.bg_char = '░' if self.background else ' '

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

        if text_color and text_color in self.text_colors:
            self.text_color = self.text_colors[text_color]
        else:
            self.text_color = self.text_colors['white']

        if box_color and box_color in self.bg_colors:
            self.bg_color = self.bg_colors[box_color]
        else:
            self.bg_color = self.bg_colors['black']

        self.color_reset = self.bg_colors['reset']

        # Create the box using setted parameters
        self._create_box()

    def _title_len(self):
        return len(self.title)

    def _create_box(self) -> None:
        if self.has_title:
            self.half_len = int(self.width / 2) - int(len(self.title) / 2) - 2

            if self.title_h_align == 'left':
                self.top_line = f' {self.top_left}' \
                                f'{self.line * 4}' \
                                f'{self.title}' \
                                f'{self.line * (self.width - len(self.title) - 6)}' \
                                f'{self.top_right}'

            elif self.title_h_align == 'center':
                self.top_line = f' {self.top_left}' \
                                f'{self.line * self.half_len}' \
                                f'{self.title}' \
                                f'{self.line * (self.half_len - self.corr_num)}' \
                                f'{self.top_right}'

            elif self.title_h_align == 'right':
                self.top_line = f' {self.top_left}' \
                                f'{self.line * (self.width - len(self.title) - 6)}' \
                                f'{self.title}' \
                                f'{self.line * 4}' \
                                f'{self.top_right}'
        else:
            self.top_line = f' {self.top_left}' \
                            f'{self.line * (self.width - 2)}' \
                            f'{self.top_right}'

        self.middle_line = f' {self.column}' \
                           f'{self.bg_color}' \
                           f'{self.bg_char * (self.width - 2)}' \
                           f'{self.color_reset}' \
                           f'{self.column}'

        self.bottom_line = f' {self.down_left}' \
                           f'{self.line * (self.width - 2)}' \
                           f'{self.down_right}'

    def _title_correct_lenght_char(self) -> int:
        corr = 0
        if (self.width + len(self.title)) % 2 != 0:
            if len(self.title) % 2 == 0:
                corr = - 1
            else:
                corr = 1
        return corr

    def _print_at(self, text: str, row: int = 1, col: int = 1) -> None:
        self.cursor.set_cursor_position(row, col)
        cursor_position = f'\033[{row};{col}H'
        print(f'{self.bg_color}{self.text_color}{cursor_position}{text}{self.color_reset}')

    def _goto(self, row: int = 1, col: int = 1):
        self.cursor.set_cursor_position(row, col)
        return print(f'\033[{row};{col}H')

    def draw(self) -> None:
        print(self.top_line)
        print(' \n'.join(self.middle_line for _ in range(self.height)))
        print(self.bottom_line)
        print()

    def set_padding(self, padding: int) -> None:
        self.padding = padding

    def _len_events(self):
        return len(self.events)

    def _create_event_text_object(self, text: str) -> object:
        text_object = Text(text, self.text_color, self.bg_color)
        return text_object

    def add_text_event(self, text: str):
        text_object = self._create_event_text_object(text)
        self.events.append(text_object)

    def _remainaing_events(self) -> object:
        remaining_messages_to_show = len(self.events) - self.height + 3
        text_object = self._create_event_text_object(f'↑(+{remaining_messages_to_show} events)')
        return text_object

    def render_events(self):
        if len(self.events) > self.height - 3:
            events_to_display = self.events[self._limit_events_to_display + 1:]
            _remaining_events_label = self._remainaing_events()
            _remaining_events_label.text_color = self.text_colors['blue']
            events_to_display.insert(0, _remaining_events_label)
        else:
            events_to_display = self.events.copy()

        for row, event in enumerate(events_to_display):
            cursor_position = f'\033[{3 + row};{5}H'
            print(f'{event.bg_color}{event.text_color}{cursor_position}{event.text}{self.color_reset}\n')

        # TEMPORARY, WILL BE REMOVED
        self._goto(row=self.height + 2, col=0)


os.system('cls')

box = Box(
    'caixa-de-texto1',
    title='BATE PAPO UOL',
    # title_padding=2,
    title_h_align='left',
    border_style='double',
    height=8,
    # width=50,
    box_color='white',
    text_color='black',
)

box.draw()
box.set_padding(2)
box.add_text_event('1')
box.add_text_event('2')
box.add_text_event('3')
box.add_text_event('4')
box.add_text_event('oieeeeeee')
box.add_text_event('6')
box.add_text_event('7')
box.add_text_event('oieeeeeee')
box.add_text_event('9')
box.add_text_event('10')

box.render_events()
