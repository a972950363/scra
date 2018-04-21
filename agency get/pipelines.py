# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProxyPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'kdlspiders':
        	content = item['addr'].split('\r\n')
        	for line in content:
        		open(r'C:\Users\Administrator\Desktop\新建文件夹\dx_proxy.txt','a').write(line+'\n')
        else :
        	open(r'C:\Users\Administrator\Desktop\新建文件夹\kdl_proxy.txt','a').write(item['addr']+'\n')
        	

