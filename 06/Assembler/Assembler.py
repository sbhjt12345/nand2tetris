#!/usr/bin/python3


from SymbolTable import *
from Parser import *
from Code import *
import sys


class Assembler:
    def __init__(self, file):
        self.st = SymbolTable()
        self.file = file
        self.address = 16

    def first_pass(self):
        ps = Parser(self.file)
        counter = 0
        while ps.hasMoreCommands():
            ps.advance()
            if ps.commandType() == A_COMMAND or ps.commandType() == C_COMMAND:
                counter += 1
            else:
                self.st.addEntry(ps.symbol(), counter)

    def second_pass(self):
        ps = Parser(self.file)
        if self.file.endswith('.asm'):
           psout = self.file.replace('.asm', '.hack')
        else:
            psout = self.file + '.hack'
        f = open(psout, 'w')
        while ps.hasMoreCommands():
            ps.advance()
            ctype = ps.commandType()
            if ctype == A_COMMAND:
                cur_address = self.helper_getOrDefault(ps.symbol())
                instruction = '{0:016b}'.format(cur_address)
            elif ctype == C_COMMAND:
                instruction = ''.join(['111', Code.comp(ps.comp()), Code.dest(ps.dest()), Code.jump(ps.jump())])
            else:
                continue
            f.write(instruction + '\n')
        f.close()

    def helper_getOrDefault(self, symbol):
        if symbol.isdigit():
            return int(symbol)
        else:
            if not self.st.contains(symbol):
                self.st.addEntry(symbol, self.address)
                self.address += 1
            return self.st.GetAddress(symbol)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)

    filename = sys.argv[1:]
    # filename = 'add.asm'
    print("this is the thing: \n")
    print(filename)
    ass = Assembler(filename[0])
    ass.first_pass()
    ass.second_pass()









