#!/usr/bin/python3

import sys
from Parser import *


class CodeWriter:
    def __init__(self, vm_file):
        self.vm_file = vm_file
        self.label = 0
        self.segmentTable = {'local': '@LCL',
                             'this': '@THIS',
                             'argument': '@ARG',
                             'that': '@THAT',
                             'temp': '@R5',
                             'pointer0': '@THIS',
                             'pointer1': '@THAT'}

    def get_next_label(self):
        self.label += 1
        return 'LABEL' + str(self.label)

    # push/pop segment index

    def writePushPop(self, command):
        order = command.split(' ')[0]
        if order == 'push':
            return self.write_push(command)
        else:
            return self.write_pop(command)

    def write_push(self, command):
        res = ''
        arg_list = command.split(' ')
        segment = arg_list[1]
        index = arg_list[2]
        if segment == 'pointer':
            segment += index
        push_end_syntax = ('@SP\n' +
                           'A=M\n' +
                           'M=D\n' +
                           '@SP\n' +
                           'M=M+1\n\n')

        if segment in ['local', 'argument', 'this', 'that']:
            res += (self.segmentTable[segment] + '\n' +
                    'D=M\n' +
                    '@' + index + '\n' +
                    'A=D+A\n' +
                    'D=M\n' +
                    push_end_syntax)

        elif segment in ['pointer0', 'pointer1']:
            res += (self.segmentTable[segment] + '\n' +
                    'D=M\n' +
                    push_end_syntax)

        elif segment == 'temp':
            res += (self.segmentTable[segment] + '\n' +
                    'D=A\n' +
                    '@' + index + '\n' +
                    'A=D+A\n' +
                    'D=M\n' +
                    push_end_syntax)

        elif segment == 'constant':
            res += ('@' + index + '\n' +
                    'D=A\n' +
                    push_end_syntax)

        elif segment == 'static':
            addr = self.vm_file.split('/')
            file_name = addr[len(addr) - 1].replace('.vm', '.' + index)
            res += ('@' + file_name + '\n' +
                    'D=M\n' +
                    push_end_syntax)
        return res

    def write_pop(self, command):
        res = ''
        arg_list = command.split(' ')
        segment = arg_list[1]
        index = arg_list[2]
        if segment == 'pointer':
            segment += index
        pop_end_syntax = ('@R13\n' +
                          'M=D\n' +
                          '@SP\n' +
                          'AM=M-1\n' +
                          'D=M\n' +
                          '@R13\n' +
                          'A=M\n' +
                          'M=D\n\n')
        if segment in ['local', 'argument', 'this', 'that']:
            res += (self.segmentTable[segment] + '\n' +
                    'D=M\n' +
                    '@' + index + '\n' +
                    'D=D+A\n' +
                    pop_end_syntax)
        elif segment in ['pointer0', 'pointer1']:
            res += (self.segmentTable[segment] + '\n' +
                    'D=A\n' +
                    pop_end_syntax)
        elif segment == 'temp':
            res += (self.segmentTable[segment] + '\n' +
                    'D=A\n' +
                    '@' + index + '\n' +
                    'D=D+A\n' +
                    pop_end_syntax)
        elif segment == 'constant':
            res += ('@' + index + '\n' +
                    'D=A\n' +
                    pop_end_syntax)
        elif segment == 'static':
            addr = self.vm_file.split('/')
            file_name = addr[len(addr) - 1].replace('.vm', '.' + index)
            res += ('@' + file_name + '\n' +
                    'D=A\n' +
                    pop_end_syntax)
        return res

    def writeArithmetic(self, command):
        res = ''
        if command == 'and':
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
                   'A = M - 1\n' +
                   'M = !M\n\n')
        elif command == 'eq' or command == 'lt' or command == 'gt':
            res = self.write_compare(res, command)
        elif command == 'add' or command == 'sub':
            res = self.write_cal(res, command)
        elif command == 'neg':
            res = (res +
                   '@SP\n' +
                   'A = M - 1\n' +
                   'M = -M\n\n'
                   )
        return res

    def write_compare(self, res, command):
        num1 = 'EQTRUE%s' % self.get_next_label()
        num2 = 'EQAFTER%s' % self.get_next_label()
        res = (res +
               '@SP\n' +
               'AM = M - 1\n' +
               'D = M\n' +
               'A = A - 1\n' +
               'D = M - D\n' +
               '@' + num1 + '\n' +
               'D;J' + command.upper() + '\n' +
               '@SP\n' +
               'A = M - 1\n' +
               'M = 0\n' +
               '@' + num2 + '\n' +
               '0;JMP\n' +
               '(' + num1 + ')\n' +
               '@SP\n' +
               'A = M - 1\n' +
               'M = -1\n' +
               '(' + num2 + ')\n\n')
        return res

    def write_cal(self, res, command):
        if command == 'add':
            tmp_str = 'M = M + D\n\n'
        else:
            tmp_str = 'M = M - D\n\n'
        res = (res +
               '@SP\n' +
               'AM = M - 1\n' +
               'D = M\n' +
               'A = A - 1\n' +
               tmp_str
               )
        return res

    def translate_file(self):
        ps = Parser(self.vm_file)
        if self.vm_file.endswith('.vm'):
            asm_file = self.vm_file.replace('.vm', '.asm')
        else:
            asm_file = self.vm_file + '.asm'

        asm_writer = open(asm_file, 'w')
        while ps.hasMoreCommands():
            ps.advance()
            ctype = ps.commandType()
            if ctype == 'C_ARITHMETIC':
                asm_writer.write(self.writeArithmetic(ps.command))
            else:
                asm_writer.write(self.writePushPop(ps.command))
        print('its finished!')
        asm_writer.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)

    filename = sys.argv[1:]
    # filename = 'add.asm'
    print("this is the thing: \n")
    print(filename)
    vm_trans = CodeWriter(filename[0])
    vm_trans.translate_file()











            

