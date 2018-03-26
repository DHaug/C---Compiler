import sys, re, string, os
from Lexer import *




if len(sys.argv) < 2:
    print("No file given!")
    exit(1)


Tokens=Lexer(sys.argv[1])
#Token and Tokens Global Vars)

if(len(Tokens)>0):
    Token = Tokens[0]



def getNextToken():
    global Token
    global Tokens
    Tokens.pop(0)
    if(len(Tokens) > 0):
        Token = Tokens[0]



def match(token, expToken):
    if token == expToken:
        getNextToken()
        return True
    else:
        print("Error! Expected token:"+expToken+" Token encountered:"+token+" On Line:"+str(Token[3]))
        exit(1)

def isType(token):
    if (token == INT or token == FLOAT or token == CHAR):
        return True
    else:
        return False

def prog():
    if isType(Token[1]):
        TYPE()
        match(Token[1],Identifier)
        REST()
        prog()
    elif(Token[1] == Const)
    else:
        pass

def TYPE():
    if Token[1] == INT:
        match(Token[1],INT)
    elif Token[1] == FLOAT:
        match(Token[1],FLOAT)
    elif Token[1] == CHAR:
        match(Token[1],CHAR)
    else:
        print("Error! Expected token:"+INT+" or "+FLOAT+" or "+CHAR+"!"+" Token encountered:"+Token[1]+" On Line:"+str(Token[3]))
        exit(1)

def REST():
    if Token[1] == LParent:
        match(Token[1], LParent)
        PARAMLIST()
        match(Token[1],RParent)
        COMPOUND()
    else:
        IDTAIL()
        match(Token[1], Semicolon)
        prog()

def PARAMLIST():
    if isType(Token[1]):
        TYPE()
        match(Token[1], Identifier)
        PARAMTAIL()
    else:
        pass

def PARAMTAIL():
    if Token[1] == CommaT:
        match(Token[1], CommaT)
        TYPE()
        match(Token[1], Identifier)
        PARAMTAIL()
    else:
        pass

def COMPOUND():
    match(Token[1],LBrace)
    DECL()
    STAT_LIST()
    RET_STAT()
    match(Token[1],RBrace)

def DECL():
    if isType(Token[1]):
        TYPE()
        IDLIST()
    else:
        pass

def IDLIST():
    match(Token[1], Identifier)
    IDTAIL()
    match(Token[1], Semicolon)
    DECL()

def IDTAIL():
    if Token[1] == CommaT:
        match(Token[1],CommaT)
        match(Token[1], Identifier)
        IDTAIL()
    else:
        pass

def STAT_LIST():
    pass

def RET_STAT():
    pass

prog()

if(len(Tokens) > 1):
    print("ERROR UNUSED TOKENS")
elif Token[1] != EOF:
    print("Error no end of file token found.")
else:
    print("Program compiled successfully..")

