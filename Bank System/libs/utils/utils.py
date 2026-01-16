import os
import time
import sys

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


def there_is_punct(text, except_for: list=None) -> bool:
    punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
            '/', ':', ';' '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            '{', '|', '}', '~']
    if except_for:
        for rem in except_for:
            punct.remove(rem)
    for c in text:
        if c in punct:
            return True
        else:
            pass
    return False

def there_is_alpha(text) -> bool:
    for c in text:
        if str(c).isalpha():
            return True
        else:
            pass
    return False

def is_punct(text) -> bool:
    punct = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.',
            '/', ':', ';' '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
            '{', '|', '}', '~']
    for c in text:
        if c not in punct:
            return False
        else:
            pass
    return True

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
