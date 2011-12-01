'''
    Created on Nov 29, 2011
    
    @author: jldupont
'''
import doctest

desc_ipv4="""
ipv4 = [
(4, version), (4, ihl), (8, tos), (16, __len__),
(16, id), (3, flags), (13, fragment_offset),
(8, ttl), (8, __next__), (16, checksum),
(32, addr_src), (32, addr_dst),
(*, options), (*, padding)
]
"""

def test_ipv4():
    """
    >>> import parser
    >>> p=parser.tokenize(desc_ipv4)
    >>> print p
    [(1, ('id', 'ipv4')), (1, ('op', '=')), (1, ('op', '[')), (2, ('op', '(')), (2, ('int', '4')), (2, ('op', ',')), (2, ('id', 'version')), (2, ('op', ')')), (2, ('op', ',')), (2, ('op', '(')), (2, ('int', '4')), (2, ('op', ',')), (2, ('id', 'ihl')), (2, ('op', ')')), (2, ('op', ',')), (2, ('op', '(')), (2, ('int', '8')), (2, ('op', ',')), (2, ('id', 'tos')), (2, ('op', ')')), (2, ('op', ',')), (2, ('op', '(')), (2, ('int', '16')), (2, ('op', ',')), (2, ('id', '__len__')), (2, ('op', ')')), (2, ('op', ',')), (3, ('op', '(')), (3, ('int', '16')), (3, ('op', ',')), (3, ('id', 'id')), (3, ('op', ')')), (3, ('op', ',')), (3, ('op', '(')), (3, ('int', '3')), (3, ('op', ',')), (3, ('id', 'flags')), (3, ('op', ')')), (3, ('op', ',')), (3, ('op', '(')), (3, ('int', '13')), (3, ('op', ',')), (3, ('id', 'fragment_offset')), (3, ('op', ')')), (3, ('op', ',')), (4, ('op', '(')), (4, ('int', '8')), (4, ('op', ',')), (4, ('id', 'ttl')), (4, ('op', ')')), (4, ('op', ',')), (4, ('op', '(')), (4, ('int', '8')), (4, ('op', ',')), (4, ('id', '__next__')), (4, ('op', ')')), (4, ('op', ',')), (4, ('op', '(')), (4, ('int', '16')), (4, ('op', ',')), (4, ('id', 'checksum')), (4, ('op', ')')), (4, ('op', ',')), (5, ('op', '(')), (5, ('int', '32')), (5, ('op', ',')), (5, ('id', 'addr_src')), (5, ('op', ')')), (5, ('op', ',')), (5, ('op', '(')), (5, ('int', '32')), (5, ('op', ',')), (5, ('id', 'addr_dst')), (5, ('op', ')')), (5, ('op', ',')), (6, ('op', '(')), (6, (None, '*')), (6, ('op', ',')), (6, ('id', 'options')), (6, ('op', ')')), (6, ('op', ',')), (6, ('op', '(')), (6, (None, '*')), (6, ('op', ',')), (6, ('id', 'padding')), (6, ('op', ')')), (7, ('op', ']'))]
    """

def test_xversa_split():
    """
    >>> from utils import xversa_split
    >>> xversa_split(desc_ipv4)
    [(1, 'ipv4'), (1, '='), (1, '['), (2, '(4,'), (2, 'version),'), (2, '(4,'), (2, 'ihl),'), (2, '(8,'), (2, 'tos),'), (2, '(16,'), (2, '__len__),'), (3, '(16,'), (3, 'id),'), (3, '(3,'), (3, 'flags),'), (3, '(13,'), (3, 'fragment_offset),'), (4, '(8,'), (4, 'ttl),'), (4, '(8,'), (4, '__next__),'), (4, '(16,'), (4, 'checksum),'), (5, '(32,'), (5, 'addr_src),'), (5, '(32,'), (5, 'addr_dst),'), (6, '(*,'), (6, 'options),'), (6, '(*,'), (6, 'padding)'), (7, ']')]
    """
    
def test_build_primitives():
    """
    >>> import parser
    >>> tokens=[(0, ("op","[")),  (0, ("op","]"))]
    >>> print parser.build_primitives(tokens)
    [(0, ('list', []))]
    >>> tokens=[(0, ("op","[")), (1, ("id","element")), (2, ("op","]"))]
    >>> print parser.build_primitives(tokens)
    [(0, ('list', ['element']))]
    >>> tokens=[(0, ("op","[")), (1, ("id","element1")), (1, ("id","element2")), (2, ("op","]"))]
    >>> print parser.build_primitives(tokens)
    [(0, ('list', ['element1', 'element2']))]
    >>> tokens=[(0, ("op","[")), (1, ("id","element1")), (1, ("id","element2")), (1, ("id","element3")), (2, ("op","]"))]
    >>> print parser.build_primitives(tokens)
    [(0, ('list', ['element1', 'element2', 'element3']))]
    >>> tokens=[(0, ("id", "start1")), (0, ("id", "start2")), (0, ("op", "=")), (0, ("op","[")), (1, ("id","element1")), (1, ("id","element2")), (1, ("id","element3")), (2, ("op","]"))]
    >>> print parser.build_primitives(tokens)
    [(0, ('id', 'start1')), (0, ('id', 'start2')), (0, ('op', '=')), (0, ('list', ['element1', 'element2', 'element3']))]
    """
    

doctest.testmod()