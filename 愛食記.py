import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

#為了爬出每一個餐廳的頁面網址，利用迴圈將搜尋索引的所有頁面跑一遍，資料儲存在list中下一段使用。
page = 1
pageurl = []
for j in range(1,{搜尋結果的最後一頁}):
    url = 'https://ifoodie.tw/explore/%E5%8F%B0%E5%8D%97%E5%B8%82/list?page={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    res = requests.get(url.format(page), headers=headers)
    html = res.text

    soup = BeautifulSoup(html, 'html.parser')
    
    titlelist = soup.find_all('a', class_="jsx-3440511973 click-tracker")
    for title in titlelist:
        urlshop = "https://ifoodie.tw" + title.get('href')
        pageurl.append(urlshop)
    page +=1

#pageurl包含了所有餐廳頁面的網址，利用迴圈請求之即可。
list = []
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
    #將留言區的評論json格式從想要的元素一個個按照順序append到list中
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
shop_df.to_csv('C:{路徑名稱}/{檔案名稱}.csv',encoding="utf_8_sig")

'''
本次爬蟲目的是要爬取愛食記網站上台南區的餐廳評論，為了後續做餐廳推薦的準備。
而撰寫爬蟲程式的要點在於每一個餐廳都是一個網頁，所以我們要先將每一個搜尋索引頁面中的餐廳網址從page={n}，
中逐一爬取後存到list，再進入list中的每一個網頁爬取留言區，
爬蟲的過程可以先將自己想要的資料型態做初步整理，像是店名、作者等等一定要的元素爬取後儲存到list按照順序存取後，
再利用pandas套件儲存成csv到本機，或是儲存成json到MongoDB之類的資料庫都可以，
因爬蟲經驗得知，這種網頁結構與資料容易整理與爬取的來源，
如果第一步可以簡單的按照格式爬取，後續整理也不需要廢多少力氣，可以直接做ETL進到本機或同步sql資料庫。
'''