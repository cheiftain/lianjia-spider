# -*- coding: utf-8 -*-
import random

class randomua(object):

    def __init__(self, agents):
        self.agents = agents;

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getList('USER_AGENTS')) # 返回的是本类的实例cls == randomua

    def process_request(self, request, spider):
        request.headers.setdefualt('User-Agent', random.choice(self.agents))