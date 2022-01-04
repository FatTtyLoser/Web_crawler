from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib import request
import pandas as pd
import random
import time
import json
import ssl
import re
import os

# 設定我們在程式之中使用 time.sleep 等待的時間，讓時間變數可設定又亂數抽取
seconds = [秒數1, 秒數2, 秒數3, 秒數4, 秒數5......]
delay = random.choice(seconds)

# 設定儲存路徑
path = r'.\\dcardtalk'
if not os.path.exists(path):
    os.mkdir(path)

# Dcard 公開 API URL
api = 'https://www.dcard.tw/service/api/v2'
# 訪問 talk 版前五篇熱門文章
url = api + '/forums/talk/posts?popular=true&limit=5'
# fack_useragent 亂數提供 headers 提高隱蔽性
headers = {
    'User-Agent' : UserAgent().random
}
req = request.Request(url = url , headers = headers)
res = request.urlopen(req)
html = res.read().decode('utf-8')
rejson = json.loads(html)
rejson
# 訪問了一次伺服器所以進行等待
time.sleep(delay)

# 第一個迴圈逐筆解析每一篇文章資訊
for articleDict in rejson:
    # 先建立文章內容變數
    articleTxt = ''
    # 取得每一篇文章的 title 作為儲存檔名
    title = articleDict['title']
    # Win10 檔名有特殊字元限制，透過 python 正則化將 title 特殊字元刪除
    if ':' and '/' and '*' and '"' and '>' and '<' and '|' and '?' and '：' and ' ' in title:
        title = re.sub("\<|\'|\?|\ |\>|\*|\:|\"|\？|\：|\||\/|\//","",title)
    else:
        pass
    # 取得每一篇文章的 ID 作為訪問單篇文章的 API 參數
    id = articleDict['id']
    # format id 訪問單篇文章
    cp_articleUrl = 'https://www.dcard.tw/service/api/v2/posts/{}'.format(id)
    cp_req = request.Request(url = cp_articleUrl , headers = headers)
    cp_res = request.urlopen(cp_req)
    cp_html = cp_res.read().decode('utf-8')
    cp_jsonData = json.loads(cp_html)
    # 加入單篇文章的內容 content 
    articleTxt += cp_jsonData['content'] + '\n=============\n'
    # 又訪問一次伺服器所以進行等待
    time.sleep(delay)
    # 先建立記數留言的 index
    index = 0
    # 留言樓層的參數設定
    after = 0
    # 透過 API 請求單篇文章的留言區 after 表示從哪一個樓層往下
    url = 'https://www.dcard.tw/service/api/v2/posts/{}/comments?limit=30&after={}'.format(id, after)
    req = request.Request(url = url , headers = headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    # 此時的 jsonData 應該是單篇文章的每一個留言樓層的內容
    jsonData = json.loads(html)
    # 又訪問一次伺服器所以進行等待
    time.sleep(delay)
    # 第二個迴圈解析每一樓層的每一個留言內容
    while True:
        # 若我們上一層迴圈裡面首次請求留言區取得的留言不為零，那麼我們確定我們有需要爬取的留言，因此進行爬取
        if len(jsonData) != 0:
            # 從第0樓開始爬取
            url = 'https://www.dcard.tw/service/api/v2/posts/{}/comments?limit=30&after={}'.format(id, after)  
            req = request.Request(url = url , headers = headers)
            res = request.urlopen(req)
            html = res.read().decode('utf-8')
            jsonData = json.loads(html)
#             print(jsonData)
            print(title+str(len(jsonData)))
            # 使用 try loop 例外處理我們遇到刪除留言的樓層
            try:
                # 如果留言沒被刪除則執行以下
                for articleCon in jsonData:
    #                 print(articleCon['content'])
                    index += 1
                    con = articleCon['content']
                    # 將換行符號刪除
                    con = re.sub("\n","",con)
                    # 整理每篇留言格式統一
                    content = str(index)+ '.' + con + '\n'
                    # 將留言字串整理新增到單篇文章內文中
                    articleTxt += content
            # 忽略刪除的留言樓層
            except:
                pass
            print('====')
            # 執行完一次迴圈表示我們訪問了一次的單篇文章固定數量的留言區，因此進行等待
            time.sleep(delay)
            # after 隨著我們設定每次爬取的留言樓層增加
            after += 30
        # 若我們訪問單篇文章留言區的留言為零，則儲存我們取得的內文
        else :
            # 儲存並寫入我們的內容，title 是文章標題，內容是單篇內文加上所有留言
            with open(r'%s\\\%s.txt' % (path, title), 'w', encoding='utf-8') as w:
                w.write(articleTxt)
            break
# print(articleTxt)