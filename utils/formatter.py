"""Module for formatting"""

def format_percentage(value):
    """Gets a decimal value and returns it formmated in percentage with comma separator
    for decimals"""
    if (100 * value).is_integer():
        return str(int(value * 100)) + '%'
    return str(round(value * 100, 1)).replace('.', ',') + "%" # pragma: no cover

def format_miliseconds(value):
    """Gets a decimal value and returns it formmated in miliseconds format_miliseconds"""
    if not value:
        return 'no delay'
    return str(value * 1000)+'ms delay'
