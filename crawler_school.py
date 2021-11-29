
import requests
from bs4 import BeautifulSoup
import pymongo
import pandas as pd
import time
import threading
import os


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

def get_year(string: str):
    for i, e in enumerate(string):
        if not e.isdigit():
            return string[:i]

def check(y, download_url):
    if y < 83 or y > 109 or ('.pdf' not in download_url):
        return False
    return True

def download_pdf(year, path, filename, download_url):
    with open(os.path.join('download', str(year), path, f"{path}-{filename}.") + download_url.split('.')[-1], 'wb') as f:
    # with open(f"/download/{year}/{path}/{path}-{filename}.{download_url.split('.')[-1]}", 'wb') as f:
        d_url = download_url
        if 'https' not in d_url:
            d_url = 'https://www.ceec.edu.tw' + d_url
        response = requests.get(d_url, headers=headers,verify=False)
        f.write(response.content)
    print(f"下載網址: {d_url}")

def crawler_page(page: int, is_parallel: bool):
    if is_parallel:
        threading_parameters = []
    payload['IndexOfPages'] = page
    resp = requests.post(url, headers=headers, verify=False, data=payload, cookies=cookie)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    for title, download in zip(soup.find_all(class_="title")[1:], soup.find_all(class_="download")[1:]):
        file_prefix = title.text.split()[0]
        y = int(get_year(file_prefix))
        file_dir = os.path.join('download', str(y), file_prefix)

        for e in download.find_all('a'):
            filename = e.text
            download_url = e.get("href")
            if check(y, download_url):
                if not os.path.isdir('download'):
                    os.mkdir('download')
                if not os.path.isdir(os.path.join('download', str(y))):
                    os.mkdir(os.path.join('download', str(y)))
                if not os.path.isdir(file_dir):
                    os.mkdir(file_dir)
                if is_parallel:
                    threading_parameters.append((y, file_prefix, filename, download_url))
                else:
                    download_pdf(y, file_prefix, filename, download_url)
    
    if is_parallel:
        # 多執行緒
        for i in range(len(threading_parameters)):
            thd = threading.Thread(target=download_pdf, name=f'download-{filename}', args=threading_parameters[i])
            threading_parameters[i] = thd
            thd.start()

        for i in range(len(threading_parameters)):
            threading_parameters[i].join()

    print(f'Page {page} Done.')  



if __name__ == '__main__':
    pass