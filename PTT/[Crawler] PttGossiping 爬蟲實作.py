# 引入我們所需要的模組套件
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import os

# 設定儲存目標資料夾
path = r'.\\Ptt_Gossiping_Article'
if not os.path.exists(path):
    os.mkdir(path)

# 設定爬蟲程式偽裝瀏覽器的參數
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
headers = {
    'User-Agent' : UserAgent().random
}
cookie = {'over18':'1'}

# Ptt網頁版 Gossiping版 主頁index
url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
# 設定頁數
n = 3
# 翻頁loop
for i in range(0, n):
    res = requests.get(url, headers=headers, cookies=cookie)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    # 同頁內的文章標題取出各文章 url
    title = soup.select('div[class="title"]')
    # 訪問各文章 loop
    for eachArticle in title:
        try:
#             利用 try except loop 訪問未被刪除的文章 否則 return 刪除資訊
            try:
                each_articleUrl = 'https://www.ptt.cc' + eachArticle.select('a')[0]['href']
                print(each_articleUrl)
            except:
                print(eachArticle)
                print("===========")
            each_articleRes = requests.get(url=each_articleUrl, headers=headers, cookies=cookie)
            each_articleHtml = each_articleRes.text
            each_articleSoup = BeautifulSoup(each_articleHtml, 'html.parser')
            each_articleAuthor = each_articleSoup.select('span[class="article-meta-value"]')[0].text
            each_articleTitle = each_articleSoup.select('span[class="article-meta-value"]')[2].text
            each_articleText = each_articleSoup.select('div[id="main-content"]')[0].text.split('--')[0]
            # [踩坑] 由於 windows 檔案名稱不得有特定的特殊字元 所以直接刪除特殊字元
            if ':' and '/' and '*' and '"' and '>' and '<' and '|' and '?' and '：' and ' ' in each_articleTitle:
                each_articleTitle = re.sub("\<|\'|\?|\ |\>|\*|\:|\"|\？|\：|\||\/|\//","",each_articleTitle)
            else:
                pass
            # 若只想要儲存內文作為文字分析需求 預處理刪除網址連結
#             if 'https://' in each_articleText:
#                 each_articleText = each_articleText.split('\n')
#                 for h in each_articleText[0:]:
#                     if 'https://' in h:
#                         each_articleText.remove(h)
#                 each_articleText = "".join(map(str, each_articleText))
#             else :
#                 pass
            # 本篇文章 information
            push_info_list = each_articleSoup.select('div[class="push"] span')
            description_list = each_articleSoup.select('div[class="article-metaline"] span')
            for i, item in enumerate(description_list):
                if (i+1)%6 == 2:
                    Article_author = item.text
                if (i+1)%6 == 4:
                    Article_title = item.text
                if (i+1)%6 == 0:
                    Article_datetime = item.text
            # 統計推噓文
            Push = 0
            Boo = 0
            Score = 0 
            for info in push_info_list:
                if '推' in info.text:
                    Push += 1
                if '噓' in info.text:
                    Boo += 1
            Score = Push - Boo
            # 留言區整理
            Commtes_author = []
            Commtes_comment = []
            Commtes_IP = []
            for n, info in enumerate(push_info_list):
                if (n+1)%4 == 2:
                    Commtes_author.append(info.text)
                if (n+1)%4 == 3:
                    Commtes_comment.append(info.text)
                if (n+1)%4 == 0:
                    Commtes_IP.append(info.text)
            # 將文章內文加上文章 info
            each_articleText += '\n----------\n'
            each_articleText += '作者：%s\n' %(Article_author)
            each_articleText += '標題：%s\n' %(Article_title)
            each_articleText += '時間：%s\n' %(Article_author)
            each_articleText += '推：%s\n' %(Push)
            each_articleText += '噓：%s\n' %(Boo)
            each_articleText += '分數：%s' %(Score)
            each_articleText += '\n----------\n'
            # 將文章內文加上留言區
            for n in range(0,len(Commtes_author)):
                each_articleText += Commtes_author[n]
                each_articleText += Commtes_comment[n]
                each_articleText += '|'+Commtes_IP[n]
            # 儲存文章到指定 Path
            try:
                if os.path.isfile(r'%s\\\%s.txt' % (path, each_articleTitle)):
                    filename = each_articleTitle+'!'+each_articleAuthor
                    with open(r'%s\\\%s.txt' % (path, filename), 'w', encoding='utf-8') as w:
                        w.write(each_articleText)
                else:
                    with open(r'%s\\\%s.txt' % (path, each_articleTitle), 'w', encoding='utf-8') as w:
                        w.write(each_articleText)
                print()
        # 偵錯放在 loop 最後透過 except print 出 方便檢查 log
            except FileNotFoundError as e:
                print(each_articleTitle)
                print(e.args)
                print('==============')
            except OSError as e:
                print(each_articleTitle)
                print(e.args)
                print('==============')
        except AttributeError as e:
            print(each_articleTitle)
            print(e.args)
            print('==============')
    # 翻頁
    url = 'https://www.ptt.cc'+soup.findAll('a', class_="btn wide")[1]['href']