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
            #self.not_written_yet()   # keep static/field as cur_token
            self.compile_var_dec('classVarDec')
        while 'constructor' in self.cur_token \
                or 'function' in self.cur_token \
                or 'method' in self.cur_token:
            self.not_written_yet()  # keep the keyword
            self.compile_subroutinedec()

    def compile_var_dec(self, tagname):
        self.write_tag(tagname)
        while ';' not in self.cur_token:
            self.not_written_yet()
            self.write_next_token()
        self.not_written_yet()
        self.write_next_token()
        self.write_second_tag(tagname)

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
        self.write_next_token()    # write '{', cur_token is var if var exists
        while 'var' in self.cur_token:
            self.compile_var_dec('varDec')  # after this step, we get first word of statement as cur_token
        self.compile_statements()
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

    def compile_statements(self):
        if 'let' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()   # write let, cur_token is varName
            self.write_next_token()
            if '[' in self.cur_token:
                self.not_written_yet()
                self.write_next_token() # now cur_token is the first in expressions
                self.compile_expressions()




        elif 'if' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()

        elif 'while' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()

        elif 'do' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()

        elif 'return' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()

    """
    expression is: term (op term)*
    """
    def compile_expressions(self):
        self.write_tag('expression')
        self.compile_term()
        while re.search(r'>(\+|-|\*|/|&amp;|\||&lt;|&gt;|=)<', self.cur_token):
            self.not_written_yet()
            self.write_next_token()
            self.compile_term()
        self.write_second_tag('expression')

    """
    term is: integerCons|stringCons|keywordCons|varName|varName '['expression']'|subroutineCall
    |'('expression')'|unaryOp term
    unaryOp is '-'
    subroutineCall is: subroutineName '('expressionList')' | 
    (className|varName)'.'subroutineName'('expressionList')'
    expressionList is : (expression(',' expression)*)?
    """
    def compile_term(self):
        self.write_tag('term')
        self.not_written_yet()
        if re.search(r'>(~|-)<', self.cur_token):
            self.write_next_token()  # deal with unary op
            self.compile_term()
        elif '(' in self.cur_token:
            self.write_next_token()   # '('
            self.compile_expressions()
            self.write_next_token()
        else:
            self.write_next_token()
            self.not_written_yet()
            if '[' in self.cur_token():
                self.write_next_token()
                self.compile_expressions()
                self.write_next_token()  # write ']'
            elif '.' in self.cur_token():
                self.write_next_token()
                self.write_next_token()  # subroutineName
                self.write_next_token()  # '('
                self.compile_expression_list()
                self.write_next_token()
            else:
                self.write_next_token()
                self.compile_expression_list()
                self.write_next_token()
        self.write_second_tag('term')

    def compile_expression_list(self):
        self.write_tag('expressionList')
        self.not_written_yet()
        if ')' not in self.cur_token:   # meaning expression list is not empty
            self.compile_expressions()  #TODO find out if it really goes to next token
        while ')' not in self.cur_token:
            self.not_written_yet()
            self.write_next_token()
            self.compile_expressions()
        self.write_second_tag('expressionList')































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









