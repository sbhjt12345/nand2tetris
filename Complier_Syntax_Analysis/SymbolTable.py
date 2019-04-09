#!/usr/bin/python3

from JackTokenizer import *
import sys



class SymbolTable:
    counts = {'STATIC': 0,
              'FIELD': 0,
              'ARG': 0,
              'VAR': 0}
    class_sbt = {}

    def __init__(self):
        self.method_sbt = {}
        self.counts['FIELD'] = 0

    def start_subroutine(self):
        self.method_sbt = {}
        self.counts['ARG'] = 0
        self.counts['VAR'] = 0

    def define(self, name, type, kind):
        cur_id = self.var_count(kind)
        self.counts[name] += 1
        if kind == 'STATIC' or kind == 'FIELD':
            self.class_sbt[name] = (type, kind, cur_id)
        else:
            self.method_sbt[name] = (type, kind, cur_id)
        return

    def var_count(self, kind):
        return self.counts[kind]

    def kind_of(self, name):
        if name in self.method_sbt.keys():
            return self.method_sbt[name][1]
        elif name in self.class_sbt.keys():
            return self.class_sbt[name][1]
        return 'NONE'

    def type_of(self, name):
        if name in self.method_sbt.keys():
            return self.method_sbt[name][0]
        elif name in self.class_sbt.keys():
            return self.class_sbt[name][0]
        return 'NONE'

    def index_of(self, name):
        if name in self.method_sbt.keys():
            return self.method_sbt[name][2]
        elif name in self.class_sbt.keys():
            return self.class_sbt[name][2]
        return 'NONE'

