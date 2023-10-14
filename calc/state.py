import inspect
import cmath
import re

class Oper:
    def __init__(self, f, pref):
        self.f = f
        self.pref = pref
        self.skipped = False
    
    def arity(self):
        return len(list(inspect.signature(self.f).parameters))
    
    def __repr__(self):
        return f"Oper<{self.arity()},{self.pref}>"

    def __add__(self,other):
        aA = self.arity()
        bA = other.arity()
        if(aA == 1 and bA == 0):
            return Oper(lambda: self.f(other.f()), aA)
        elif(aA == 0 and bA == 1):
            return Oper(lambda: other.f(self.f()), aA)
        elif(aA == 1 and bA == 1):
            return Oper(lambda a: self.f(other.f(a)), max(aA,bA))
        elif(aA == 1 and bA == 2):
            return Oper(lambda a,b: self.f(other.f(a,b)), max(aA,bA))
        elif(aA == 2 and bA == 1):
            return Oper(lambda a,b: self.f(a, other.f()), max(aA,bA))
        elif(aA == 2 and bA == 2):
            return Oper(lambda a,b: self.f(other.f(a,b),b), max(aA,bA))
        elif(aA == 2 and bA == 0):
            return Oper(lambda a: self.f(a,other.f()), aA)
        elif(aA == 0 and bA == 2):
            return Oper(lambda a: other.f(self.f(),a), bA)

def eq(a,b):
    state[a.val] = b
    return b

state = {"+": Oper(lambda a,b: a+b, 1),\
         "*": Oper(lambda a,b: a*b, 2),\
         "/": Oper(lambda a,b: a/b, 2),\
         "-": Oper(lambda a,b: a-b, 1),\
         "**": Oper(lambda a,b: a**b, 3),\
         "E": Oper(lambda a,b: a*10**b, 15),\
         "=": Oper(eq, 0),\
         "print" : Oper(lambda a: print(a), 0),\
         "do" : Oper(lambda a: a.f(), 16),\
         "e" : cmath.e, "pi": cmath.pi}

literals = {"nm" : re.compile(r"\-?\d+(\.\d)?"),\
            "ident" : re.compile(r"[^\d\s();\[\]\{\}]+"),\
            "delim": re.compile(r";")}

