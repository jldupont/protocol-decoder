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
import types
from utils import xversa_split, xtotype, xop

Op_Tokens=[
        "=", ">", "<", ">=", "<="
        ]

Group_Tokens=[
        "[", "]", "(", ")", ","
        ]

Graph=[
        ## object op pattern-binary
        [(False, "id"), (False, "op"), (False, "binary")]
        
        ## object op pattern-hex
       ,[(False, "id"), (False, "op"), (False, "hex")]
       
        ## object op [tuples]
       ,[(False, "id"), (False, "op"), (True, "tuple")]
       ]

class ParserException(Exception):
    pass

def tokenize(raw_text):
    """
    Tokenize the input text, preserving the 'line number'
    
    @return list of tokens
    
    token:  (linenbr, (type, value))
    """
    def _xop(tokens):
        def _(x):
            return xop(x, "op", tokens)
        return _
        
    raw_tokens=xversa_split(raw_text, tokens=Op_Tokens+Group_Tokens)
    tokens=map(xtotype, raw_tokens)    
    tokens=map(_xop(Op_Tokens+Group_Tokens), tokens)
    return tokens

def build_primitives(tokens):
    """
    Handles 'tuple' :  (x,y)
    Handles 'list'  :  [ ... ]
    
    Token of the form:  (linenbr, (type, value))
    """
    def reducer(tk1, tk2):
        #print "tk1:%s  tk2:%s" % (tk1, tk2)
        #sys.stdout.flush()
        
        l2, (_t2, v2) = tk2
        if type(tk1)==types.TupleType:
            liste=[tk1]
        else:
            liste=tk1
            
        #print "liste: %s" % liste
            
        ## inside the list
        tail = liste.pop()
        l1, (t1, v1) = tail
        output=liste            
       
        ## case 1
        if v1=="[" and v2=="]":
            output.append((l1, ("list", [])))
            return output
        
        ## case 2
        if v1=="[":
            output.append((l1, ("list", [v2])))
            return output
        
        ## case 3
        if v2=="]":
            if t1=="list":
                output.append((l1, ("list", v1)))
            else:
                output.append((l2, ("error", "] without [")))
            return output
        
        ## case 4
        if v2=="[":
            output.append(tail)
            output.append((l2, ("list", [])))
            return output
        
        ## case 5: inside a list
        if t1=="list":
            v1.append(v2)
            output.append((l1, ("list", v1)))
            return output
        
        #print "<output: %s" % output    
        output.append(tail)
        output.append(tk2)
        #print ">output: %s" % output
        return output
    
    
    r=reduce(reducer, tokens)
    return r

    
    