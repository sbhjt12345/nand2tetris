#!/usr/bin/python3

import re

A_COMMAND = 'A'
C_COMMAND = 'C'
L_COMMAND = 'L'


class Parser:
    def __init__(self, filepath):
        try:
            with open(filepath, 'r') as f:
                self.commands = list(filter(len, [re.sub('//.*$', '', line).strip() for line in f]))
        except FileNotFoundError:
            print("could not find %s" % filepath)

    def hasMoreCommands(self):
        return len(self.commands) > 0

    def advance(self):
        if self.hasMoreCommands():
            self.command = self.commands.pop(0)

    def commandType(self):
        if self.command[0] == '@':
            return A_COMMAND
        elif self.command[0] == '(' and self.command[-1] == ')':
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.commandType() == A_COMMAND:
            return self.command[1:]
        elif self.commandType() == L_COMMAND:
            return self.command[1:-1]

    def dest(self):
        try:
            index = self.command.index('=')
            return self.command.split('=')[0]
        except ValueError:
            return ''

    def comp(self):
        return self.command.split('=')[-1].split(';')[0]

    def jump(self):
        if self.command.find(';') != -1:
            return self.command.split('=')[-1].split(';')[-1]
        return ''
















            

