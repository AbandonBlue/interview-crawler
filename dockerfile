# 建立基礎環境供 Mongodb, python 使用
# comment: baseImage, 記住不可以同行(與指令)
FROM python:3.7.3           

# 新增資料夾 crawler_app
WORKDIR /crawler_app

# 將與dockerfile同level檔案加入 crawlr_dir
# ADD . /crawler_app
ADD crawler_route.py /crawler_app
ADD crawler_school.py /crawler_app
ADD crawler.py /crawler_app
ADD requirements.txt /crawler_app


# 下載必須套件
RUN pip install -r requirements.txt

# 執行程式, CMD 在dockerfile裡面只能有一個
CMD ["python", "crawler.py"]