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
### 3.Terminal中执行 scrapy crawl lianjia
# 使用备注
###默认爬取<b>北京</b>地区的二手房成交数据<br/>
###若要爬取其他城市，请搜索"中国城市代码表"，用目标城市代码替换scrapycrawler/setting.py中，CITY_CODE的值，
例如爬取上海，则修改为<code>CITY_CODE='310000'</code>
