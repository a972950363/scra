# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem

class KdlspiderSpider(scrapy.Spider):
    name = 'kdlspider'
    allowed_domains = ['kuaidaili.com']
    start_urls = []
    for i in range(1,6):
    	start_urls.append('https://www.kuaidaili.com/free/inha/'+str(i)+'/')
    def parse(self, response):
        item = ProxyItem()

        mian = response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for li in mian:
            ip = li.xpath('//td[1]/text()').extract()[0]
            port = li.xpath('//td[2]/text()').extract()[0]   #解析时要加根符号
            item['addr'] = str(ip) +':'+ str(port)  #不同类型数据不可直接相加
            yield item   