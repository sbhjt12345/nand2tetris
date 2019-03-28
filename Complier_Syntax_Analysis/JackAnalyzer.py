#!/usr/bin/python3


from CompilationEngine import *
import os


class JackAnalyzer:
    def __init__(self, filepath):
        jtk = JackTokenizer(filepath)
        jtk.output_t_xml()
        CompilationEngine(filepath)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("enter sth")
        sys.exit(1)
    filename = sys.argv[1:][0]
    file_split_list = filename.split('/')
    if file_split_list[len(file_split_list)-1].endswith('.jack'):
        JackAnalyzer(filename)
    else:
        file_path_list = []
        for root, _, files in os.walk(filename):
            for f in files:
                if f.endswith('.jack'):
                    file_path_list.append(os.path.join(root, f))
        print(file_path_list)
        for fpl in file_path_list:
            JackAnalyzer(fpl)

