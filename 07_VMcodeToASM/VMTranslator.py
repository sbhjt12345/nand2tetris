#!/usr/bin/python3

import sys
from Parser import *
import os


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

    def write_bootstrap(self):
        res = ''
        res += ('@256\n' +
                'D=A\n' +
                '@SP\n' +
                'M=D' +
                self.write_call('call Sys.init 0'))
        return res

    def write_label(self, command):
        res = ''
        addr = self.vm_file.split('/')
        label_name = command.split(' ')[1]
        res += '(' + addr[len(addr) - 1].replace('.vm', '$' + label_name) + ')\n'
        return res

    def write_goto(self, command):
        res = ''
        addr = self.vm_file.split('/')
        label_name = command.split(' ')[1]
        print("the command is :" + command + ", and the label name is " + label_name)
        res += '@' + addr[len(addr) - 1].replace('.vm', '$' + label_name) + '\n0;JMP\n'
        print(res)
        return res

    def write_if(self, command):
        res = ''
        addr = self.vm_file.split('/')
        label_name = command.split(' ')[1]
        res += ('@SP\n' +
                'AM=M-1\n' +
                'D=M\n' +
                '@' + addr[len(addr) - 1].replace('.vm', '$' + label_name) + '\n' +
                'D;JGT\n')
        return res

    def write_function(self, command):
        res = ''
        addr = self.vm_file.split('/')
        function_elements = command.split(' ')
        res += '(' + function_elements[1] + ')\n'
        k = int(function_elements[2])
        tmp_command = 'push constant 0'
        for i in range(0, k):
            res += self.write_push(tmp_command)
        return res

    def write_call(self, command):
        res = ''
        call_elements = command.split(' ')
        #print(call_elements)
        num_args = int(call_elements[2])
        push_end_syntax = ('@SP\n' +
                           'A=M\n' +
                           'M=D\n' +
                           '@SP\n' +
                           'M=M+1\n')
        return_address = self.write_label('label RETADD' + call_elements[2])
        return_asm = return_address.replace('(', '').replace(')', '')
        res += ('@' + return_asm + '\n' +
                'D=A\n' +
                push_end_syntax +
                '@LCL\n' +
                'D=M\n' +
                push_end_syntax +
                '@ARG\n' +
                'D=M\n' +
                push_end_syntax +
                '@THIS\n' +
                'D=M\n' +
                push_end_syntax +
                '@THAT\n' +
                'D=M\n' +
                push_end_syntax +
                'D=M\n' +
                '@' + str(num_args + 5) + '\n'
                'D=D-A\n' +
                '@ARG\n' +
                'M=D\n' +
                '@SP\n' +
                'D=M\n' +
                '@LCL\n' +
                self.write_goto('goto ' + call_elements[1]) +
                return_address
                )
        return res

    def write_return(self):
        res = ''
        res += ('@LCL\n' +
                'D=M\n' +
                '@FRAME\n' +
                'M=D\n' +
                '@5\n' +
                'A=D-A\n' +
                'D=M\n' +
                '@RET\n' +
                'M=D\n' +
                '@SP\n' +
                'AM=M-1\n' +
                'D=M\n' +
                '@ARG\n' +
                'A=M\n' +
                'M=D\n' +
                '@ARG\n' +
                'D=M+1\n' +
                '@SP\n' +
                'M=D\n' +
                self.return_helper(1, 'THAT') +
                self.return_helper(2, 'THIS') +
                self.return_helper(3, 'ARG') +
                self.return_helper(4, 'LCL') +
                '@RET\n' +
                'A=M\n' +
                '0;JMP\n\n')
        return res

    def return_helper(self, k, seg):
        frame_asm = ('@FRAME\n' +
                     'D=M\n' +
                     '@' + str(k) + '\n' +
                     'D=D-A\n' +
                     'A=D\n' +
                     'D=M\n' +
                     '@' + seg + '\n' +
                     'M=D\n')
        return frame_asm

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


class FileTranslator:
    def __init__(self, file_list, file_or_dir_abs_path):
        self.file_list = file_list  # every file in this file list is abs path
        self.file_or_dir_abs_path = file_or_dir_abs_path

    def is_dir(self):
        if self.file_or_dir_abs_path.endswith('.vm'):
            return False
        else:
            return True

    def process_files(self):
        if self.is_dir():
            asm_file = self.file_or_dir_abs_path + '.asm'
        else:
            asm_file = self.file_or_dir_abs_path.replace('.vm', '.asm')
        asm_writer = open(asm_file, 'w')
        for file in self.file_list:
            self.translate_file(file, asm_writer)
        print('its finished!')
        asm_writer.close()

    def translate_file(self, file, asm_writer):
        ps = Parser(file)
        vm_trans = CodeWriter(file)
        while ps.hasMoreCommands():
            ps.advance()
            ctype = ps.commandType()
            if ctype == 'C_ARITHMETIC':
                asm_writer.write(vm_trans.writeArithmetic(ps.command))
            elif ctype == 'C_LABEL':
                asm_writer.write(vm_trans.write_label(ps.command))
            elif ctype == 'C_GOTO':
                asm_writer.write(vm_trans.write_goto(ps.command))
            elif ctype == 'C_IF':
                asm_writer.write(vm_trans.write_if(ps.command))
            elif ctype == 'C_FUNCTION':
                asm_writer.write(vm_trans.write_function(ps.command))
            elif ctype == 'C_CALL':
                asm_writer.write(vm_trans.write_call(ps.command))
            elif ctype == 'C_RETURN':
                asm_writer.write(vm_trans.write_return())
            else:
                asm_writer.write(vm_trans.writePushPop(ps.command))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)
    filepath = sys.argv[1:][0]
    file_split_list = filepath.split('/')
    if file_split_list[len(file_split_list)-1].endswith('.vm'):
        ft = FileTranslator([filepath], filepath)
    else:
        file_path_list = []
        for root, _, files in os.walk(filepath):
            file_path_list = [os.path.abspath(os.path.join(root, f)) for f in files if f.endswith('.vm')]
        vm_file_name = file_split_list[len(file_split_list)-1]
        ft = FileTranslator(file_path_list, filepath + '/' + vm_file_name)
    ft.process_files()
















            

