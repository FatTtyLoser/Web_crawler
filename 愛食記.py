import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import numpy
import time
import sys, json

page = 1
list = []
pageurl = []
for j in range(1,68):
    url = 'https://ifoodie.tw/explore/%E5%8F%B0%E5%8D%97%E5%B8%82/list?page={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    res = requests.get(url.format(page), headers=headers)
    html = res.text

    soup = BeautifulSoup(html, 'html.parser')
    
    titlelist = soup.find_all('a', class_="jsx-2133253768 click-tracker")
    for title in titlelist:
        urlshop = "https://ifoodie.tw" + title.get('href')
        pageurl.append(urlshop)
    page +=1

for k in pageurl:
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    url = k
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    comment_demo = soup.select('script[class="next-head"][type="application/ld+json"]')
    list_comment = comment_demo[1].string.split('">')
    comment = list_comment[0]
    json_comment = json.loads(comment)
    # print(json_comment)
    try:
        for i in range(6):
            if json_comment['review'][i]['author']['name'] != False :
                    list.append(json_comment['name'])
                    list.append(json_comment['review'][i]['author']['name'])
                    list.append(json_comment['review'][i]['datePublished'])
                    list.append(json_comment['review'][i]['description'])
            else :
                break
    except:
        pass
    
step = 4
slicelist = [list[i:i + step] for i in range(0, len(list), step)]
shop_df = pd.DataFrame(slicelist)
shop_df.index = shop_df.index + 1  # 自訂索引值
shop_df.columns = ["店名","作者", "日期", "評論"]
# print(shop_df)
shop_df.to_csv('C:/Users/Jeffery1009/Desktop/爬蟲QQ/愛食記評論.csv',encoding="utf_8_sig")