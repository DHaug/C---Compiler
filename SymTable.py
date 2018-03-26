#Assignment 4
#Compiler Construction
#Due: 3/18/2018
#DESC: This program implements a simple symbol table using a hash table as its core function.
#Since python doesn't have structures and unions by default, I have imported them as libraries
#and integrated them into my table. This module is imported by another driver script and created
# as an object.

import enum as Enum
from collections import defaultdict
import ctypes as ctype

class VarType(Enum.Enum):
    charType = 1
    intType = 2
    floatType = 3

class EntryType(Enum.Enum):
    constEntry = 1
    varEntry = 2
    functionEntry = 3


class SymTable:
    def __init__(self):
        self.__Table = defaultdict(list)
        self.__PrimeNum=211

    def __hash(self, lex): #double underscore to signal the interpreter that this is a private method
        h,g = 0
        for character in lex:
            h = (h<<24) + ord(character)
            if (g == h & 0xF0000000):
                h = h^(g >> 24)
                h = h^g

        return h % self.__PrimeNum

    #inserts an entry
    def insert(self, lex, token, depth):
        tableentry = TableEntry(lex,token,depth)
        index = hash(tableentry.Lexeme)
        self.__Table[index].insert(0,tableentry)

    #looks up a specific lexeme and returns the pointer to the entry
    def lookup(self, lex):
        for entry in self.__Table:
            for subEntry in self.__Table[entry]:
                if subEntry.Lexeme == lex:
                    return subEntry

    #Deletes all entries at the inputted depth
    def deleteDepth(self, depth):
        for entry in self.__Table:
            for subEntry in self.__Table[entry]:
                if subEntry.Depth == depth:
                    self.__Table[entry].remove(subEntry)

    #Writes the lexeme for every entry at the specified depth
    def writeTable(self,depth):
        for entry in self.__Table:
            for subEntry in self.__Table[entry]:
                if subEntry.Depth == depth:
                   print(str(subEntry.Lexeme))
                elif subEntry.Depth < depth: #if the current depth is less then the search depth, then
                    return                   #there aren't anymore in the list to look for

#TableEntry object to store the details of an entry into the table
class TableEntry:
    def __init__(self, lex, token, depth):
        self.Lexeme = lex
        self.Token = token
        self.Depth = depth
        self.EntryType = None

        class VAR(ctype.Structure):
            TypeOfVariable = None #Cannot bind this to anything yet in python
            offset = int()
            size = int()

        class CONSTANT(ctype.Structure):
            TypeOfConstant = None #Cannot set this to anything yet in python
            offset = int()
            #Sub-union in CONSTANT struct
            class ValUnion(ctype.Union):
                _fields_ = [("Value", ctype.c_int),
                            ("ValueR", ctype.c_float)]

        class FUNCTION(ctype.Structure):
            SizeOfLocal = int()
            NumberOfParameters = int()
            ReturnType = None #Cannot set this to anything yet in python
            ParamList = [] #Stores the VarTypes of each parameter

        #union to store all of the previous structures
        class TypeStoredUnion(ctype.Union):
            _fields_ = [
                ("var", VAR),
                ("constant", CONSTANT),
                ("function", FUNCTION)
            ]
