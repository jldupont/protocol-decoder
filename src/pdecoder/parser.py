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
from utils import versa_split

Op_Tokens=[
        "=", ">", "<", ">=", "<="
        ]

Group_Tokens=[
        "[", "]", "|", "(", ")", ","
        ]

DTypes={
         "object_name": "string"
        ,"operator": Op_Tokens
        }

StateGraph=[
            [("object_name", "string"), ("op", "operator"),("match_pattern", "")] 
            ]

class ParserException(Exception):
    pass

def parse(raw_text):
    """
    Parses the input text
    
    @return list of tokens
    """
    s1=raw_text.split("\n")
    
    raw_tokens=versa_split(s1, tokens=Op_Tokens+Group_Tokens)
    
    
    