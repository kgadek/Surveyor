#!/usr/bin/python

import sys;
import math;
import ply.lex as lex;
import ply.yacc as yacc;


class Mem():
    def __init__(self):
        self.counter = 1
        
    def get_mem(self):
        newmem = "mem" + str(self.counter)
        self.counter += 1
        return newmem
        
class Pos():
    def __init__(self):
        self.counter = 101
        
    def get_pos(self):
        newpos = str(self.counter)
        self.counter += 1
        return newpos
        

class Expr():
    def __init__(self, arg1, op, arg2):
        self.op = op
        self.arg1 =  arg1
        self.arg2 = arg2
    
    def eval(self):
        ret1 = self.arg1.eval()
        ret2 = self.arg2.eval()
        mem = memgen.get_mem()
        pos = posgen.get_pos()
        print(pos, ": ", mem, " = ", ret1, self.op, ret2)
        return mem

class Const():
    def __init__(self, val):
        if(val == math.floor(val)):
            self.val = int(val)
        else:
            self.val = val
    
    def eval(self):
        return self.val

class Var():
    def __init__(self, name):
        self.name = name
        
    def eval(self):
        return self.name
    
class Assign():
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def eval(self):
        ret1 = self.left.eval()
        ret2 = self.right.eval()
        pos = posgen.get_pos()
        print(pos, ": ", ret1, " = ", ret2)

class Compar():
    pass
    
class ChoiceInstr():
    pass
    
class ListInstr():
    pass
    


literals = "{}()<>=;+-*/"

tokens = ( "ID", "NUMBER", "IF",  "ELSE", "EQ", "NEQ", "LE", "GE" );

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


def t_NUMBER(t):
    r"\d+(\.\d*)?|\.\d+"
    t.value = float(t.value)
    return t

def t_IF(t):
    "if"
    return t

def t_ELSE(t):
    "else"
    return t

def t_LE(t):
    r"<="
    return t

def t_GE(t):
    r">="
    return t

def t_EQ(t):
    r"=="
    return t

def t_NEQ(t):
    r"!="
    return t

def t_ID(t):
    r"[a-zA-Z_]\w*"
    return t


precedence = (
   ("nonassoc", 'IFX'),
   ("nonassoc", 'ELSE'),
   ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
   ("left", '+', '-'),
   ("left", '*', '/') )



def p_error(p):
    print("Syntax error at token", p.type)

def p_program(p):
    """program : instructions"""


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""
    

def p_instruction(p):
    """instruction : assignment
                   | choice_instr"""
    

def p_assignment(p):
    """assignment : ID '=' expression ';' """
    
    p[0] = Assign(Var(p[1]),p[3])
    p[0].eval()

def p_expression(p):
    """expression : NUMBER
                  | ID
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | '(' expression ')' """
    
    if(len(p) == 2):
        if(type(p[1]) == float):
            p[0] = Const(p[1])
        else:
            p[0] = Var(p[1])
    elif(len(p) == 4):
        if(p[1] != '('):
            p[0] = Expr(p[1],p[2],p[3])
        else:
            p[0] = p[2]

def p_choice_instr(p):
    """choice_instr : IF '(' condition ')' stmt %prec IFX
                    | IF '(' condition ')' stmt ELSE stmt """


def p_condition(p):
    """condition : expression EQ  expression
                 | expression NEQ expression
                 | expression GE  expression
                 | expression LE  expression
                 | expression '<' expression
                 | expression '>' expression """

def p_stmt(p):
    """stmt : assignment
            | '{' instructions '}'
            | choice_instr """


if len(sys.argv)>1:
    file = open(sys.argv[1], "r");
else:
    file = open("example.txt", "r");


memgen = Mem()
posgen = Pos()

lexer = lex.lex()
parser = yacc.yacc()
text = file.read()
parser.parse(text, lexer=lexer)




