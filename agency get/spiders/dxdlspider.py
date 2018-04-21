# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class DxdlspiderSpider(scrapy.Spider):
    name = 'dxdlspider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://api.xicidaili.com/free2016.txt']

    def parse(self, response):
        item = ProxyItem()
        item['addr'] = response.text
        return item
