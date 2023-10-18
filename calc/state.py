import inspect
import cmath
import re
from dataclasses import dataclass

@dataclass
class Token:
    ltype : str
    val : str

def fopcr(pref, rop):
    def _(a,b):
        state["a"] = a
        state["b"] = b
        A = rop.f()
        del state["a"]
        del state["b"]
        return A
    return Oper(_,pref)

def WHILE(a,b):
    while b.f():
        a.f()

def question(a,b):
    return Oper(lambda c: b if a else c,14)

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
    if(isinstance(b,Token) and b.val in state): b = state[b.val]
    state[a.val] = b
    return b

state = {"+" : Oper(lambda a,b: a+b, 3),\
         "==" : Oper(lambda a,b: a==b, 2),\
         "<" : Oper(lambda a,b: a<b, 2),\
         ">" : Oper(lambda a,b: a>b, 2),\
         "+" : Oper(lambda a,b: a+b, 3),\
         "*" : Oper(lambda a,b: a*b, 4),\
         "/" : Oper(lambda a,b: a/b, 4),\
         "-" : Oper(lambda a,b: a-b, 3),\
         "**" : Oper(lambda a,b: a**b, 5),\
         "E" : Oper(lambda a,b: a*10**b, 15),\
         "?" : Oper(question, 1),\
         "while" : Oper(WHILE, 1),\
         "=" : Oper(eq, 0),\
         "input" : Oper(lambda a: input(a), 0),\
         "print" : Oper(lambda a: print(a), 0),\
         "do" : Oper(lambda a: a.f(), 14),\
         "num" : Oper(lambda a: float(a), 14),\
         "bin" : Oper(fopcr, 15),\
         "e" : cmath.e, "pi" : cmath.pi,\
         "true" : True, "false" : False}

literals = {"nm" : re.compile(r"\-?\d+(\.\d)?"),\
            "cnm" : re.compile(r"\-?\d+(\.\d)?i"),\
            "ident" : re.compile(r"[^\"\d\s();\[\]\{\}]+"),\
            "str" : re.compile(r"\".*\""),\
            "delim": re.compile(r";")}

