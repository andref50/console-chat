from ctypes import *
import os

STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    _fields_ = [("x", c_short), ("y", c_short)]


def print_at(r, c, s):
    os.system('cls')
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("windows-1252")
    windll.kernel32.WriteConsoleA(h, c_char_p(c), len(c), None, None)


print_at(5, 20, "Hellor")
