'''
    Created on Nov 29, 2011
    
    @author: jldupont
'''
import parser
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
    >>> p=parser.parse(desc_ipv4)
    >>> print p
    [('id', 'ipv4'), ('op', '='), ('op', '['), ('op', '('), ('int', '4'), ('op', ','), ('id', 'version'), ('op', ')'), ('op', ','), ('op', '('), ('int', '4'), ('op', ','), ('id', 'ihl'), ('op', ')'), ('op', ','), ('op', '('), ('int', '8'), ('op', ','), ('id', 'tos'), ('op', ')'), ('op', ','), ('op', '('), ('int', '16'), ('op', ','), (None, '__len__'), ('op', ')'), ('op', ','), ('op', '('), ('int', '16'), ('op', ','), ('id', 'id'), ('op', ')'), ('op', ','), ('op', '('), ('int', '3'), ('op', ','), ('id', 'flags'), ('op', ')'), ('op', ','), ('op', '('), ('int', '13'), ('op', ','), (None, 'fragment_offset'), ('op', ')'), ('op', ','), ('op', '('), ('int', '8'), ('op', ','), ('id', 'ttl'), ('op', ')'), ('op', ','), ('op', '('), ('int', '8'), ('op', ','), (None, '__next__'), ('op', ')'), ('op', ','), ('op', '('), ('int', '16'), ('op', ','), ('id', 'checksum'), ('op', ')'), ('op', ','), ('op', '('), ('int', '32'), ('op', ','), (None, 'addr_src'), ('op', ')'), ('op', ','), ('op', '('), ('int', '32'), ('op', ','), (None, 'addr_dst'), ('op', ')'), ('op', ','), ('op', '('), (None, '*'), ('op', ','), ('id', 'options'), ('op', ')'), ('op', ','), ('op', '('), (None, '*'), ('op', ','), ('id', 'padding'), ('op', ')'), ('op', ']')]
    """

    

doctest.testmod()