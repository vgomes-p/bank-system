from random import shuffle, sample
from string import ascii_letters, digits, ascii_lowercase, ascii_uppercase
from .chars import PUNCT, ret_puncts
from .debug import debug
from .strings import div_str, list_to_str
from .token import make_token, get_tokens, get_coord

def _gen_add(amount: int, nbr: bool=False, except_for: list=False) -> list:
    ret = []
    punct = PUNCT.copy()
    if except_for:
        for c in punct:
            if c in except_for:
                punct.remove(c)
    if nbr:
        while amount > 0:
            base = (
                sample(ascii_lowercase, k=10) +
                sample(PUNCT, k=10)
            )
            shuffle(base)
            gen = "".join(base)
            ret.append(gen[0:4])
            amount -= 1
    while amount > 0:
        base = (
            sample(ascii_letters, k=10) +
            sample(digits, k=10)
        )
        shuffle(base)
        gen = "".join(base)
        ret.append(gen[0:4])
        amount -= 1
    return ret


def _gen_chars(gen_type: str="new_chars", gen_level: str="simple", except_for: list=False, add: list=False) -> str:
    number = ["nbr", "num", "number"]
    if except_for:
        punct = [p for p in PUNCT if p not in except_for]
    else:
        punct = PUNCT.copy()
    punct_str = "".join(punct)

    if gen_level in number:
        if gen_type == "new_chars":
            while True:
                base = (
                        sample(ascii_lowercase, 10) +
                        sample(punct, 10)
                        )
                shuffle(base)
                if add:
                    for c in base:
                        if c in add:
                            base.remove(c)
                ret = "".join(base)
                if len(ret) >= 10:
                    return str(ret[0:10])
                else:
                    continue
        else:
            chars = digits
    elif gen_level == "simple":
        chars = ascii_lowercase + digits
    elif gen_level == "medium":
        chars = ascii_lowercase + digits + ascii_uppercase
    elif gen_level == "advanced":
        chars = ascii_lowercase + digits + ascii_uppercase + punct_str
    else:
        pass
    ret = []
    if gen_type == "new_chars":
        return "".join(sample(chars, len(chars)))
    return "".join(chars)


def _mixed(parts: list, add: list) -> tuple[str, list]:
    pos = []
    mixed_list = []
    cursor = 0

    for i, part in enumerate(parts):
        mixed_list.append(part)
        cursor += len(part)
        if i < len(add):
            pos.append(cursor)
            mixed_list.append(add[i])
            cursor += len(add[i])
    return list_to_str(mixed_list), pos


def _unmixed(text: str, add: list, pos: list) -> str:
    for p, a in zip(reversed(pos), reversed(add)):
        text = text[:p] + text[p + len(a):]
    return text



def _switch(text: str, new_char: list, old_char: list) -> str:
    switch_list = []
    for c in text:
        if c in old_char:
            i = old_char.index(c)
            switch_list.append(new_char[i])
        else:
            switch_list.append(c)
    return "".join(switch_list)


def _key_datas(process_type: str, except_for: list=False) -> dict:
    ret = {}
    if process_type == "number":
        add = _gen_add(10, nbr=True, except_for=except_for)
        ret["old_chars"] = _gen_chars("old_chars", "number", except_for, add)
        ret["new_chars"] = _gen_chars("new_chars", "number", except_for, add)
        ret["add"] = add
    elif process_type == "simple":
        add = _gen_add(10, except_for=except_for)
        ret["old_chars"] = _gen_chars("old_chars", "simple", except_for, add)
        ret["new_chars"] = _gen_chars("new_chars", "simple", except_for, add)
        ret["add"] = add
    elif process_type == "medium":
        add = _gen_add(10, except_for=except_for)
        ret["old_chars"] = _gen_chars("old_chars", "medium", except_for, add)
        ret["new_chars"] = _gen_chars("new_chars", "medium", except_for, add)
        ret["add"] = add
    elif process_type == "advanced":
        add = _gen_add(10, except_for=except_for)
        ret["old_chars"] = _gen_chars("old_chars", "advanced", except_for, add)
        ret["new_chars"] = _gen_chars("new_chars", "advanced", except_for, add) 
        ret["add"] = add
    else:
        debug(stats="Failed", error_text="process entered is invalid!", output=[f"process entered: {process_type}"])
        return {"failed": "invalid entry!"}
    return ret


