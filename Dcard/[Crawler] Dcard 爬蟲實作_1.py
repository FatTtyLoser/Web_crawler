from fake_useragent import UserAgent
from urllib import request
import pandas as pd
import requests
import random
import time
import json
import ssl
import re
import os

# 設定圖片儲存路徑
if not os.path.exists('./dcardPhoto'):
    os.mkdir('./dcardPhoto')

# 設定如果遇到網站需要認證則忽略認證直接進行訪問
ssl._create_default_https_context=ssl._create_unverified_context

# Dcard 公開 API URL
api = 'https://www.dcard.tw/service/api/v2'

# 設定請求伺服器的資訊頭，內容是偽裝瀏覽器
UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
headers = {
    'User-Agent': UserAgent
}

# API 加上參數訪問攝影版的前十熱門文章
url = api + '/forums/photography/posts?popular=true&limit=10'

# 對 API 進行 GET 請求
req = request.Request(url=url, headers=headers)
res = request.urlopen(req)
html = res.read().decode('utf-8')

# 將 html.txt 用 json 解析形成 list
jsonData = json.loads(html)
jsonData

# 透過 loop 把 list 拆開逐一針對 json 的標籤做選取
# title = 每篇文章的標題，mediaMeta = 每篇文章的 img 格式為 list，id = 每篇文章的 url 
for articleDict in jsonData:
    title = articleDict['title']
    articleUrl = 'https://www.dcard.tw/f/photography/p/' + str(articleDict['id'])
    print(title)
    print(articleUrl)
    # 利用迴圈把每篇文章的 img 一張一張儲存
    for imgs in articleDict['media']:
        print('\t' + imgs['url'])
        time.sleep(2)
        imagePath = './dcardPhoto/{}_{}'.format(title, imgs['url'].split('/')[-1])
        imgContent = requests.get(imgs['url'], headers=headers).content
        with open(imagePath, 'wb') as f:
            f.write(imgContent)
    print()