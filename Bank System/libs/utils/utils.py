import os
import time
import sys

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty

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
