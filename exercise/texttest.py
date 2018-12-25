import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Build a dataframe with your connections
df = pd.DataFrame({'from': ['A', 'B', 'C', 'A', 'E', 'F', 'E', 'G', 'G', 'D', 'F'],
                   'to': ['D', 'A', 'E', 'C', 'A', 'F', 'G', 'D', 'B', 'G', 'C']})
df

# Build your graph
G = nx.from_pandas_dataframe(df, 'from', 'to')

# Fruchterman Reingold
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.fruchterman_reingold_layout(G))
plt.title("fruchterman_reingold")

# Circular
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.circular_layout(G))
plt.title("circular")

# Random
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.random_layout(G))
plt.title("random")

# Spectral
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.spectral_layout(G))
plt.title("spectral")

# Spring
nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.spring_layout(G))
plt.title("spring")


def main():
    target_file = open('scw_2016.txt', 'r', encoding='utf-8')
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
        tmp_str = ''
        result = m.parse(sent).strip().split('\n')
        mini_result = [i.split('\t') for i in result]
        # print(mini_result)
        del mini_result[-1]
        for sent in tmplist:
            tmp_str = ''
            mini_result = [i.split('\t') for i in m.parse(sent).strip().split('\n')]
            del mini_result[-1]
            for i in range(len(mini_result)):
                word = mini_result[i]
                # print(word)
                if len(word) <= 3:
                    pass
                if "名詞" in word[3] and notnum(word[0]):
                    tmp_str += word[0]
                else:
                    if tmp_str != '':
                        wordcounter[tmp_str] += 1
                    tmp_str = ''

    wc_new = Counter(el for el in wordcounter.elements() if wordcounter[el] >= 10)
    print(wc_new)
    return wc_new


def refine(wc, key_list):
    refine_dict = {}
    for key in key_list:
        for word in wc.keys():
            if key in word and not word in refine_dict:
                refine_dict[word] = wc[word]
    rd = sorted(refine_dict.items(), key=lambda kv: -kv[1])
    rd_rect = {}
    for k, v in rd:
        rd_rect[k] = v
    print(rd_rect)
    return rd_rect


def notnum(string):
    return string not in '０１２３４５６７８９0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.-'


wc_new = main()
rd = refine(wc_new, ['高齢', 'イノベーション', '雇用', '研究開発', '健康', '女性', '中小', '革新', '個人', '技術', '人材', '個人消費', '産業', \
                     'シェアリング', 'データ', 'テレワーク', '回復', 'ロボット', 'スタート', 'リーマンショック', '製造業'])

wc = WordCloud(
    width=1366,
    height=768,
    background_color="white",
    font_path='07gothic.ttf'
).generate_from_frequencies(rd)
wc.to_file("【WCW TeamA】WordCloud_2015to2017.png")
