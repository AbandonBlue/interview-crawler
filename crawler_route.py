import pymongo
import pandas as pd
from bs4 import BeautifulSoup
import requests


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

def data_to_column(row_data):
    
    idx1 = row_data.find('[')
    route = row_data[row_data.find('【'):idx1]
    destination = row_data[idx1:]
    return route, destination


def get_rows(rows, soup):
    for row_data in soup.find(class_="routeData").find_all('li'):
        row_data = ''.join(row_data.text.split())
        data_tuple = data_to_column(row_data)
        print(data_tuple)
        rows.append({'route': data_tuple[0], 'description': data_tuple[1]})
    return rows


def to_csv(rows):
    df = pd.DataFrame(rows)
    df.to_csv('台北到朝馬.csv', encoding='utf-8-sig', index=False) # 中文編碼問題


def get_col(db_name="ticket_route_db", col_name="route"):
    # 建立DB、Collection、插入資料

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    
    return mycol

def insert_to_mongo(mycol, rows):
    mycol.insert_many(rows)  # list of dict
    print("資料進入mongo db.")



if __name__ == '__main__':
    pass