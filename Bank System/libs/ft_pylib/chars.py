PUNCT = ['!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.',
            '/', ':', ';' '<', '=', '>', '?', '@', '[', ']', '^', '_', '`',
            '{', '|', '}', '~']

def there_is_punct(text: str, except_for: list=None) -> bool:
    """
    Check whether a string contains any punctuation character.

    By default, the function checks against all characters defined in
    the global ``PUNCT`` list. Specific characters can be excluded
    from the check using the ``except_for`` parameter.
    
    Punctuations in PUNCT: !#$%&()*+,-.,/:; <=>?@[]^_`,{|}~

    :param text: The text to be analyzed.
    :type text: str
    :param except_for: A list of punctuation characters to ignore.
                       If None, all punctuation characters are considered.
    :type except_for: list | None
    :return: True if at least one punctuation character is found,
             False otherwise.
    :rtype: bool
    """
    punct = PUNCT.copy()
    if except_for:
        for rem in except_for:
            punct.remove(rem)
    for c in text:
        if c in punct:
            return True
        else:
            pass
    return False


def ret_puncts(text: str) -> list:
    """
    Return all punctuation characters found in a string.

    The function scans the input text and collects every character
    that matches one of the characters defined in ``PUNCT``.

    Punctuations in PUNCT: !#$%&()*+,-.,/:; <=>?@[]^_`,{|}~
    
    :param text: The text to be analyzed.
    :type text: str
    :return: A list containing all punctuation characters found
             in the text, in their original order.
    :rtype: list
    """
    punct = PUNCT.copy()
    ret = []
    for c in text:
        if c in punct:
            ret.append(c)
        else:
            pass
    return ret



def there_is_alpha(text: str) -> bool:
    """
    Check whether a string contains at least one alphabetic character.

    Alphabetic characters are determined using ``str.isalpha()``.

    :param text: The text to be analyzed.
    :type text: str
    :return: True if at least one alphabetic character is found,
             False otherwise.
    :rtype: bool
    """
    for c in text:
        if str(c).isalpha():
            return True
        else:
            pass
    return False


def is_punct(text: str) -> bool:
    """
    Check whether a string is composed exclusively of punctuation characters.

    The function returns True only if **all** characters in the string
    are present in the ``PUNCT`` list.

    Punctuations in PUNCT: !#$%&()*+,-.,/:; <=>?@[]^_`,{|}~

    :param text: The text to be analyzed.
    :type text: str
    :return: True if all characters are punctuation characters,
             False otherwise.
    :rtype: bool
    """
    punct = PUNCT.copy()
    for c in text:
        if c not in punct:
            return False
        else:
            pass
    return True