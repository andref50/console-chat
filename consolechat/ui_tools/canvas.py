import os


class Canvas:
    def __init__(self, width: int = None, height: int = None) -> None:

        # Get terminal window size
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = os.get_terminal_size()

        # Validates box size, set to terminal size if greater than terminal bounds
        self.width = width if width and width < self.TERMINAL_WIDTH else self.TERMINAL_WIDTH
        self.height = height if height and height< self.TERMINAL_HEIGHT else self.TERMINAL_HEIGHT - 1

        self.elements = []
        self.buffer = []

        self.clear_buffer()

    def gotoxy(self, col, row):
        return self.buffer[row][col]

    def print_at_buffer(self, char, col, row):
        self.buffer[row][col] = char

    def add_element(self, element):
        if element not in self.elements:
            max_x_pos = self.width - element.width
            max_y_pos = self.height - element.height - 2

            element.x = min(element.x, max_x_pos)
            element.y = min(element.y, max_y_pos)
            self.elements.append(element)

    def remove_element(self, element):
        if element in self.elements:
            self.elements.remove(element)

    def clear_buffer(self):
        self.buffer = list(['.' for _ in range(self.width)] for _ in range(self.height))

    def draw_to_buffer(self, element):
        for row in range(len(element.box)):
            for col in range(len(element.box[row])):
                self.buffer[row + element.y][col + element.x] = element.box[row][col]

    def update(self):
        self.clear_buffer()
        for e in self.elements:
            self.draw_to_buffer(e)

    def draw(self):
        self.update()
        print(''.join(j for i in self.buffer for j in i))


canvas = Canvas()
