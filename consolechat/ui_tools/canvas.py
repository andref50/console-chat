import os


class ElementNotFitCanvas(Exception):
    """ Element too big for this canvas """
    def __init__(self, element_id):
        self.element_id = element_id

    def __str__(self):
        return f'The {self.element_id} element is too big to fit this canvas'


class ElementAlreadyInCanvas(Exception):
    """ Element too big for this canvas """
    def __init__(self, element_id):
        self.element_id = element_id

    def __str__(self):
        return f'The {self.element_id} was already added in canvas'


class ElementNotInCanvas(Exception):
    """ Element too big for this canvas """
    def __init__(self, element_id):
        self.element_id = element_id

    def __str__(self):
        return f'The {self.element_id} is not in canvas'


class Canvas:
    def __init__(self, width: int = None, height: int = None) -> None:

        # Get terminal window size
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = os.get_terminal_size()

        # Validates box size, set to terminal size if greater than terminal bounds
        self.width = width if width and width < self.TERMINAL_WIDTH else self.TERMINAL_WIDTH - 2
        self.height = height if height and height< self.TERMINAL_HEIGHT else self.TERMINAL_HEIGHT - 5

        self.elements = []

    def add_element(self, element):
        if element not in self.elements:
            try:
                self._check_element_size(element)
            except ElementNotFitCanvas:
                print(ElementNotFitCanvas(element.id))
            self.elements.append(element)
        else:
            raise ElementAlreadyInCanvas(element.id)

    def remove_element(self, element):
        if element not in self.elements:
            raise ElementNotInCanvas(element.id)
        self.elements.remove(element)

    def get_elements(self):
        return self.elements

    def _check_element_size(self, element) -> bool:
        if element.width > self._free_width() or element.height > self._free_height():
            raise ElementNotFitCanvas(element.id)
        return True

    def _free_width(self) -> int:
        return self.width - self._occupied_width()

    def _free_height(self) -> int:
        return self.height - self._occupied_height()

    def _occupied_width(self) -> int:
        return sum([element.width for element in self.elements])

    def _occupied_height(self) -> int:
        return sum([element.height for element in self.elements])
