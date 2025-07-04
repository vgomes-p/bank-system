import os
import time as tm
import sys
if os.name == 'nt':
	import msvcrt
else:
	import termios
	import tty

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_number(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def press_enter():
	if os.name == 'nt':
		while True:
			if msvcrt.kbhit():
				key = msvcrt.getch()
				if key == b'\r':
					break
			tm.sleep(0.01)
	else:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			while True:
				ch = sys.stdin.read(1)
				if ch == '\r' or ch == '\n':
					break
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)