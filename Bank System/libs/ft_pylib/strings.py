from math import ceil
from time import sleep


def letterby(entry: str, timer: float=0.05, end='\n'):
    """
    Print a string to the terminal one character at a time.

    This function simulates a typing effect by progressively printing
    the input string to stdout with a delay between each character.

    :param entry: The text to be printed character by character.
    :type entry: str
    :param timer: Delay in seconds between each printed character.
    :type timer: float
    :param end: String appended after the final output.
    :type end: str
    :return: None
    :rtype: None
    """
    cnt = 0
    while cnt <= len(entry):
        nw_str = entry[0:cnt]
        print(f'\r{nw_str}|', end='', flush=True)
        sleep(timer)
        cnt += 1
    print(f'\r{entry} ', end=end, flush=True)


def div_str(text: str, times: int) -> list:
    """
    Divide a string into a specified number of parts.

    The string is split into ``times`` parts of approximately equal
    size. The final part may contain fewer characters depending on
    the string length.

    :param text: The text to be divided.
    :type text: str
    :param times: Number of parts to divide the string into.
    :type times: int
    :return: A list containing the divided string parts.
    :rtype: list
    """
    ret = []
    text_len = len(text)
    parts_size = ceil(text_len / times)
    text_part = ""
    init_cut = 0
    final_cut = parts_size
    while times != 1:
        text_part = text[init_cut:final_cut]
        init_cut = final_cut
        final_cut += parts_size
        ret.append(text_part)
        times -= 1
    text_part = text[init_cut:]
    ret.append(text_part)
    return ret


def split_by(text: str, nbr: int) -> list:
    """
    Split a string into chunks of a fixed size.

    The function iterates through the string and splits it into
    substrings containing ``nbr`` characters each.

    :param text: The text to be split.
    :type text: str
    :param nbr: Number of characters per chunk.
    :type nbr: int
    :return: A list of substrings split by the specified size.
    :rtype: list
    """
    cnt = len(text)
    ret = []
    i = 0
    e = nbr
    while cnt != nbr:
        splited_by = text[i:e]
        i = e
        e += nbr
        ret.append(splited_by)
        cnt -= nbr
    return ret


def str_to_list(text: str) -> list:
    """
    Convert a string into a list of characters.

    :param text: The string to be converted.
    :type text: str
    :return: A list where each element is a character from the string.
    :rtype: list
    """
    ret = []
    for c in text:
        ret.append(c)
    return ret

def list_to_str(entry_list: list) -> str:
    """
    Convert a list of characters into a string.

    :param entry_list: A list of characters to be joined.
    :type entry_list: list
    :return: A string formed by joining all list elements.
    :rtype: str
    """
    return "".join(entry_list)