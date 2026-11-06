from typing import Callable, Iterable, Optional

def ft_filter(function: Callable | None, iterable: Iterable) -> Iterable:
    '''
ft_filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.
    '''
    '! thieu dieu kien neu arg1 la None'
    ret = (x for x in iterable if function(x))
    return ret

def is_even(n):
    return n % 2 == 0

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

ret = list(filter(None, numbers))

print(f'Result is: {ret}')

    
