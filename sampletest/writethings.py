#!/usr/bin/python3

import sys


# class Dasabi:
#     def __init__(self, str):
#         self.str = str
#
#     def dosth(self):
#         with open('haha.rtf', 'r') as f:
#             with open('haha_baba.rtf', 'w') as wf:
#                 len_size = 10
#                 f_read = f.read(len_size)
#                 while len(f_read) > 0:
#                     print(f_read, end='hello', file=wf)
#                     f_read = f.read(len_size)
#                 print('dasabi')
#
#
# if __name__ == '__main__':
#     x = Dasabi(sys.argv[1:])
#     x.dosth()


with open('/Users/aa007500/Downloads/nand2tetris/projects/06/add.asm', 'r') as f:
    with open('haha_caca.rtf', 'w') as wf:
        len_size = 10
        f_read = f.read(len_size)
        while len(f_read) > 0:
            print(f_read, end='hello', file=wf)
            f_read = f.read(len_size)
        print('dasabi')

