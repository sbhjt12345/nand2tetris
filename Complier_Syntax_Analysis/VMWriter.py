#!/usr/bin/python3


class VMWriter:
    def __init__(self, filepath):
        self.output = filepath

    def write_push(self, segment, index):
        if segment == 'ARG':
            segment = 'argument'
        elif segment == 'CONST':
            segment = 'constant'
        self.output.write('push {} {}\n'.format(segment.lower(), index))

    def write_pop(self, segment, index):
        if segment == 'ARG':
            segment = 'argument'
        elif segment == 'CONST':
            segment = 'constant'
        self.output.write('pop {} {}\n'.format(segment.lower(), index))

    def write_arithmetic(self, command):
        self.output.write(command.lower() + '\n')

    def write_label(self, label):
        self.output.write('label {}'.format(label))

    def write_goto(self, label):
        self.output.write('goto {}'.format(label))

    def write_if(self, label):
        self.output.write('if-goto {}'.format(label))

    def write_call(self, name, nArgs):
        self.output.write('call {} {}\n'.format(name, nArgs))

    def write_function(self, name, nLocals):
        self.output.write('function {} {}\n'.format(name, nLocals))

    def write_return(self):
        self.output.write('return\n')

    def close(self):
        self.output.close()




