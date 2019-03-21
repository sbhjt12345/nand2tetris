#!/usr/bin/python3

from JackTokenizer import *
import sys


class CompilationEngine:
    def __init__(self, filepath):
        try:
            self.filepath = filepath
            self.tokenizer = JackTokenizer(filepath)
            self.tokenizer.output_t_xml()
            self.txml_reader = open(filepath.replace('.jack', 'T.xml'), 'r')
            self.txml_reader.readline()   # omit <token>
            self.output = filepath.replace('.jack', '.xml')
            self.indent_count = 0
            self.xml_writer = open(self.output, 'w')



            self.xml_writer.close()


        except FileNotFoundError:
            print("could not find %s" % filepath)

    def compile_class(self, tokens):
        syntax = '<class>\n' + \
                 self.write_tag() + \
                 '<keyword>' + tokens.pop(0) + '</keyword>\n' + \
                 '<identifier>' + tokens.pop(0) + '</identifier>\n' + \
                 '<symbol>' + tokens.pop(0) + '</symbol>'


    def write_tag(self, tag_name):
        syntax = self.write_indent() + '<%s>' % tag_name + '\n'
        self.xml_writer.write(syntax)
        self.indent_count += 1

    def write_indent(self):
        return '\t' * self.indent_count

    def write_next_token(self):
        syntax = self.write_indent() + self.txml_reader.readline()
        self.xml_writer.write(syntax)







