import os
import time
import sys

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


def clear(init_wait_time=0, final_wait_time=0):
    '''Clean the terminal's screen'''
    time.sleep(float(init_wait_time))
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(float(final_wait_time))


def is_valid_number(value):
    '''Check's if a number is valid'''
    try:
        float(value)
        return True
    except ValueError:
        return False


def press_enter():
    '''Prevent user from using/typing anything until the type enter'''
    if os.name == "nt":
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b"\r":
                    break
            time.sleep(0.01)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == "\r" or ch == "\n":
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def is_negative_number(value):
    '''Checks if a number is negative'''
    try:
        return float(value) < 0
    except ValueError:
        return False
