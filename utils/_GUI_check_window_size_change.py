import os

MIN_WIDTH = 60
MIN_HEIGHT = 30


def check_size_change():
    width = MIN_WIDTH
    height = MIN_HEIGHT
    cmd = f'mode {width}, {height}'
    os.system(cmd)
    while True:
        size = os.get_terminal_size()
        if size[0] != width or size[1] != height:
            if size[0] < MIN_WIDTH:
                os.system(f'mode {MIN_WIDTH}, {size[1]}')
            elif size[1] < MIN_HEIGHT:
                os.system(f'mode {size[0]}, {MIN_HEIGHT}')
            os.system('cls')
            print('changed')
            print(f'{size[0] = }, {size[1] = }')
            width = size[0]
            height = size[1]


check_size_change()
