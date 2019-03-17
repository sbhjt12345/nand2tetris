#!/usr/bin/python3

import re


class JackTokenizer:
    def __init__(self, filepath):
        try:
            with open(filepath, 'r') as f:
                self.tokens = list(filter(None, [re.sub('//.*$', '', line).strip() for line in f]))
        except FileNotFoundError:
            print("could not find %s" % filepath)

    def has_more_tokens(self):
        return len(self.tokens) > 0

    