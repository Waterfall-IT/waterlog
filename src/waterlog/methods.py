def to_fixed(value: float, ndigits: int = 0) -> str:

    if ndigits < 0:
        return str(round(round(value, ndigits)))
    
    if ndigits == 0:
        return str(round(value))
    
    str_value = str(round(value, ndigits))
    return str_value + '0' * (ndigits - len(str_value.split('.')[1]))