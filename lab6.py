#!/usr/bin/python

import sys;
import ply.lex as lex;
import ply.yacc as yacc;


class Mem():
    def __init__(self):
        self.counter = 1
        
    def get_mem(self):
        newmem = "mem" + str(self.counter)
        self.counter += 1
        return newmem

class Expr():
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 =  arg1
        self.arg2 = arg2
    
    def eval(self):
        mem = memgen.get_mem()
        print(mem," = ", self.arg1, self.op, self.arg2)



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

def p_expression(p):
    """expression : NUMBER
                  | ID
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | '(' expression ')' """
    
    if(len(p) == 2):
        p[0] = p[1]              
    elif(len(p) == 4):
        if(p[2] == '+'):
            some_expr = Expr(p[2],p[1],p[3])
            some_expr.eval()

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
    file = open("dane.txt", "r");


memgen = Mem()

lexer = lex.lex()
parser = yacc.yacc()
text = file.read()
parser.parse(text, lexer=lexer)