def pos_to_str(pos: list) -> str:
    return ",".join(str(i) for i in pos)

def pos_to_int(pos: str) -> list:
    if not pos:
        return []
    return [int(x) for x in pos.split(",")]


def encrypt(text: str, key: str="simple") -> dict:
    """
    Encrypt a text string using a character-mapping and token-based scheme.

    This function transforms the input text by:
    - Dividing it into parts
    - Mixing additional generated fragments
    - Substituting characters using a generated key
    - Reversing the final result

    Alongside the encrypted text, multiple tokens are generated.
    These tokens contain all the information required to fully
    reconstruct the original text during decryption.

    :param text: The plain text to be encrypted.
    :type text: str
    :param key: Encryption complexity level. Supported values are:
                ``"number"``, ``"simple"``, ``"medium"``, ``"advanced"``.
                Higher levels increase character variety and complexity.
    :type key: str
    :return: A dictionary containing:
             - ``encrypted_text``: the encrypted output string
             - ``token_1``: mixed character-mapping token
             - ``token_2``: seed used to reconstruct the character mapping
             - ``token_3``: positional data for mixed fragments
             - ``inter``: length of injected fragments
             - ``key``: encryption level used
    :rtype: dict
    """
    many_div = {"number": 3, "simple": 4, "medium": 5, "advanced": 6}
    parts_count = many_div[key]
    if len(text) <= 12:
        parts_count = max(2, len(text) // 3)
    elif len(text) <= 24:
        parts_count = max(3, len(text) // 4)
    
    parts = div_str(text=text, times=parts_count)
    except_for = ret_puncts(text=text)
    key_type = _key_datas(process_type=key, except_for=except_for)
    add = key_type["add"][:len(parts) - 1]
    inter = len(add[0]) if add else 0
    
    new_char = key_type["new_chars"]
    old_char = key_type["old_chars"]
    
    mk_token = make_token(old_str=old_char, new_str=new_char)
    token_1 = mk_token["token"]
    token_2 = mk_token["seed"]
    
    mixed, pos = _mixed(parts, add)
    token_3 = pos_to_str(pos)
    
    final = _switch(mixed, new_char, old_char)
    final = final[::-1]
    
    return {
        "encrypted_text": final,
        "token_1": token_1,
        "token_2": token_2,
        "token_3": token_3,
        "inter": inter,
        "key": key,
    }


def decrypt(encrypted: dict) -> str:
    """
    Decrypt a text encrypted with the ``encrypt`` function.

    This function reverses the encryption process by:
    - Restoring the original character mapping using tokens
    - Undoing character substitutions
    - Removing injected fragments
    - Reassembling the original text

    The input dictionary must be the exact output produced
    by the ``encrypt`` function.

    :param encrypted: Dictionary containing encrypted text and
                      all required tokens for decryption.
    :type encrypted: dict
    :return: The original decrypted plain text.
    :rtype: str
    """
    encrypted_text = encrypted["encrypted_text"]
    token_1 = encrypted["token_1"]
    token_2 = encrypted["token_2"]
    token_3 = encrypted["token_3"]
    inter   = encrypted["inter"]

    i, e = get_coord(token_2)
    old_char, new_char = get_tokens(token_1, i, e)
    final = encrypted_text[::-1]
    mixed = _switch(final, old_char, new_char)
    pos = pos_to_int(token_3)
    real_adds = []
    for p in pos:
        real_adds.append(mixed[p:p + inter])
    unmixed = _unmixed(mixed, real_adds, pos)
    return unmixed
