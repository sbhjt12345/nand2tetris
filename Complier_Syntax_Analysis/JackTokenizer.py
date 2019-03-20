#!/usr/bin/python3

import re

COMMENT_RE = r'(//(.*))|(/\*(.*?)\*/)'
KEYWORD_RE = r'(class)|(constructor)|(function)|(method)|(field)|(static)|(var)|(int)|' + \
             r'(char)|(boolean)|(void)|(true)|(false)|(null)|(this)|(let)|(do)|(if)|(else)|' + \
             r'(while)|(return)'
SYMBOL_RE = r'\(|\)|\{|\}|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~'
INTEGER_CONSTANT_RE = r'\d+'
STRING_CONSTANT_RE = r'"[^("|\n)]*"'
IDENTIFIER_RE = r'[^\d]\w+'
RE_LIST = [KEYWORD_RE, SYMBOL_RE, INTEGER_CONSTANT_RE, STRING_CONSTANT_RE, IDENTIFIER_RE]
LEXICAL_MAP = {
    KEYWORD_RE: "KEYWORD",
    SYMBOL_RE: 'SYMBOL',
    INTEGER_CONSTANT_RE: 'INT_CONST',
    STRING_CONSTANT_RE: 'STRING_CONST',
    IDENTIFIER_RE: 'IDENTIFIER'
}


class JackTokenizer:
    def __init__(self, filepath):
        try:
            self.tokens = []
            input_file = open(filepath, 'r')
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
                    self.tokens.append((word, LEXICAL_MAP[regex]))
                    line = line[len(word):]












