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
            self.cur_token = self.txml_reader.readline()   # omit <token>
            self.written = True
            self.output = filepath.replace('.jack', '.xml')
            self.indent_count = 0
            self.xml_writer = open(self.output, 'w')



            self.xml_writer.close()


        except FileNotFoundError:
            print("could not find %s" % filepath)

    def compile_class(self):
        self.write_tag('class')
        self.write_next_token()  # keyword class
        self.write_next_token()  # identifier className
        self.write_next_token()  # symbol {
        while 'static' in self.cur_token or 'field' in self.cur_token:
            self.compile_vardec()
        while 'constructor' in self.cur_token \
                or 'function' in self.cur_token \
                or 'method' in self.cur_token:
            self.compile_subroutinedec()







    def compile_vardec(self):
        self.write_tag('classVarDec')
        self.write_next_token()    # keyword field or static
        self.write_next_token()    # type
        self.write_next_token()    # identifier field name
        while ',' in self.cur_token:  # now that we read cur_token but havent written it, change self.written to false
            self.not_written_yet()
            self.write_next_token()  # symbol ,
            self.write_next_token()  # identifier field name
        self.not_written_yet()
        self.write_next_token()    # symbol ; cur_token is now next var or class body
        self.write_second_tag('classVarDec')

    def compile_subroutinedec(self):
        self.write_tag('subroutineDec')
        self.write_next_token()    # keyword cons, method or func
        self.write_next_token()    # type
        self.write_next_token()    # identifier subroutineName
        self.write_next_token()    # (, now self.token is either ) or type param
        while ')' not in self.token:
            self.not_written_yet()
            self.compile_parameter_list()
        self.not_written_yet()
        self.write_next_token()    # write ')'
        self.write_tag('subroutineBody')




        self.write_second_tag('subroutineBody')
        self.write_second_tag('subroutineDec')

    def compile_parameter_list(self):
        self.write_tag('parameterList')
        self.write_next_token()   # type
        self.write_next_token()   # identifier param name
        while ',' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()
            self.write_next_token()  # we get cur_token as ',' or ')'
        self.write_second_tag('parameterList')















    def is_var_dec(self):
        return






    def write_tag(self, tag_name):
        syntax = self.write_indent() + '<%s>' % tag_name + '\n'
        self.xml_writer.write(syntax)
        self.indent_count += 1

    def write_second_tag(self, tag_name):
        self.indent_count -= 1
        syntax = self.write_indent() + '</%s>' % tag_name + '\n'
        self.xml_writer.write(syntax)

    def write_indent(self):
        return '\t' * self.indent_count

    """
    write current token into xml_writer,
    then get the next token as the current token.
    Therefore, if current token is written, then cur_token = next token to be processed
    else, write the current token.
    """
    def write_next_token(self):
        if self.written:
            self.cur_token = self.txml_reader.readline()
        else:
            self.written = True
        self.xml_writer.write(self.write_indent() + self.cur_token)

    def not_written_yet(self):
        self.written = False









