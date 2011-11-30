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
    txt=txt.replace("\n", " ")
    tokens=tokens if tokens is not None else []
    for token in tokens:
        txt=txt.replace(token, " %s " % token)
    r=txt.split(" ")
    
    def not_empty(x):
        try:
            return len(x)!=0
        except:
            s=x.strip()
            return len(s)!=0
        
    r2=filter(not_empty, r) 
    return r2

def xversa_split(txt, tokens=[]):
    
    def assign_line_nbr(line, linenbr):
        return (linenbr, line)
        
    _lines=txt.split("\n")
    lines=map(assign_line_nbr, _lines, range(0, len(_lines)))
    
    def tokenize(x):
        linenbr, line=x   
        for token in tokens:
            line=line.replace(token, " %s " % token)
            
        fragments=line.split(" ")
        
        def put_line_nbr(x):
            return (linenbr, x)
            
        return map(put_line_nbr, fragments)

    def extend(a, b):
        return a+b
    
    _tokens=map(tokenize, lines)
    tokens=reduce(extend, _tokens)
    
    def not_empty(x):
        _, line=x
        try:
            return len(line)!=0
        except:
            s=line.strip()
            return len(s)!=0
        
    r2=filter(not_empty, tokens) 
    return r2


def _check(regex, inp):
    s=inp.strip()
    r=regex.match(s)
    if r is None:
        return False
    
    return r.group()==s
    

REGEX_PATTERN_ID=r'[_a-z][_a-z0-9]+'
REGEX_ID=re.compile(REGEX_PATTERN_ID)

def is_id(txt):
    """
    Determines if 'txt' is an "identifier" string
    
    @return Boolean

    >>> is_id("__len__")
    True
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
    return _check(REGEX_ID, txt)

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
    return _check(REGEX_BINARY, txt)    

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
    return _check(REGEX_HEX, txt)

def totype(x):
    """
    >>> totype("a1234")
    ('id', 'a1234')
    >>> totype(1234)
    ('int', 1234)
    >>> totype("BX10101010") # doctest:+ELLIPSIS
    ('binary', ...)
    """
    
    ## ORDER IS IMPORTANT!
    fs=[ 
        (is_binary_pattern, "binary") 
        ,(is_hex_pattern,   "hex")
        ,(int,              "int")
        ,(is_id,            "id")
        ]
    
    for f, name in fs:
        try:
            r=f(x)
            if r is True:
                return (name, x)
            if r is False:
                continue
            return (name, x)
        except:
            pass
    return (None, x)

def xtotype(x):
    """
    >>> xtotype((1, "a1234"))
    (1, ('id', 'a1234'))
    >>> xtotype((2, 1234))
    (2, ('int', 1234))
    >>> xtotype((3, "BX10101010")) # doctest:+ELLIPSIS
    (3, ('binary', ...))
    """
    linenbr, line=x
    r=totype(line)
    return (linenbr, r)
            
def xop(x, otype, tokens):
    linenbr, r=x
    t, v=r
    if t is None:
        if v in tokens:
            return (linenbr, (otype, v))
    return x
            
            
if __name__=="__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

