#!/usr/bin/python3

from JackTokenizer import *
import sys


class CompilationEngine:
    def __init__(self, filepath):
        try:
            self.filepath = filepath
            self.txml_reader = open(filepath, 'r')
            self.cur_token = self.txml_reader.readline()   # omit <token>
            self.written = True
            self.output = filepath.replace('T.xml', 'M.xml')
            self.indent_count = 0
            self.xml_writer = open(self.output, 'w')
            self.compile_class()
            self.txml_reader.close()
            self.xml_writer.close()
        except FileNotFoundError:
            print("could not find %s" % filepath)

    def compile_class(self):
        self.write_tag('class')
        self.write_next_token()  # keyword class
        self.write_next_token()  # identifier className
        self.write_next_token()  # symbol {
        self.not_written_yet()
        while 'static' in self.cur_token or 'field' in self.cur_token:
            self.compile_var_dec('classVarDec')
        while 'constructor' in self.cur_token \
                or 'function' in self.cur_token \
                or 'method' in self.cur_token:
            self.not_written_yet()  # keep the keyword
            self.compile_subroutinedec()

    def compile_var_dec(self, tagname):
        print('we are in compile var_dec')
        self.write_tag(tagname)
        while ';' not in self.cur_token:
            #self.not_written_yet()
            self.write_next_token()
            self.not_written_yet()
        self.write_next_token()
        self.not_written_yet()    # written = false, go to next element
        self.write_second_tag(tagname)

    def compile_subroutinedec(self):
        print('we are in subroutine dec')
        self.write_tag('subroutineDec')
        self.write_next_token()    # keyword cons, method or func
        self.write_next_token()    # type
        self.write_next_token()    # identifier subroutineName
        self.write_next_token()    # (, now self.token is either ) or type param
        self.not_written_yet()     # go to next token, written is false
        if ')' not in self.cur_token:
            self.compile_parameter_list()
        self.write_next_token()    # write ')'
        self.not_written_yet()     # go to the first element in subroutineBody
        self.write_tag('subroutineBody')
        self.write_next_token()    # write '{'
        self.not_written_yet()     # cur_token is var if var exists
        while 'var' in self.cur_token:
            self.compile_var_dec('varDec')  # after this step, we get first word of statement as cur_token
        self.compile_statements()           # when enter this step, cut_token is first element of statements
        self.write_second_tag('subroutineBody')
        self.write_second_tag('subroutineDec')

    def compile_parameter_list(self):
        print('we are in param list')
        self.write_tag('parameterList')
        while ')' not in self.cur_token:
            self.write_next_token()
            self.not_written_yet()
        self.write_second_tag('parameterList')

    def compile_statements(self):
        print('we are in statements')
        self.write_tag('statements')
        while 'let' in self.cur_token \
                or 'if' in self.cur_token \
                or 'while' in self.cur_token \
                or 'do' in self.cur_token \
                or 'return' in self.cur_token:
            if 'let' in self.cur_token:
                self.compile_let_statement()
            elif 'if' in self.cur_token:
                self.compile_if_statement()
            elif 'while' in self.cur_token:
                self.compile_while_statement()
            elif 'do' in self.cur_token:
                self.compile_do_statement()
            elif 'return' in self.cur_token:
                self.compile_return_statement()

    def compile_let_statement(self):
        self.write_tag('letStatement')
        self.write_next_token()  # write let
        self.not_written_yet()   # cur_token is varName
        self.write_next_token()  # write varName
        self.not_written_yet()   # cur_token is '[' or '='
        if '[' in self.cur_token:
            self.write_next_token()  # write '['
            self.not_written_yet()   # cur_token is first element in expression
            self.compile_expressions()
            self.write_next_token()  # write ']'
        self.write_next_token()
        self.compile_expressions()
        self.write_next_token()
        self.write_second_tag('letStatement')

    def compile_if_statement(self):
        self.write_tag('ifStatement')
        self.not_written_yet()
        self.write_next_token()  # write if
        self.write_next_token()
        self.compile_expressions()
        self.write_next_token()
        self.write_next_token()
        self.compile_statements()
        self.write_next_token()
        if 'else' in self.cur_token:
            self.not_written_yet()
            self.write_next_token()
            self.write_next_token()
            self.compile_statements()
            self.write_next_token()
        self.write_second_tag('ifStatement')

    def compile_while_statement(self):
        self.write_tag('whileStatement')
        self.not_written_yet()
        self.write_next_token()  # write while
        self.write_next_token()
        self.compile_expressions()
        self.write_next_token()
        self.write_next_token()
        self.compile_statements()
        self.write_next_token()
        self.write_second_tag('whileStatement')

    def compile_do_statement(self):
        self.write_tag('doStatement')
        self.not_written_yet()
        self.write_next_token()  # do
        self.write_next_token()  # subroutineName or varName
        self.not_written_yet()
        if '.' in self.cur_token:
            self.write_next_token()
            self.write_next_token()  # subroutineName
            self.write_next_token()  # '('
            self.compile_expression_list()
            self.write_next_token()
        else:
            self.write_next_token()
            self.compile_expression_list()
            self.write_next_token()
        self.write_next_token()
        self.write_second_tag('doStatement')

    def compile_return_statement(self):
        self.write_tag('returnStatement')
        self.not_written_yet()
        self.write_next_token()  # return
        if ';' not in self.cur_token:
            self.not_written_yet()
            self.compile_expressions()
        self.write_next_token()
        self.write_second_tag('returnStatement')

    """
    expression is: term (op term)*
    """
    def compile_expressions(self):
        self.write_tag('expression')
        self.compile_term()
        while re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', self.cur_token):
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
        if re.search(r'> (~|-) <', self.cur_token):
            self.write_next_token()  # deal with unary op
            self.compile_term()
        elif '(' in self.cur_token:
            self.write_next_token()   # '('
            self.compile_expressions()
            self.write_next_token()
        else:
            self.write_next_token()
            self.not_written_yet()
            if '[' in self.cur_token:
                self.write_next_token()
                self.compile_expressions()
                self.write_next_token()  # write ']'
            elif '.' in self.cur_token:
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
        print(self.cur_token)
        self.xml_writer.write(self.write_indent() + self.cur_token)

    def not_written_yet(self):
        if self.written:
            self.cur_token = self.txml_reader.readline()
        self.written = False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)

    filename = sys.argv[1:]
    print("this is the thing: \n")
    jtk = CompilationEngine(filename[0])









