# -*- coding: utf-8 -*-
import json

from scrapy import log
from scrapy.http import Request
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

from scrapycrawler.items import HouseDetailItem


class LianjiaSpider(Spider):
    name = 'lianjia'
    allowed_domains = ['m.lianjia.com']
    base_url = 'http://m.lianjia.com'
    start_url = '{}/mapi/dict/city/Info?city_id=110000'.format(base_url)
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'connection': 'keep-alive',
            'cookie': 'lianjia_uuid=486acbc4-ec65-40ee-bf19-3bb5edf87faa; _smt_uid=584e0baf.c146f06; '
                      'lj-ss=1e5c8b6bb356c2aabadd162c97341948; ubt_load_interval_b=1482158907197; '
                      'gr_user_id=e513be73-c4fd-416d-bb8a-5fa3fabd0fef; '
                      'ubta=3154866423.83801682.1482158907396.1482158907396.1482158907396.1; '
                      'ubtc=3154866423.83801682.1482158907399.0455210DB487A3EE2CC76C240D2EA03B; ubtd=1; '
                      'lj-api=342a9dda437f3007bdc32885b0f4abfc; select_city=110000; select_nation=1; _gat=1; '
                      '_gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; '
                      'lianjia_ssid=aa8ecf0f-9eae-4095-ab1a-d698402c4219; '
                      'CNZZDATA1254525948=18037264-1482159476-%7C1482299879; '
                      'CNZZDATA1253491255=249835780-1482160243-%7C1482295269; _ga=GA1.2.687066279.1481509810',
            'host': 'm.lianjia.com',
            'referer': 'http://m.lianjia.com/bj/xiaoqu/pg4/',
            'x-requested-with': 'XMLHttpRequest',
            'x-forward-for': '221.235.53.169'
        }
    }

    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse
        )

    def parse(self, response):
        # 链家城市的地铁、商圈数据
        map_json = json.loads(response.body_as_unicode())
        districts = map_json['data']['info'][0]['district']
        for district in districts:
            zones = district['bizcircle']
            for zone in zones:
                #item = ZoneItem()
                # 商圈id
                #item['id'] = zone['bizcircle_id']
                # 商圈拼音
                pinyin = zone['bizcircle_quanpin']
                #item['pinyin'] = zone['bizcircle_quanpin']
                # 商圈中文名
                #item['name'] = zone['bizcircle_name']
                yield Request(
                    url='http://m.lianjia.com/bj/chengjiao/{}/pg1/?_t=1'.format(pinyin),
                    callback=self.parse_zone
                )

    def parse_zone(self, response):
        json_response = json.loads(response.body_as_unicode())
        html = json_response['body']
        soup = BeautifulSoup(html, "lxml")
        for li in soup.findAll('li', {'class': 'pictext'}):
            detail_url = li.a['href']
            yield Request(
                url='{}{}'.format(self.base_url, detail_url),
                callback=self.parse_detail
            )

        # 生成该商圈下一页的url
        json_args = json.loads(json_response['args'])
        if json_args['no_more_data'] != 1:
            cur_page = int(json_args['cur_page'])
            next_page = cur_page + 1
            yield Request(
                url=response.url.replace('pg{}'.format(cur_page), 'pg{}'.format(next_page)),
                callback=self.parse_zone
            )

    def parse_detail(self, response):
        json_response = json.loads(response.body_as_unicode())
        soup = BeautifulSoup(json_response['body'], "lxml")
        item = HouseDetailItem()

        # Essential
        try:
            item['title'] = soup.find(name='h3', attrs={'class': 'house_desc'}).string
            h3 = soup.find('h3', attrs={'class': 'similar_data'})
            item['price'] = h3.find('span', attrs={'data-mark': 'price'}).string
            item['unit'] = h3.find('p', text='单价').findNext('p').string.strip()
        except AttributeError:
            self.log('Essential attribute empty for %s' % response.url, level=log.WARNING)

        # Optional
        ul = soup.find('ul', {'class': 'house_description big lightblack'})
        item['date'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='日期：'))
        item['source'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='来源：'))
        item['floor'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='楼层：'))
        item['orientation'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='朝向：'))
        item['year'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='年代：'))
        item['building_type'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='楼型：'))
        item['fitment'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='装修：'))
        item['purpose'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='用途：'))
        item['region'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='区域：'))
        item['subway'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='地铁：'))
        item['heating'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='供暖：'))
        item['community'] = self._get_with_default(lambda x: x.parent.contents[1], ul.find('span', text='小区：'))

        # div class="info_layer" data-mark="more_house_info
        yield item

    @staticmethod
    def _get_with_default(func, param, default='-'):
        try:
            return func(param)
        except AttributeError:
            return default
