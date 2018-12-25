import re
from collections import Counter
import matplotlib.pyplot as plt
import MeCab
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def main():
    target_file = open('script.txt', 'r', encoding='utf-8')
    text = target_file.read()
    target_file.close()
    tmp = re.sub(r'\n', '', text)
    tmp = re.sub(r'（.{7,10}）', '', tmp)
    tmplist = tmp.split('。')
    wordcounter = Counter()
    # shortwordcounter = Counter()

    m = MeCab.Tagger('-Ochasen')
    for sent in tmplist:
        # print(sent)
        result = m.parse(sent).strip().split('\n')
        mini_result = [i.split('\t') for i in result]
        # print(mini_result)
        del mini_result[-1]
        for i in range(len(mini_result)):
            word = mini_result[i]
            if i > 0:
                word1 = mini_result[i - 1]
            else:
                word1 = ['', '', '', '０', '']
            if "名詞" in word[3] and "名詞" in word1[3] and notnum(word[0]) and notnum(word1[0]):
                wordcounter[mini_result[i - 1][0] + word[0]] += 1
            elif "名詞" in word[3] and "形容詞" in word1[3] and notnum(word[0]) and notnum(word1[0]):
                wordcounter[word1[0] + word[0]] += 1
    wc_new = Counter(el for el in wordcounter.elements() if wordcounter[el] >= 20)
    return wc_new


def refine(wc, key_list):
    refine_dict = {}
    for key in key_list:
        for word in wc.keys():
            if key in word and not word in refine_dict:
                refine_dict[word] = wc[word]
    rd = sorted(refine_dict.items(), key=lambda kv: -kv[1])
    print(rd)
    return rd


def notnum(string):
    return string not in '０１２３４５６７８９'


import matplotlib as mpl

# print(mpl.matplotlib_fname())
# for f in font_manager.fontManager.ttflist:
#     print(f)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams["figure.figsize"] = [8, 3]
plt.rcParams['font.size'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
wc_new = main()
rd = refine(wc_new, ['外国', '国際', '雇用', '人材', '海外', '業'])
fig, axs = plt.subplots(1, 1, figsize=(20, 5), sharey=True)
names = [u'{}'.format(k[0]) for k in rd]
values = [k[1] for k in rd]
axs.bar(names, values)
fig.suptitle(u'頻度ヒストグラム_平成22年度経済財政白書_2011')
plt.show()