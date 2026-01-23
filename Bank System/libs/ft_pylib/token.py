from .strings import div_str
from math import ceil

def tokenizator(string: str, split_char: str=" ") -> list:
    """
    Split a string into tokens based on a delimiter character.

    This function manually parses the input string and separates it
    into substrings whenever the specified split character is found.

    :param string: The string to be tokenized.
    :type string: str
    :param split_char: Character used as the token delimiter.
    :type split_char: str
    :return: A list of tokens extracted from the string.
    :rtype: list
    """
    ret = []
    word = ''
    cnt = 0
    while cnt < len(string):
        if string[cnt] == '\0':
            break
        init = cnt
        while cnt < len(string):
            if string[cnt] == '\0' or string[cnt] == split_char:
                break
            cnt += 1
        cnt += 1
        word = string[init:cnt-1]
        ret.append(word)
    return ret

def make_token(old_str: str, new_str: str) -> dict:
    """
    Create a mixed token and a seed for later reconstruction.

    This function interleaves parts of ``new_str`` and ``old_str``
    into a single token string. It also generates a seed containing
    positional information required to recover the original strings.

    :param old_str: Original string to be embedded in the token.
    :type old_str: str
    :param new_str: New string to be mixed with the original string.
    :type new_str: str
    :return: A dictionary containing:
             - ``token``: the mixed string
             - ``seed``: positional data for reconstruction
    :rtype: dict
    """
    seed_list = []
    tokens = []
    parts_old_str = div_str(old_str, ceil(len(old_str)/2))
    parts_new_str = div_str(new_str, ceil(len(new_str)/2))
    init = 0
    nbr = 0
    for p in parts_new_str:
        tokens.append(p)
        init = len("".join(tokens))
        seed_list.append(str(init))
        tokens.append(parts_old_str[nbr])
        end = len("".join(tokens))
        seed_list.append(str(end))
        nbr += 1
    seed = ".".join(seed_list)
    return {"token": "".join(tokens), "seed": seed}

def get_coord(seed: str) -> tuple[list, list]:
    """
    Extract positional coordinates from a seed string.

    The seed is expected to be a sequence of integers separated by
    dots, representing alternating start and end positions.

    :param seed: Seed string containing positional data.
    :type seed: str
    :return: A tuple containing two lists:
             - start positions
             - end positions
    :rtype: tuple[list, list]
    """
    init = []
    end = []

    buf = []
    expecting_init = True

    for ch in seed:
        if ch != '.':
            buf.append(ch)
        else:
            num = int("".join(buf))
            buf.clear()

            if expecting_init:
                init.append(num)
                expecting_init = False
            else:
                end.append(num)
                expecting_init = True
    num = int("".join(buf))
    if expecting_init:
        init.append(num)
    else:
        end.append(num)

    return init, end

    
def get_tokens(token: str, init: list, end: list) -> tuple[str, str]:
    """
    Reconstruct original strings from a mixed token and coordinates.

    Using the positional data provided by ``init`` and ``end``,
    this function separates the mixed token into two strings:
    the original embedded string and the remaining mixed content.

    :param token: The mixed token string.
    :type token: str
    :param init: List of start positions.
    :type init: list
    :param end: List of end positions.
    :type end: list
    :return: A tuple containing:
             - the reconstructed old string
             - the reconstructed new string
    :rtype: tuple[str, str]
    """
    
    token_1 = []
    token_2 = []

    last = 0
    for i, e in zip(init, end):
        token_2.append(token[last:i])
        token_1.append(token[i:e])
        last = e

    token_2.append(token[last:])
    return "".join(token_1), "".join(token_2)