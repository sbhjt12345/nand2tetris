#!/usr/bin/python3

import re



class Parser:
    def __init__(self, filepath):
        try:
            with open(filepath, 'r') as f:
                self.commands = list(filter(None, [re.sub('//.*$', '', line).strip() for line in f]))
        except FileNotFoundError:
            print('could not find %s' % filepath)

        self.cType = {
            'add': 'C_ARITHMETIC', 'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC', 'eq': 'C_ARITHMETIC',
            'gt': 'C_ARITHMETIC', 'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC', 'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC', 'push':'C_PUSH',
            'pop': 'C_POP', 'label': 'C_LABEL',
            'goto': 'C_GOTO', 'if-goto': 'C_IF',
            'function': 'C_FUNCTION', 'return': 'C_RETURN',
            'call': 'C_CALL'
        }

    def hasMoreCommands(self):
        return len(self.commands) > 0

    def advance(self):
        if self.hasMoreCommands():
            self.command = self.commands.pop(0)

    def commandType(self):
        type = self.command.split(' ')[0]
        return self.cType[type]





