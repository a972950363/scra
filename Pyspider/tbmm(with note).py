from pyspider.libs.base_handler import *
 
PAGE_START = 1
PAGE_END = 30
DIR_PATH = '/var/py/mm'
 
 
class Handler(BaseHandler):
    crawl_config = {
    }
 
    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='  # 目标URL
        self.page_num = PAGE_START     # 页面ID
        self.total_num = PAGE_END      # 页面范围
        self.deal = Deal()  #Deal类
 
    def on_start(self):      # 构造URL
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            self.crawl(url, callback=self.index_page,validate_cert=False)
            self.page_num += 1
 
    def index_page(self, response):
        for each in response.doc('.lady-name').items():     #调用PyQuery库用返回的内容生成一个PyQuery对象以方便使用，生成对象时默认已经把里面的所有链接格式化成绝对链接，可直接分析使用．    items()用来遍历字典（返回可遍历的(键, 值) 元组数组。）
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js',validate_cert=False)  #crawl用于爬取指定的网页； .attr()：获取、修改属性值；  callback指定用哪个方法处理内容；  fetch_type,validate_cert 用来加载JS与处理SSL出错
 
    def detail_page(self, response):
        domain = response.doc('.mm-p-domain-info li > span').text()  #选择进一步链接   text()方法用于取出文本内容
        if domain:
            page_url = 'https:' + domain  #构造进一步URL
            self.crawl(page_url, callback=self.domain_page,validate_cert=False)   #指定爬取链接与处理方法
 
    def domain_page(self, response):   #爬取内容处理方法  （response为初始爬取页）
        name = response.doc('.mm-p-model-info-left-top dd > a').text()   # 名字
        dir_path = self.deal.mkDir(name)   #新建名字文件夹，采用deal类，mkDir方法
        brief = response.doc('.mm-aixiu-content').text()
        if dir_path:
            imgs = response.doc('.mm-aixiu-content img').items()  #提取图片
            count = 1
            self.deal.saveBrief(brief, dir_path, name)   # 保存图片
            for img in imgs:
                url = img.attr.src   #图片地址
                if url:
                    extension = self.deal.getExtension(url)
                    file_name = name + str(count) + '.' + extension
                    count += 1
                    self.crawl(img.attr.src, callback=self.save_img,
                               save={'dir_path': dir_path, 'file_name': file_name},validate_cert=False)
 
    def save_img(self, response):
        content = response.content
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
        self.deal.saveImg(content, file_path)
 
 
import os
 
class Deal:
    def __init__(self):
        self.path = DIR_PATH     # DIR_PATH 自定义路径
        if not self.path.endswith('/'):   # endswith() 方法用于判断字符串是否以指定后缀结尾，如果以指定后缀结尾返回True，否则返回False。
            self.path = self.path + '/'   
        if not os.path.exists(self.path):  #判断路径是否存在
            os.makedirs(self.path)   #makedirs 用来创建目录树
 
    def mkDir(self, path):
        path = path.strip() #移除空格
        dir_path = self.path + path   #创建目录下子路径
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path
 
    def saveImg(self, content, path):   #写入文件
        f = open(path, 'wb')
        f.write(content)
        f.close()
 
    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"   #目录 + 名称 + 图片
        f = open(file_name, "wb+")
        f.write(str(content.encode('utf-8')))
 
    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension