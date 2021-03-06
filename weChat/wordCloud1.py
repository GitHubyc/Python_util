# coding:utf-8
import itchat
import re

import jieba

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image

itchat.login()
friends = itchat.get_friends(update=True)[0:]
tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)

# 拼接字符串
text = "".join(tList)


wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)



# font_path为字体，默认当前文件夹下的HYQiHei-25J.ttf
my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         max_font_size=40, random_state=42,
                         font_path='HYQiHei-25J.ttf').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
