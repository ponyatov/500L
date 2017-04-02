import ply.lex  as lex
import ply.yacc as yacc

tokens = ['SYM','BINOP','DEF']

t_ignore = ' \t\r'

def t_newline(t):
	r'\n'
	t.lexer.lineno += 1

t_BINOP = r'[\.\,]'
def t_DEF(t):
	r'def'
	return t
def t_SYM(t):
	r'[a-zA-Z0-9_]+|\#.*|[\(\)\:\=\;\%\[\]\-\{\}]|\'.*\''
	return t

def p_REPL_none(p): ' REPL : '
def p_REPL_recur(p):
	' REPL : REPL ex '
	print p[2]

def p_ex_SYM(p):
	' ex : SYM '
	p[0] = p[1] # atom

def p_ex_BINOP(p):
	' ex : ex BINOP ex '
	p[0] = [ p[2] , p[1] , p[3] ]

def p_ex_DEF(p):
	' ex : DEF SYM '
	p[0] = [ p[1] , p[2] ]

def t_error(t): print 'lexer/error',t
def p_error(p): print 'parse/error',p

import sys
lex.lex()
yacc.yacc(debug=False,write_tables=False).parse(sys.stdin.read())
