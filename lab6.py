#!/usr/bin/python

import sys;
import math;
import ply.lex as lex;
import ply.yacc as yacc;

def invert_op(op):
    """odwraca operator, potrzebne zeby zaprzeczyc 
    warunek przy instrukcji if, a to z kolei jest potrzebne bo mamy mniej skokow dzieki temu"""
    if(op == "<"): return ">="
    elif(op == ">"): return "<="
    elif(op == ">="): return "<"
    elif(op == "<="): return ">"
    elif(op == "=="): return "!="
    elif(op == "!="): return "=="

class Mem():
    """zwraca nam kolejne zmienne tymczasowe mem1, mem2, ..."""
    def __init__(self):
        self.counter = 1
        
    def get_mem(self):
        newmem = "mem" + str(self.counter)
        self.counter += 1
        return newmem
        
class Pos():
    """zwraca nam adresy w pamieci"""
    def __init__(self):
        self.counter = 101
        
    def get_pos(self):
        """tutaj adres kolejnej instrukcji"""
        newpos = str(self.counter)
        self.counter += 1
        return newpos
        
    def get_jump_pos(self):
        """natomiast tutaj adres do ktorego mamy zrobic skok"""
        newpos = str(self.counter)
        return newpos

class Expr():
    """expr to jakies dzialanie, np. 2+2, wynik zapisywany jest w zmiennej tymczasowej mem"""
    def __init__(self, arg1, op, arg2):
        self.op = op
        self.arg1 =  arg1
        self.arg2 = arg2
        self.mem = ""
    
    def get_res(self):
        """zwraca nam numerek zmiennej mem w ktorej jest wynik"""
        return self.mem
    
    def eval(self):
        """ewaluuje dziecji w drzewie syntaktycznym, pobiera memy ktore zwroca
        i robi stringa (generuje swoj kod) ktorego przekazuje do przodka w drzewie"""
        ret1 = self.arg1.eval()
        ret2 = self.arg2.eval()
        retmem1 = self.arg1.get_res()
        retmem2 = self.arg2.get_res()
        mem = memgen.get_mem()
        self.mem = mem
        pos = posgen.get_pos()
        wyn = ""
        wyn += ret1
        wyn += ret2
        wyn += str(pos) + ": " + mem + " = " + retmem1 + " " + self.op + " " + retmem2 + "\n"
        return wyn

class Const():
    """stała, jakas liczba, jeśli float z zerem po przecinku to zamieniam na inta"""
    def __init__(self, val):
        if(val == math.floor(val)):
            self.val = int(val)
        else:
            self.val = val
    
    def get_res(self):
        return str(self.val)
    
    def eval(self):
        """stała nie generuje zadnego kodu wiec pusty"""
        return ""

class Var():
    """zmienna, podobnie jak przy stałej"""
    def __init__(self, name):
        self.name = name
        
    def get_res(self):
        return self.name
        
    def eval(self):
        return ""
    
class Assign():
    """przypisanie wyniku do zmiennej"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def eval(self):
        """ewaluuje dzieci, pobiera ich wyniki i tworzy swoj kod który zwraca do przodka"""
        ret1 = self.left.eval()
        ret2 = self.right.eval()
        retmem1 = self.left.get_res()
        retmem2 = self.right.get_res()
        pos = posgen.get_pos()
        wyn = ""
        wyn += ret1
        wyn += ret2
        wyn += str(pos) + ": " + retmem1 + " = " + retmem2 + "\n"
        return wyn

class Compar():
    """porownanie"""
    def __init__(self, arg1, op, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.retmem1 = ""
        self.retmem2 = ""
    
    def get_res(self):
        return (self.op,self.retmem1,self.retmem2)
    
    def eval(self):
        """analogicznie jak pozostałe"""
        ret1 = self.arg1.eval()
        ret2 = self.arg2.eval()
        wyn = ""
        wyn += ret1
        wyn += ret2
        self.retmem1 = self.arg1.get_res()
        self.retmem2 = self.arg2.get_res()
        return wyn
    
class ChoiceInstr():
    """instrukcja warunkowa if"""
    def __init__(self, cond, sttm, sttm2):
        self.cond = cond
        self.sttm = sttm
        self.sttm2 = sttm2
        
    def eval(self):
        """tutaj chyba najtrudniejszy fragment, nie mam teraz czasu wiec tylko po krótce opowiem,
        trzeba ewaluować warunek, sprawdzić czy to jest sam if czy if a potem else, poobliczać skoki...
        jesli nie ma else to sttm2 == 0 bo tak wrzucam w parserze"""
        ret = self.cond.eval()
        retmem = self.cond.get_res()
        pos = posgen.get_pos()
        wyn = ""
        wyn += ret
        jumppos1 = 0
        ret1 = self.sttm.eval()
        wyn2 = ""
        if(self.sttm2 != 0):
            pos2 = posgen.get_pos()
            jumppos1 = posgen.get_jump_pos()
            ret2 = self.sttm2.eval()
            jumppos2 = posgen.get_jump_pos()
            wyn2 += str(pos2) + ": " + "if" + "== " + "1 " + "1 " + str(jumppos2) + "\n"
            wyn2 += ret2
        if(jumppos1 == 0):
            jumppos1 = posgen.get_jump_pos()
        wyn += str(pos) + ": " + "if" + invert_op(retmem[0]) + " " + retmem[1] + " " + retmem[2] + " " + str(jumppos1) + "\n"
        wyn += ret1
        wyn += wyn2
        return wyn
    
class ListInstr():
    """instrukcje w bloku {}"""
    def __init__(self, l_instr):
        self.l_instr = l_instr
        
    def eval(self):
        """ewaluuje wszystkie po kolei"""
        wyn = ""
        for i in self.l_instr:
            wyn += i.eval()
        return wyn
    


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
    p[0] = ListInstr(p[1])
    print(p[0].eval())

def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""

    if(len(p) == 3):
        if(type(p[1]) == list):
            x = []
            x.extend(p[1])
            x.append(p[2])
            p[0] = x
        else:
            x = []
            x.append(p[2])
            p[0] = x
    else:
        x = []
        x.append(p[1])
        p[0] = x

def p_instruction(p):
    """instruction : assignment
                   | choice_instr"""
    
    p[0] = p[1]
    
def p_assignment(p):
    """assignment : ID '=' expression ';' """
    
    p[0] = Assign(Var(p[1]),p[3])

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
    if(len(p) == 6):
        p[0] = ChoiceInstr(p[3], p[5], 0)
    else:
        p[0] = ChoiceInstr(p[3], p[5], p[7])

def p_condition(p):
    """condition : expression EQ  expression
                 | expression NEQ expression
                 | expression GE  expression
                 | expression LE  expression
                 | expression '<' expression
                 | expression '>' expression """
                 
    p[0] = Compar(p[1],p[2],p[3])
    
def p_stmt(p):
    """stmt : assignment
            | '{' instructions '}'
            | choice_instr """
    
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = ListInstr(p[2])
        

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




