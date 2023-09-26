#!/usr/bin/env python3
#
#
#Assembler.py
#
# CS2001   Project 6 Assembler
# 31 July 2013
# last updated 23 Sept 2021
#
# start code version
#
import sys  #for command line launch functionality

from Code import *
from SymbolTable import *
from Parser import *


'''Manages the assembly process, used the Parser to do the mechanical tokenizing and then
   determines the semantically correct thing to do with those tokens. Then uses the Parser
   to break tokens into appropriate components and requests the translations of those
   components from the Code module. Labels are passed to the SymbolTable to get mapped
   against addresses.'''
class Assembler(object):

##########################################
#Constructor

    def __init__(self, target):

        index = target.find('.asm')
        if ( index < 1):
            raise RuntimeError( "error, cannot use the filename: " + target )

        self.inputFileName = target
        self.outputFileName = self.inputFileName[:index] + '.hack'

        self.parser = Parser(self.inputFileName)

        self.code = Code()
        self.st = SymbolTable()




##########################################
#public methods

    def assemble(self):
        '''Does the assembly and creates the file of machine commands,
           returning the name of that file '''
        self.__firstPass()
        return  self.__output( self.__secondPass() )







##########################################
#private/local methods
 
    def __output(self, codeList):
        ''' outputs the machine code codeList into a file and returns the filename'''

        file = open(self.outputFileName,"w")
        file.write("\n".join(codeList))
        file.close()
        return self.outputFileName


    def __firstPass(self):
        ''' Passes over the file contents to populate the symbol table with label declarations'''
        #MUST prevent the Assembler reaching into the parser
        #   while also not requiring the parser to become semantically aware
        #so let parser do mechanical work
        #   and let Assembler do the semantic part on the returned results

        labels = self.parser.processLabels();
        # Apend the new labels to the SymbolTable dictionary
        for key,value in labels.items():
            self.st.addEntry(key, value)


    def __secondPass(self):
        ''' Manage the translation to machine code, returning a list of machine instructions'''
        
        machineCode = []
        self.parser.create_toParse_iterrator()
        command = self.parser.advance()
        while( command ):         
            command_type = self.parser.commandType(command)
            if command_type == 1: # A - Instruction
                command = self.parser.symbol(command)
                bitString = self.__assembleA(command)

            elif command_type == 2: # C - Instruction
                bitString = self.__assembleC(command)
            else:
                symStr = self.parser.symbol()
                raise RuntimeError( 'There should be no labels on second pass, errant symbol is ' + symStr)
            machineCode.append(bitString)
            command = self.parser.advance()
        return machineCode



    def __assembleC(self, command):
        ''' Do the mechanical work to translate a C_COMMAND, returns a string representation
            of a 16-bit binary word.'''

        c_ins_parts = self.parser.command_separation(command)
        return '111'+self.code.comp(c_ins_parts[0])+self.code.dest(c_ins_parts[1])+self.code.jump(c_ins_parts[2]);



         
    def __assembleA(self, command):
        ''' Do the mechanical work to translate an A_COMMAND, returns a string representation
            of a 16-bit binary word.'''

        if command.isdigit():
            command = int(command)
            value = '0' + "{0:015b}".format(command)
            return value      #google: python string format
        else:
            if self.st.contains(command):
                return '0' + "{0:015b}".format(int(self.st.getAddress(command)))
            else:
                address = self.st.getNextVariableAddress()
                self.st.addEntry(command, address)
                return '0' + "{0:015b}".format(int(address))
    




#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable

if __name__=="__main__":

    target = sys.argv[1]         # uncomment this one and comment out the others,
                                   #   for final deliverable
    
    # target = 'add/Add.asm'       # for internal IDLE testing only
    # target = 'max/MaxL.asm'      # for internal IDLE testing only
    # target = 'max/Max.asm'       # for internal IDLE testing only
    # target = 'rect/RectL.asm'    # for internal IDLE testing only
    # target = 'rect/Rect.asm'     # for internal IDLE testing only
    # target = 'pong/PongL.asm'    # for internal IDLE testing only
    # target = 'pong/Pong.asm'     # for internal IDLE testing only

    assembler = Assembler(target)
    print('done parsing, assembled file is:', assembler.assemble())



