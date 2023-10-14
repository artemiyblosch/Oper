import re
from dataclasses import dataclass
from state import *

@dataclass
class Token:
    ltype : str
    val : str

code = "a = (+2);"

def br(i, code, oc):
    start = i = i + 1
    nest = 1
    while nest!=0:
        if (code[i]==oc[0]): nest+=1
        elif (code[i]==oc[1]): nest-=1
        i+=1
    return start, i

def lex(code):
    res = []
    i = 0

    while i < len(code):
        if(code[i]=="("):
            start, i = br(i, code, "()")
            res.append(Token("brs",code[start:i-1]))
        elif(code[i]=="{"):
            start, i = br(i, code, r"{}")
            res.append(Token("nulop",code[start:i-1]))

        for ltype in literals:
            a = literals[ltype].match(code[i:])
            if (a == None): continue
            res.append(Token(ltype, a.group()))
            i+=len(a.group())-1
            break

        i+=1
    return res

def exop(i,code):
    if(code[i].arity() == 2):
        if(len(code) == 1):
            code[i].skipped = True
            return code
        elif(i == 0):
            return code[:i] + [Oper(lambda a: code[i].f(a, code[i+1]), code[i].pref)] + code[i+2:]
        return code[:i-1] + [code[i].f(code[i-1],code[i+1])] + code[i+2:]
    elif (code[i].arity() == 1):
        if(len(code) == 1):
            code[i].skipped = True
            return code
        return code[:i] + [code[i].f(code[i+1])] + code[i+2:]
    elif (code[i].arity() == 0):
        code[i] = code[i].f()
        return code
    raise RuntimeError("How did we get here?")

def parse(code):
    for i,v in enumerate(code):
        if(v.ltype == "nm"):
            code[i] = float(v.val)
        elif(v.ltype == "ident"):
            if(v.val in state):
                code[i] = state[v.val]
        elif(v.ltype == "brs"):
            code[i] = parse(lex(v.val))[0]
        elif(v.ltype == "nulop"):
            code[i] = Oper(lambda:execute(lex(v.val))[-1][0],0)

    opers = [i for i,v in enumerate(code) if isinstance(v,Oper) if not v.skipped]
    while opers != []:
        i = max(opers,key=lambda a: code[a].pref)
        code = exop(i,code)
        opers = [i for i,v in enumerate(code) if isinstance(v,Oper)]
        for i in code:
            if isinstance(code[i],Oper) and code[i].skipped:
                code[i].skipped = False
    return code

def execute(code):
    start = i = 0
    res = []
    while i < len(code):
        while code[i].ltype != "delim": i+=1
        res.append(parse(code[start:i]))
        start = i = i + 1
    pass
    return res

execute(lex(code))