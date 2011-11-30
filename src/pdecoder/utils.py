'''
Created on Nov 29, 2011

@author: jldupont
'''
import re


def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7])
    [1, 2, 3, 42, None, 4, 5, 6, 7]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def versa_split(txt, tokens=None):
    """
    Splits the 'txt' string based on all the elements of 'seps'
    
    >>> s="t1 t2=t3 t4"
    >>> versa_split(s, tokens=["="])
    ['t1', 't2', '=', 't3', 't4']
    """
    def s(sep):
        def _(txt):
            return txt.split(sep)
        return _

    tokens=tokens if tokens is not None else []
    for token in tokens:
        txt=txt.replace(token, " %s " % token)
    r=txt.split(" ")
        
    return r


REGEX_PATTERN_ID=r'[a-z][a-z0-9]+'
REGEX_ID=re.compile(REGEX_PATTERN_ID)

def is_id(txt):
    """
    Determines if 'txt' is an "identifier" string
    
    @return Boolean
    
    >>> is_id("allo")
    True
    >>> is_id("1allo")
    False
    >>> is_id(" allo ")
    True
    >>> is_id(" allo1234 ")
    True
    >>> is_id(" a1234llo1234 ")
    True
    """
    s=txt.strip()
    r=REGEX_ID.match(s)
    if r is None:
        return False
    
    return r.group()==s

REGEX_PATTERN_BINARY=r'B[X01]+'
REGEX_BINARY=re.compile(REGEX_PATTERN_BINARY)
        
def is_binary_pattern(txt):
    """
    Determines if 'txt' is a "binary pattern"
    e.g.  B011111X
    
    >>> is_binary_pattern("B1001")
    True
    >>> is_binary_pattern("B1001X")
    True
    >>> is_binary_pattern("BXXXXX")
    True
    >>> is_binary_pattern("B2222")
    False
    >>> is_binary_pattern("H011111")
    False
    >>> is_binary_pattern("HXXXXXX")
    False
    """
    s=txt.strip()
    r=REGEX_BINARY.match(s)
    if r is None:
        return False
    
    return r.group()==s

REGEX_PATTERN_HEX=r'H[X0-9a-f]+'
REGEX_HEX=re.compile(REGEX_PATTERN_HEX)
        
def is_hex_pattern(txt):
    """
    Determines if 'txt' is an "hex pattern"
    e.g.  B011111X
    
    >>> is_hex_pattern("B1001")
    False
    >>> is_hex_pattern(" HX0123456789abcdef ")
    True
    >>> is_hex_pattern(" HXXXXXXXXXXXXXXXXX ")
    True
    >>> is_hex_pattern("H00000000000000000")
    True
    """
    s=txt.strip()
    r=REGEX_HEX.match(s)
    if r is None:
        return False
    
    return r.group()==s


            
if __name__=="__main__":
    import doctest
    doctest.testmod()