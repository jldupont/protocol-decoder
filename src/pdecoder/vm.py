'''
Created on 2011-12-06

@author: jldupont
'''
import utils
import types

def not_empty(x, strict=False):
    """
    Determines if the list, tuple, dict or string is empty
    """
    try:
        ### applies to list, tuple, dict
        return len(x)!=0
    except:
        ### for strings
        try:
            s=x.strip()
            return len(s)!=0
        except:
            if strict:
                raise
            return False


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
    """
    Compose an object 'o' with a list of functions
    Useful in 'map' application
    """
    def c(o):
        for fn in fn_list:
            o=fn(o)
        return o
    return c

def feval(l):
    """
    Maps a list of strings to their native types
    e.g. "[...]" -> [...] 
    """
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
        
        def is_fn(x):
            return x.startswith("fn_")
        
        def get_fns():
            fns=filter(is_fn, self.__dict__)
            return map(lambda x:x[3:], fns)
        
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
        ## are treated as correctly:  compress ', ' to ','
        f=compose([comas, split])
        _sts=map(f, _lines)

        self.sts=filter(f_not_empty, _sts)
        self.fns=get_fns()        
        
    def resolve(self, field_or_string_or_scalar):
        """
        Is it a "field" in the dic or a "scalar"?
        """
        try:
            ## scalar
            maybe_scalar=field_or_string_or_scalar
            code, value=utils.versa_int(maybe_scalar)
            assert(code==True)
            return ("scalar", value)
        except:
            ## maybe a register
            maybe_reg=field_or_string_or_scalar
            value=self.dic.get(maybe_reg, None)
            if value is not None:
                return ("field", value)
        
        maybe_fn=field_or_string_or_scalar
        if maybe_fn in self.fns:
            return ("function", maybe_fn)
            
        return ("unknown", field_or_string_or_scalar)
    
    def _common(self, fnname, fn, rreg, field_or_scalar):
        try:
            try:
                lcode, lvalue=self.resolve(rreg)
                assert(lcode=="field")
            except AssertionError:
                return ("error", "reg'%s' not defined" % rreg)
            
            try:
                rcode, rvalue=self.resolve(field_or_scalar)
                assert(rcode!="unknown")
            except AssertionError:
                return ("error", "expecting a register or scalar, got '%s'" % field_or_scalar)

            try:            
                return fn(rreg, lvalue, rvalue)
            except Exception,e:
                return ("error", "calling '%s' with lvalue=%s , rvalue=%s : %s" % (fnname, lvalue, rvalue, e))
    
        except Exception,e:
            return ("error", "unknown error: %s" % e)    
    
        
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
        
        'rreg' is supposed to be a field in the dic
        """
        try:
            try:
                lcode, lvalue=self.resolve(rreg)
                assert(lcode=="field")
            except AssertionError:
                return ("error", "reg'%s' not defined" % rreg)
            
            try:
                rcode, rvalue=self.resolve(field_or_scalar)
                assert(rcode!="unknown")
            except AssertionError:
                return ("error", "expecting a register or scalar, got '%s'" % field_or_scalar)
            
    
            result=(lvalue==rvalue)
            if result:
                return ("ok", None)
            return ("assert_equal", "lvalue'%s' != rvalue'%s'" % (lvalue, rvalue))
        except Exception,e:
            return ("error", "unknown error: %s" % e)    
        
    def fn_mask(self, rreg, field_or_scalar):
        """
        Perform a "bitwise AND"
        """
        def mask(rreg, reg_value, data):
            if type(data)!=types.IntType:
                return ("error", "expecting a scalar for the operard, got '%s'" % data)
            self.dic[rreg]=(reg_value & data)
            return ("ok", None)
        
        return self._common("mask", mask, rreg, field_or_scalar)
        
    def fn_load(self, rreg, field_or_scalar1, field_or_scalar2):
        """
        load  rreg  data_offset  byte_count
        """
        
        
        
        
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

    code5="""
    let  r1 0b1101
    let  r2 0b1100
    mask r2 r1
    """

    def test5():
        """
        >>> vm=VM(code5)
        >>> vm.run(None)
        ('ok', None, None, None)
        >>> print vm.dic["r2"]
        12
        """
    
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

