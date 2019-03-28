#!/usr/bin/python3

from JackTokenizer import *
import sys


class CompilationEngine:
    def __init__(self, filepath):
        try:
            self.filepath = filepath
            self.txml_output = filepath.replace('.jack', 'T.xml')
            self.txml_reader = open(self.txml_output, 'r')
            self.cur_token = self.txml_reader.readline()   # omit <token>
            self.written = True
            self.output = filepath.replace('.jack', '.xml')
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
        self.mix_two()
        while 'static' in self.cur_token or 'field' in self.cur_token:
            self.compile_var_dec('classVarDec')
        while 'constructor' in self.cur_token \
                or 'function' in self.cur_token \
                or 'method' in self.cur_token:
            self.compile_subroutinedec()
        self.mix_two()
        self.write_second_tag('class')

    def compile_var_dec(self, tagname):
        self.write_tag(tagname)
        while ';' not in self.cur_token:
            self.write_next_token()
            self.not_written_yet()
        self.write_next_token()
        self.not_written_yet()    # written = false, go to next element
        self.write_second_tag(tagname)

    def compile_subroutinedec(self):
        self.write_tag('subroutineDec')
        self.write_next_token()    # keyword cons, method or func
        self.write_next_token()    # type
        self.write_next_token()    # identifier subroutineName
        self.mix_two()             # write ( and get next
        self.compile_parameter_list()
        self.mix_two()
        self.write_tag('subroutineBody')
        self.mix_two()
        while 'var' in self.cur_token:
            self.compile_var_dec('varDec')  # after this step, we get first word of statement as cur_token
        self.compile_statements()           # when enter this step, cut_token is first element of statements
        self.mix_two()
        self.write_second_tag('subroutineBody')
        self.write_second_tag('subroutineDec')

    def compile_parameter_list(self):
        self.write_tag('parameterList')
        while ')' not in self.cur_token:
            self.write_next_token()
            self.not_written_yet()
        self.write_second_tag('parameterList')

    def compile_statements(self):
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
        self.write_second_tag('statements')

    def compile_let_statement(self):
        self.write_tag('letStatement')
        self.write_next_token()
        self.mix_two()
        if '[' in self.cur_token:
            self.mix_two()
            self.compile_expressions()
            self.write_next_token()  # write ']'
        self.mix_two()
        self.compile_expressions()
        self.mix_two()
        self.write_second_tag('letStatement')

    def compile_if_statement(self):
        self.write_tag('ifStatement')
        self.write_next_token()   # write if and get '('
        self.mix_two()
        self.compile_expressions()
        self.write_next_token()   # write ')'
        self.mix_two()
        self.compile_statements()
        self.mix_two()
        if 'else' in self.cur_token:
            self.write_next_token()   # write else
            self.mix_two()
            self.compile_statements()
            self.mix_two()
        self.write_second_tag('ifStatement')

    def compile_while_statement(self):
        self.write_tag('whileStatement')
        self.write_next_token()   # write while
        self.mix_two()
        self.compile_expressions()
        self.write_next_token()   # write )
        self.mix_two()
        self.compile_statements()
        self.mix_two()
        self.write_second_tag('whileStatement')

    def compile_do_statement(self):
        self.write_tag('doStatement')
        self.write_next_token()  # do
        self.mix_two()
        if '.' in self.cur_token:
            self.write_next_token()  # write '.', true
            self.write_next_token()  # get and write subroutineName
        self.mix_two()
        self.compile_expression_list()
        self.write_next_token()      # write )
        self.mix_two()               # write ;
        self.write_second_tag('doStatement')

    def compile_return_statement(self):
        self.write_tag('returnStatement')
        self.mix_two()
        if ';' not in self.cur_token:
            self.compile_expressions()
        self.mix_two()
        self.write_second_tag('returnStatement')

    """
    expression is: term (op term)*
    """
    def compile_expressions(self):
        self.write_tag('expression')
        self.compile_term()
        while re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', self.cur_token):
            self.mix_two()
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
        if re.search(r'> (~|-) <', self.cur_token):
            self.mix_two()
            self.compile_term()
        elif '(' in self.cur_token:
            self.mix_two()
            self.compile_expressions()
            self.mix_two()
        else:
            self.mix_two()
            if '[' in self.cur_token:
                self.mix_two()
                self.compile_expressions()
                self.mix_two()
            elif '.' in self.cur_token:
                self.write_next_token()  # write '.', true
                self.write_next_token()  # get and write subroutineName
                self.mix_two()
                self.compile_expression_list()
                self.mix_two()
            elif '(' in self.cur_token:
                self.mix_two()
                self.compile_expression_list()
                self.mix_two()
        self.write_second_tag('term')

    def compile_expression_list(self):
        self.write_tag('expressionList')
        self.not_written_yet()    # get the first element of expression list
        if ')' not in self.cur_token:   # meaning expression list is not empty
            self.compile_expressions()  #TODO find out if it really goes to next token
        while ')' not in self.cur_token:
            self.mix_two()
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
        return '  ' * self.indent_count

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
        if self.written:
            self.cur_token = self.txml_reader.readline()
        self.written = False

    def mix_two(self):
        self.write_next_token()
        self.not_written_yet()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)

    filename = sys.argv[1:]
    print("this is the thing: \n")
    jtk = CompilationEngine(filename[0])









