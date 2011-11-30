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
    """
    
    

doctest.testmod()