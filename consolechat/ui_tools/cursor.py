class Cursor:
    def __init__(self):
        self.position_row = 0
        self.position_col = 0

    def set_cursor_position(self, row: int, col: int):
        self.position_row = row
        self.position_col = col

    def get_cursor_position(self):
        return self.position_row, self.position_col
