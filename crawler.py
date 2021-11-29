import requests
import json
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
import time
import threading
import os

from crawler_route import data_to_column, get_rows, to_csv, get_col, insert_to_mongo
from crawler_school import get_year, check, download_pdf, crawler_page

    
if __name__ == '__main__':
    print("測驗 1 開始:")
    url = "http://www.kingbus.com.tw/ticketRoute.php"
    post_data = {
        'area': "台北",
        'origin': "臺北轉運站",
        'destination': "朝馬轉運站",
        "submit": "查詢",
    }


    resp = requests.post(url, data=post_data)
    resp.raise_for_status()     # 如果請求有問題，直接發生錯誤
    resp.encoding = resp.apparent_encoding  # 正確編碼以顯示網頁，損失部分性能
    soup = BeautifulSoup(resp.text, 'html.parser')
    rows = []

    rows= get_rows(rows, soup)
    to_csv(rows)
    my_col = get_col()
    insert_to_mongo(my_col, rows)
    query = {"route": {"$regex": "埔里"}}
    count = my_col.count_documents(query)
    print(count)

    print("測驗 1 完畢。")



    print("測驗 2 開始")
    url = "https://www.ceec.edu.tw/xmfile/indexaction"
    payload = {
        '__RequestVerificationToken': 'KGE6snp7CGrGB_4lIBFfZ0Jp3f0zPPUUIwr11RGN2VeO07bLoRZ-uMUMOSf07gNtGpMzURm14shZoAqbag9Uy6T_5llAGjlA5YRvwLQhwq01',
        'XsmSId': '0J052424829869345634',
        'CondsSId': '0L331653270379684361',
        'ExecAction': 'Q',
        'IndexOfPages': 1,
        'Annaul': '',
        'CatSId': '',
        'PageSize': 10
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                'AppleWebKit/537.36 (KHTML, like Gecko)'
                                'Chrome/75.0.3770.100 Safari/537.36',
        'Connection': 'close' # 解決過多request被鎖ConnectionError: HTTPSConnectionPool(host='www.ceec.edu.twhttps', port=443): Max retries exceeded with url: //www.ceec.edu.tw/files/file_pool/1/0j076800993877603476/01-107%E5%AD%B8%E6%B8%AC%E5%9C%8B%E6%96%87%E5%AE%9A%E7%A8%BF.pdf (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x000002760AB6C518>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
    }
    cookies = '__RequestVerificationToken=FsUPgzxpYDXktZ_8Q-O5V41RNiTlKkb2pddziz59ph8YC8rQ6OB9oGkD2xO2pTP9rvGm5Ai026i-rKdvgUMF2BHrB8h67C9Vwo88jJk9IzQ1; FSize=M; fwchk=DWPwNx7zMsX+jAVRQaUEUd2Mpds0000'
    cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")} 
    t = time.time()
    for i in range(0, 17):
        crawler_page(i, True)

    print(f"threading 耗時: {time.time()-t} 秒")


    print("測驗 2 完畢")

    print(f"測驗1第4題答案: {count}")

    # 如何要運行docker, 可開始下面讓app保持運行
    # while True:
    #     time.sleep(10)