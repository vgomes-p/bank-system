from time import sleep
import os

def clear(init_wait_time: int=0, final_wait_time: int=0):
    """
    Clear the terminal screen with optional delays.
    
    This function pauses execution for an optional amount of time
    before clearing the terminal, clears the screen using the
    appropriate command for the current operating system, and
    optionally pauses again after clearing.

    :param init_wait_time: Time in seconds to wait before clearing
                           the terminal.
    :type init_wait_time: int
    :param final_wait_time: Time in seconds to wait after clearing
                            the terminal.
    :type final_wait_time: int
    :return: None
    :rtype: None
    """
    sleep(float(init_wait_time))
    os.system("cls" if os.name == "nt" else "clear")
    sleep(float(final_wait_time))