# interview-crawler


## 任務完成狀況 ##
- [x] 測驗題1
    1. [x] 從起迄站查詢台北轉運站至朝馬轉運站的路線
    2. [x] 將路線查詢結果輸出成CSV
        - 台北到朝馬.csv
    3. [x] 將路線查詢結果寫入MongoDB(或SQL)
    4. [x] 統計MongoDB (或SQL)中route欄位有出現埔里的筆數
        - 簡單用Regex計算
- [x] 測驗題2
    1. [x] 下載學科能力測驗中83年度~109年度全部學科一般試題中所有的pdf檔案
    2. [x] 分類存放下載完成的pdf檔案
    3. [x] 請測量並盡量減少下載檔案所需的時間
        - 其中透過 threading 節省 1/3 的時間，若要詳細證明可以搭配統計檢定 run 多次。



---

## 使用說明 ## 
- [x] 方法1: 透過venv 開啟 python 環境確保程式運行，預設本地端mongodb, python已經有建立。
```
          $ python -m virtualenv env
          $ env\Scripts\activate.bat
    (env) $ pip install -r requirements.txt
          $ python crawler.py
```
    - 測驗1第4小題答案會顯示在最後。

- 方法2: 透過docker-compose 連同 mongodb server一同建立
    - 因本地電腦 docker-compose 版本老舊，遇到[docker-compose-up-invalid-service-name 問題](https://stackoverflow.com/questions/53442908/docker-compose-up-invalid-service-name-only-a-za-z0-9-chara)，版本修改即可解決問題。
    - 但因時間有限，故沒有針對這邊繼續解決，還是給面試官參考。
    - 但後續的檔案儲存需要透過 docker expose 匯出, 亦可用bash cat簡單檢視