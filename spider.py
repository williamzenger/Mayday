import requests
from requests.exceptions import RequestException
# from multiprocessing import Pool
import re
from bs4 import BeautifulSoup
import jieba
import wordcloud
import collections

print('Libraries imported')

url_list = []

a = 0
while a != 70:
    a += 1
    for b in range(1,40):
        urls = 'https://mojim.com/cny100012x{}x{}.htm'.format(a,b)
        url_list.append(urls)


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
lyrics = []
for each_item in url_list:
    response = requests.get(each_item, headers=headers).text
    try:
        if response != '\ufeff\ufeff\ufefferror':
            soup = BeautifulSoup(response, features='lxml')
            text = [item.get_text(strip=True) for item in soup.select('dd.fsZx3')][0]
            pattern = re.sub(r'\[.*','',text).replace('更多更详尽歌词 在※ Mojim.com　魔镜歌词网','').replace('\u3000','').strip()
            lyrics.append(pattern)

            song = [item.get_text(strip=True) for item in soup.select('dt.fsZx2')][0]        
            file = song+'.txt'
            f=open(file,'w')
            f.write(pattern)
            f.close()
            print(song)
        else:
            pass
    except:
        FileNotFoundError

print(len(lyrics))

lyrics_string = ''.join(lyrics)
seg_lists = [word for word in jieba.cut(lyrics_string, cut_all=False) if len(word)>=2]
# print("Default Mode: " + "/ ".join(seg_lists))  # 精确模式
print(seg_lists)

import collections

exclude_words = ['五月天','阿信','作曲','作词','编曲','La','HoSee','Repeat','什么','这样','这个',
                 '不是','一天','一个','就是','OK','怪兽','La ','var','OKOK','最新', '单曲','首歌',
                 '曲长', '20', '分钟', 'non', 'stop', 'mix']

i = 0
while i != 5:
    for word in seg_lists:
        if word in exclude_words:
            seg_lists.remove(word)
    i +=1

c = collections.Counter(seg_lists)
for word_freq in c.most_common(50):
    word, freq = word_freq
    print(word, freq)