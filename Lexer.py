# NAME: Derek Haugen
# CLASS: Compiler Construction - Hamer
# ASSIGN#: Assignment 1
# DESC: This is a simple lexical analyzer written to tokenize
#       A subset of the C language. The lexer primarily utilizes
#       regular expressions to match tokens from the input stream.
#
import re, sys, os
#These should be enumerated types but I have declared them as strings
#so that they can also be used for the print statements. They serve
#the same purpose as the enumeration.
AssignT = 'assignop'
MulT = 'mulop'
AddT = 'addop'
RelationT = 'relop'
RParent = 'rightparT'
LParent = 'leftparT'
RBracket = 'rightbracketT'
LBracket = 'leftbracketT'
RBrace = 'rightbraceT'
LBrace = 'leftbraceT'
CommaT = 'commaT'
PeriodT = 'periodT'
QuoteT = 'quoteT'
Reserved = 'reservedT'
Value = 'numT'
ValueR = 'numRealT'
Identifier = 'idT'
Semicolon = "semiT"
IF = 'ifT'
ELSE = 'elseT'
WHILE = 'whileT'
INT = 'integerT'
FLOAT = 'floatT'
CHAR = 'charT'
BREAK = 'breakT'
CONTINUE = 'continueT'
VOID = 'voidT'
STRLITERAL = "strliteralT"
EOF="eofT"
NewLine = "Increment Line Count"
Comment = "Increment with how many newlines found"
Const = 'constantT'
Linecount = 1

tokenFormats = [
    (r'[ \t]+', None), #Whitespace
    (r'[\n]',NewLine),
    (r'\/\*(\*(?!\/)|[^*])*\*\/', Comment), #Comment
    (r'\(', LParent),
    (r'\)', RParent),
    (r'\[', LBracket),
    (r'\]', RBracket),
    (r'\{', LBrace),
    (r'\}', RBrace),
    (r'\,', CommaT),
    (r'"{1}.*?"', STRLITERAL),
    (r'\.', PeriodT),
    (r'[0-9]*\.[0-9]+', ValueR),
    (r'\+', AddT),
    (r'-', AddT),
    (r'\|\|', AddT),
    (r';', Semicolon),
    (r'\*', MulT),
    (r'/', MulT),
    (r'\%', MulT),
    (r'&&', MulT),
    (r'==', RelationT),
    (r'!=', RelationT),
    (r'<=', RelationT),
    (r'>=', RelationT),
    (r'>', RelationT),
    (r'<', RelationT),
    (r'\=', AssignT),
    (r'if(?=\s|\()', IF),
    (r'else(?=\s|\{)', ELSE),
    (r'while(?=\s|\()', WHILE),
    (r'float(?=\s)', FLOAT),
    (r'int(?=\s)', INT),
    (r'char(?=\s)', CHAR),
    (r'break(?=\s|\;)', BREAK), #watch that semicolon
    (r'continue(?=\s|\;)', CONTINUE),
    (r'void(?=\s)', VOID),
    (r'[0-9]+', Value),
    (r'[A-Za-z][A-Za-z0-9_]*', Identifier),
]

#handles the reading from the file to get characters for analysis
def Lexer(inFile):
    arg = inFile
    file = open(arg)
    inLines = file.read()
    file.close()
    tokens = lexer(inLines, tokenFormats)  # keep a list of the tokens for later
    return tokens

#Main function that takes the list of regular expressions and uses them
#to match for expected tokens
def lexer(input, tokenFormats):
    global Linecount
    pos = 0
    lines = 0
    tokens = []
    while pos < len(input):
        match = None
        for tokenFormat in tokenFormats:
            pattern, tag = tokenFormat
            regex = re.compile(pattern)
            match = regex.match(input,pos)
            if match:
                lexeme = match.group(0)
                if tag:
                    if tag == Identifier and len(str(lexeme)) > 27:
                        sys.stderr.write('Illegal length for identifier: %s\n' % lexeme)
                        break;
                    if tag == NewLine:
                        Linecount = Linecount + 1
                        break;
                    if tag == Comment:
                        temp = str(lexeme).split('\n')
                        Linecount = Linecount + len(temp) -1
                        break;
                    attr = checkForAttribute(lexeme,tag)
                    token = (lexeme,tag,attr,Linecount)
                    tokens.append(token)
                    break
                else:
                    break
        if not match:
            sys.stderr.write('Illegal or unknown character: %s\n' % input[pos])
            pos = pos + 1
            lines = lines + 1
        else:
            pos = match.end(0)
    endT=("",EOF,"", Linecount)
    tokens.append(endT)
    return tokens

#function to print found token
def printToken(token,lines):
    template="{0:20}{1:15}{2:10}{3:10}"
    if lines > 20:
        input("Press Enter To Continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(template.format("Lexeme", "Token", "Attribute", "Linenumber"))
        print(template.format(token[0], token[1], token[2], token[3]))
        lines = 0
    else:
        print(template.format(token[0], token[1], token[2],token[3]))
        lines = lines + 1
    return lines

#function that checks if a specific
#token has an attribute associated
def checkForAttribute(val,tag):
    if tag == Value:
        return int(val)
    elif tag == ValueR:
        return float(val)
    elif tag == STRLITERAL:
        return val
    else:
        return ""


