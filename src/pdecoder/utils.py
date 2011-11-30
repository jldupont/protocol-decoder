'''
Created on Nov 29, 2011

@author: jldupont
'''
def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

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

            
if __name__=="__main__":
    import doctest
    doctest.testmod()