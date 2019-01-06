#!/usr/bin/python3

import sys
from Parser import *

class CodeWriter:
    def __init__(self, vm_file):
        self.vm_file = vm_file
        self.label = 0

    def setFileName(self, filename):
        filename.write()

    def get_next_label(self):
        self.label += 1
        return str(self.label)


    # push/pop segment index

    def WritePushPop(self, command, segment, index):
        return ""

    def writeArithmetic(self, command):
        res = ''
        if command == 'eq':
            pass
        elif command == 'and':
            res = (res +
                   '@SP\n' +
                   'AM = M - 1\n' +
                   'D = M\n' +
                   'A = A - 1\n' +
                   'M = D&M\n\n')
        elif command == 'or':
            res = (res +
                   '@SP\n' +
                   'AM = M - 1\n' +
                   'D = M\n' +
                   'A = A - 1\n' +
                   'M = D|M\n\n')
        elif command == 'not':
            res = (res +
                   '@SP\n' +
                   'AM = M - 1\n' +
                   'M = !M\n\n')
        elif command == 'eq':
            num1 = 'EQTRUE%s' % self.get_next_label()
            num2 = 'EQAFTER%s' % self.get_next_label()
            res = (res +
                   '@SP\n' +
                   'AM = M - 1\n' +
                   'D = M\n' +
                   'A = A - 1\n' +
                   'D = D - M\n' +
                   '@' + num1 + '\n' +
                   'D;JEQ\n' +
                   '@SP\n' +
                   'A = M - 1\n' +
                   'M = 0\n' +
                   '@' + num2 + '\n' +
                   '0;JMP\n' +
                   '('+ num1 + ')\n' +
                   '@SP\n' +
                   'A = M - 1\n' +
                   'M = -1\n' +
                   '(' + num2 + ')\n\n')

        return ""


    def translate_file(self):
        ps = Parser(self.vm_file)
        if self.vm_file.endswith('.vm'):
            asm_file = self.file.replace('.vm', '.asm')
        else:
            asm_file = self.file + '.vm'

        asm_writer = open(asm_file, 'w')
        while ps.hasMoreCommands():
            ps.advance()
            ctype = ps.commandType()
            if ctype == 'C_ARITHMETIC':
                asm_writer.write(self.writeArithmetic(ps.command))
            else:
                pass
        asm_writer.close()










            

