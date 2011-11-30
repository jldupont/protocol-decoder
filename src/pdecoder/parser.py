'''
    Created on Nov 29, 2011
    @author: jldupont
    
    
    expression
        object#name op match-pattern
        object#name.field#name op match-pattern

    match-pattern
        pattern
        [ tuples ]
    
    pattern
        pattern-binary
        pattern-hex
    
    pattern-binary
        B elements-binary
    
    pattern-hex
        H elements-hex
    
    elements-binary
        element-binary
        element-binary elements-binary
    
    elements-hex
        element-hex
        element-hex elements-hex
    
    element-binary
        0
        1
        X
    
    element-hex
        0-9 a-f
        X
    
    tuple
        (nbr_bits, field#name)
    
    nbr_bits
        number
    
    name
        char
        char chars
    
    char
        a-z
    
    number
        int
    int
        digit
        digit1-9 digits
         
    digits
        digit
        digit digits
    op
        =
        >
        <
        >=
        <=
'''
from utils import xversa_split, xtotype, xop

Op_Tokens=[
        "=", ">", "<", ">=", "<="
        ]

Group_Tokens=[
        "[", "]", "(", ")", ","
        ]

class ParserException(Exception):
    pass

def parse(raw_text):
    """
    Parses the input text
    
    @return list of tokens
    """
    def _xop(tokens):
        def _(x):
            return xop(x, "op", tokens)
        return _
        
    raw_tokens=xversa_split(raw_text, tokens=Op_Tokens+Group_Tokens)
    tokens=map(xtotype, raw_tokens)    
    tokens=map(_xop(Op_Tokens+Group_Tokens), tokens)
    
    return tokens

        
    
    