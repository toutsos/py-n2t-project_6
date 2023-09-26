#
#Parser.py
#
# CS2001   Project 6 Assembler

# 31 July 2013
# last updated 21 Sept 2021
#
# start code version
#

'''Manages the mechanical work of breaking the input into tokens, and later further breaking
   down presented tokens into component chunks.  The Parser does not know what the chunks mean
   or what to do with them, it just knows how to slice-and-dice. '''

class Parser(object):

    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

##########################################
#Constructor

    def __init__(self, fileName):
        loadedList = self.__loadFile(fileName)
        
        self.toParse = self.__filterFile(loadedList)

        #self.__toTestDotTxt()


##########################################
#public Methods

    def advance(self):
        '''reads and returns the next command in the input,
           returns false if there are no more commands.  '''
        try:
            return next(self.iter)
        except StopIteration:
            return False


    def create_toParse_iterrator(self):
        self.iter = iter(self.toParse)



    def commandType(self, command):
        ''' returns type of the command
            Parser.A_COMMAND   @xxx
         or Parser.C_COMMAND   c-commands
         or Parser.L_COMMAND   a label e.g. (LABEL)
        '''
        result = 0   #initialized to a tattle-tail value
        
        if(command.startswith('(')):
            return self.L_COMMAND;
        elif (command.startswith('@')):
            return self.A_COMMAND;
        else:
            return self.C_COMMAND;

        return result



    def symbol(self, command):
        ''' returns
             symbol or decimal of an A-command
          or symbol of a label'''
        
        type = self.commandType(command)
        if type == 1 :
            result =  command[1:]
        elif type == 3:
            index = command.find(')')
            result = command[1:index]
        else:
            #eliminate silent failures wherever possible
            raise RuntimeError("Error!!! parse.symbol(): We should never parse a symbol from a C_COMMAND")
            result = None
        
        return result



    def dest(self, command):
        ''' returns the dest mnemonic portion of the command '''

        #TODO  complete this function
        pass

    
    def comp(self, command):
        ''' returns the comp mnemonic portion of the command '''
        
        #TODO  complete this function
        pass


    
    def jump(self, command):
        ''' returns the jmp mnemonic portion of the command '''

        #TODO  complete this function
        pass


    def command_separation (self,command):
        # Return a tuple with the 3 parts of C - Instruction, I didn't use the 3 separates methods because
        # I had to search 3 times if equality exists.
        index_of_equality = command.find('=')
        if index_of_equality < 0:
            index_of_semicolon = command.find(';')
            cmd = command[:index_of_semicolon]
            jmp = command[index_of_semicolon + 1:]
            dest = 'null'
        else:
            dest = command[:index_of_equality]
            cmd = command[index_of_equality + 1:]
            jmp = 'null'

        return cmd,dest,jmp

    def processLabels(self):
        ''' Passes over the list of commands and removes labels from the code being parsed.
            As labels are identified they are added to a dictionary of <label, romAddress>
            pairs.  After passing over the entire file the dictionary is returned. '''        
        labels = dict()
        label_list = []

        for num, line in enumerate(self.toParse):
            type_of_command = self.commandType(line)
            if type_of_command == 3:
                label_list.append(line)
                label = self.symbol(line)
                labels[label] = num

        # Remove Labels from toParse list
        for key in label_list:
            index = self.toParse.index(key)
            self.toParse.pop(index)

        return labels 



##########################################
#private/local Methods



    def __toTestDotTxt(self):
        '''this is just for outputting our stripped file as a test
           this function will not be active in the final program'''

        file = open("test.txt","w")
        file.write("\n".join(self.toParse))
        file.close() 



    def __loadFile(self, fileName):
        '''Loads the file into memory.
           -fileName is a String representation of a file name,
           returns contents as a simple List.'''

        with open(fileName,'r') as my_file :
            fileList = my_file.read().split("\n");

        return fileList   



    def __filterFile(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''

        filteredList = []

        for line in fileList:
            line = self.__filterOutEOLComments(line)
            line = line.strip()
            if len(line) != 0:
                filteredList.append(line)
        
        return filteredList   



    def __filterOutEOLComments(self, line):
        '''Removes end-of-line comments.

           -line is a string representing single line
           returns the filtered line, which may be empty'''

        index = line.find('//')
        if index >= 0:
            line = line[:index]

        return line    

            
