from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib import request
import pandas as pd
import requests
import random
import time
import json
import ssl
import re
import os


# 設定儲存路徑
if not os.path.exists('./dcardstock'):
    os.mkdir('./dcardstock')

# Dcard 公開 API URL
api = 'https://www.dcard.tw/service/api/v2'

# URL 即是 API 加上參數為對股票討論版請求熱門排序前十名的文章
url = api + '/forums/stock/posts?popular=true&limit=10'

# Fake_useragent 讓我們每一次的 requests 都有不同的且真實的 headers
headers = {
    'User-Agent' : UserAgent().random
}

req = request.Request(url = url , headers = headers)
res = request.urlopen(req)
html = res.read().decode('utf-8')

# 使用 json 來解析透過 API 請求的內容
rejs = json.loads(html)

# 查看我們透過 json 解析後的結構
rejs
# 建立一個空集合的 DataFrame
pdData = pd.DataFrame()

# 利用一個迴圈把一篇一篇的文章取出我們想要的標籤與內容
for jsonData in rejs:
    # append 一篇文章的 Data
    pdData = pdData.append(pd.DataFrame(
        data=
        [{'id':jsonData['id'],
          '標題':jsonData['title'],
          '摘要':jsonData['excerpt'],
          '版別':jsonData['forumAlias'],
          '發文時間':jsonData['createdAt'],
          '更新時間':jsonData['updatedAt'],
          '回應數量':jsonData['commentCount'],
          '愛心數量':jsonData['likeCount'],
          '標註':jsonData['topics'],
          '分類':jsonData['forumName'],
          '性別':jsonData['gender'],
          'url':'https://www.dcard.tw/f/{}/p/'.format(jsonData['forumAlias']) + str(jsonData['id'])}],
        columns=['id','版別','標題','摘要','發文時間','更新時間','回應數量','愛心數量','標註','分類','性別','url']))
# pdData

# 儲存所有文章整理好的資料輸出成 .csv 格式，也可以使用 pd.to_excel 來儲存
pdData.to_csv(path + '/stockResoure.csv',encoding="utf_8_sig")