#!/usr/bin/python3

import re
import sys

COMMENT_RE = r'(//(.*))|(/\*(.*?)\*/)'
KEYWORD_RE = r'(class)|(constructor)|(function)|(method)|(field)|(static)|(var)|(int)|' + \
             r'(char)|(boolean)|(void)|(true)|(false)|(null)|(this)|(let)|(do)|(if)|(else)|' + \
             r'(while)|(return)'
SYMBOL_RE = r'\(|\)|\{|\}|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~'
INTEGER_CONSTANT_RE = r'\d+'
STRING_CONSTANT_RE = r'"[^("|\n)]*"'
IDENTIFIER_RE = r'[^\d]\w*'
RE_LIST = [KEYWORD_RE, SYMBOL_RE, INTEGER_CONSTANT_RE, STRING_CONSTANT_RE, IDENTIFIER_RE]
LEXICAL_MAP = {
    KEYWORD_RE: 'keyword',
    SYMBOL_RE: 'symbol',
    INTEGER_CONSTANT_RE: 'integerConstant',
    STRING_CONSTANT_RE: 'stringConstant',
    IDENTIFIER_RE: 'identifier'
}


class JackTokenizer:
    def __init__(self, filepath):
        try:
            self.tokens = []
            self.filepath = filepath
            input_file = open(filepath, 'r')
            multiple_line_comments = False
            for line in input_file.readlines():
                if line.startswith("/*"):
                    multiple_line_comments = True
                    continue
                if multiple_line_comments:
                    index = line.find('*/')
                    if index == -1:
                        continue
                    else:
                        line = line[index+2:]
                        multiple_line_comments = False
                self.decompress_line(re.sub(COMMENT_RE, '', line).strip())   # get the clean line here
            input_file.close()
        except FileNotFoundError:
            print("could not find %s" % filepath)

    def has_more_tokens(self):
        return len(self.tokens) > 0

    def advance(self):
        if self.has_more_tokens():
            self.token = self.tokens.pop(0)

    def tokenType(self):
        return self.token[1]

    def get_current_token(self):
        return self.token[0]

    def decompress_line(self, line):
        while len(line) != 0:
            for regex in RE_LIST:
                match_syntax = re.match(regex, line)  # match matches the start of the string
                if match_syntax is not None:
                    word = match_syntax.group()
                    if LEXICAL_MAP[regex] == 'stringConstant':
                        word = word.replace('"', '')
                    self.tokens.append((word, LEXICAL_MAP[regex]))
                    line = line[len(word):].strip()

    def output_t_xml(self):
        txml = self.filepath.replace('.jack', 'T2.xml')
        special_symbol_map = {
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            '&': '&amp;'
        }
        f = open(txml, 'w')
        f.write('<tokens>\n')
        for token_tuple in self.tokens:
            if token_tuple[0] in special_symbol_map.keys():
                syntax = '<%s> ' % token_tuple[1] + special_symbol_map[token_tuple[0]] + ' </%s>\n' % token_tuple[1]
            else:
                syntax = '<%s> ' % token_tuple[1] + token_tuple[0] + ' </%s>\n' % token_tuple[1]
            f.write(syntax)
        f.write('</tokens>\n')
        f.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)

    filename = sys.argv[1:]
    print("this is the thing: \n")
    print(filename)
    jtk = JackTokenizer(filename[0])
    jtk.output_t_xml()
















