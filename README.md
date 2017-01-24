# 简介
### 链家网二手房成交纪录爬虫
### 使用Python3开发，基于Scrapy实现爬取
### 使用BeautifulSoup进行页面解析
### 使用Mongodb进行存储
# 使用方法
### 1.先安装依赖的Python库
pip install Scrapy
pip install beautifulsoup4
### 2.修改配置文件 scrapycrawler/setting.py
MONGODB_SERVER='localhost'        #mongdb的ip地址<br />
MONGODB_PORT=27017                #mongodb端口<br />
MONGODB_DB='house'                #mongodb用于存储成交数据的数据库名称<br />
MONGODB_COLLECTION='lianjiatotal' #mongodb用于存储成交数据的集合名称<br />
### Terminal中执行 scrapy crawl lianjia
