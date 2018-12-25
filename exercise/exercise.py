#!/usr/bin/python3
import random
import time
from PIL import Image

# year = input("year: ")
# month = input("month: ")
# day = input("day: ")
# step3 = sum(list(map(int, year + month + day)))
# lucky_number = sum([int(i) for i in str(step3)]) % 9+1
# print(lucky_number)



today_action = ["授業中に関わらず夕方までとりあえず寝てしまった", "鈴木さんに「うるせーよババア箱崎に帰れ」と思わず叫んでしまった",
                "今日はちゃんとスーツ着てふざけない", "安井くんの表情を観察する",
                "りかと中村と小松の修羅場を楽しむ。本当にカップルできたらすんーーーーーげいウケる", "新井さんとちゃんまゆは兄弟なの？",
                "一回だけ幕張まで自転車で来たことある", "浦上三兄弟：浦上ご・浦上こ・く浦上（韓国人）",
                "ぐジョンもーのお父さんの名前は具志堅", "富沢正治の研修日常は：爆笑・爆笑・爆笑・爆笑……",
                "中村くんは毎週末ナンパしに行くらしい",
                "赤いシャツ着てて片手の親指ぐるぐる回って片手がグリッパー握りながら女性の同期に「オレの人間性どう思う？」って聞く人を当てて下さい"]
num = random.randrange(12)
print(num)
if num <= 1:
    print("今日はまた新井さんに怒られたよ！その原因は：")
    print(today_action[num] + '\n')
    print("で、夕食どうする？")
elif num <= 10:
    print("研修期間あるある： たとえば......\n")
    input("")
    for i in range(2, 11):
        print("なんと！！！")
        time.sleep(3)
        print(today_action[i] + '\n')

    print("\n安井くん、どう思う？")
else:
    print("ここからはクイズです。賞金1円。")
    print(today_action[num] + '\n')
    print("ヒント：安井くんが同期の中で一番ジジー顔してると思ってる人です")

time.sleep(3)
print("\n最後は、秘密一つシェアさせていただきましょう。ふふふ")
print("\nそうだ\n")
time.sleep(1)
print("僕がキラだ")
time.sleep(3)
image = Image.open('killer.jpg')
image.show()








