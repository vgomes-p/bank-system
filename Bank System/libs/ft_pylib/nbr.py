def is_valid_number(value) -> bool:
    """
    Check whether a value can be converted to a numeric type.

    The function attempts to convert the input value to a float.
    If the conversion succeeds, the value is considered valid.

    :param value: The value to be validated.
    :return: True if the value can be converted to a float,
             False otherwise.
    :rtype: bool
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_negative_number(value) -> bool:
    """
    Check whether a value represents a negative number.
    
    The function attempts to convert the input value to a float
    and evaluates whether it is less than zero.
    
    :param value: The value to be evaluated.
    :return: True if the value is a valid number and is negative,
             False otherwise.
    :rtype: bool
    """
    try:
        return float(value) < 0
    except ValueError:
        return False