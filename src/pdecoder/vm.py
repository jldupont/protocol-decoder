'''
Created on 2011-12-06

@author: jldupont
'''
import utils

def not_empty(x):
    try:
        return len(x)!=0
    except:
        s=x.strip()
        return len(s)!=0

def f_not_empty((_, x)):
    """
    >>> print f_not_empty((0, []))
    False
    """
    try:
        return len(x)!=0
    except:
        s=x.strip()
        return len(s)!=0

def compose(fn_list):
    def c(o):
        for fn in fn_list:
            o=fn(o)
        return o
    return c

def feval(l):
    
    def e(o):
        try:    return eval(o)
        except: return o
        
    return map(e, l)


class base():
    """
    Code lines are simple:
        function  field_name  [parameters]
    """
    
    def __init__(self, code):
        
        def assign_line_nbr(line, linenbr):
            return (linenbr, line)
        
        def split((line_nbr, raw)):
            _=raw.split(" ")
            tokens=filter(not_empty, _)
            return (line_nbr, tokens)
        
        def comas((_, x)):
            return (_, x.replace(", ", ","))
        
        ## we want non-empty lines
        _=code.split("\n")
        _=filter(not_empty, _)
        _lines=map(assign_line_nbr, _, range(0, len(_)))  ## (linenbr, line_data)

        ## since the separator is the space,
        ## we want to make sure that coma separated constructs
        ## are treated as correctly
        f=compose([comas, split])
        _sts=map(f, _lines)

        self.sts=filter(f_not_empty, _sts)        
        
    def run(self, data):
        self.data=data
        self.line_ptr=0
        self.dic={}
        ctx="start"
        linenbr=None
        try:
            ## go through all "statements"
            for stsx in self.sts:
                (linenbr, sts)=stsx
                ctx="expecting 'function'"
                fn=sts.pop(0)
                ctx="evaluating parameters"
                params=feval(sts)
                ctx="calling function '%s'" % fn
                code, msg=getattr(self, "fn_%s" % fn)(*params)
                assert(code=="ok")
                
        except AssertionError:
            return (code, ctx, linenbr, msg)
                
        except Exception, e:
            return ("error", ctx, linenbr, e)
        
        return ("ok", None, None, None)
            
        
      
class VM(base):
    
    def __init__(self, code):
        base.__init__(self, code)
        self.data=None
        
    def fn_let(self, rreg, scalar):
        #print "let rreg(%s) scalar(%s)" % (rreg, scalar)
        self.dic[rreg]=scalar
        return ("ok", None)
        
    def fn_length(self, rreg, reg):
        """
        Computes the length of the expected array pointed by 'reg'
        """
        try:
            data=self.dic[reg]
        except:
            return ("error", "reg'%s' not defined" % reg)
        
        try:
            l=len(data)
        except:
            return ("error", "can't evaluate length of data in reg'%s'" % reg)
        #print "length rreg(%s) reg(%s) -> %s" % (rreg, reg, l)
        self.dic[rreg]=l
        return ("ok", None)
    
    def fn_assert_equal(self, rreg, field_or_scalar):
        """
        Compare contents of register 'rreg' with 'field or scalar'
        """
        lvalue=self.dic.get(rreg, None)
        if lvalue is None:
            return ("error", "reg'%s' not defined" % rreg)
        try:
            ## scalar
            code, rvalue=utils.versa_int(field_or_scalar)
            assert(code==True)
        except:
            ## maybe a register
            rvalue=self.dic.get(field_or_scalar, None)
            if rvalue is None:
                return ("error", "expecting a register or scalar, got '%s'" % field_or_scalar)
            
        result=(lvalue==rvalue)
        if result:
            return ("ok", None)
        return ("assert_equal", "lvalue'%s' != rvalue'%s'" % (lvalue, rvalue))
    
        
      
        
        
if __name__=="__main__":
    
    code1="""
    f1 r1 a1 a2
    f2 r2 b1 b2
    """
    
    code2="""
    let r1 [111, 222, 333]
    length r2 r1
    """

    
    def test1():
        """
        >>> vm=VM(code1)
        >>> print vm.sts
        [(0, ['f1', 'r1', 'a1', 'a2']), (1, ['f2', 'r2', 'b1', 'b2'])]
        """
        
    def test2():
        """
        >>> vm=VM(code2)
        >>> vm.run(None)
        ('ok', None, None, None)
        >>> print vm.dic["r1"]
        [111, 222, 333]
        >>> print vm.dic["r2"]
        3
        """

    code3="""
    let r1 0b1001
    assert_equal r1 9
    """

    def test3():
        """
        >>> vm=VM(code3)
        >>> vm.run(None)
        ('ok', None, None, None)
        """

    code4="""
    let r1 0b1001
    assert_equal r1 8
    """

    def test4():
        """
        >>> vm=VM(code4)
        >>> vm.run(None)
        ('assert_equal', "calling function 'assert_equal'", 1, "lvalue'9' != rvalue'8'")
        """
    
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
