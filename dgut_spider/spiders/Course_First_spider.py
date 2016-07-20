import scrapy
from dgut_spider.items import CourseItem
import os
import re
import json

class CourseSpider(scrapy.Spider):
    name = 'Course'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.CoursePipeline': 300
                }
            }
    
    def __init__(self, *args, **kwargs):
        super(CourseSpider, self).__init__(*args, **kwargs)
        self.url = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/Private/List_XNXQKC.aspx?xnxq='
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx'

        self.XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
        self.XNXQs = {}

    def openDataFile(self, fileName):
        if not os.path.exists(fileName):
            print("Error, file %s doesn't exist " % fileName)
            os._exit(-1)

        f = open(fileName, 'r')
        for eachline in f:
            js = json.loads(eachline)
            self.XNXQs[js['text']] = js['num'] # json -> dict

        f.close()

    def start_requests(self):
        yield scrapy.Request(self.getUrl, callback=self.requestForCourse)


    def requestForCourse(self, response):
        findSessonId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=")

        self.openDataFile(self.XNXQName)
        
        for key, value in self.XNXQs.items():
            request = scrapy.Request(self.url+value,
            headers={
                'Host': 'jwxt.dgut.edu.cn',

                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

                'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

                'Accept-Encoding': 'gzip, deflate',

                'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx',

                'Cookie': findSessonId[0]+'='+findSessonId[1],

                'Connection': 'keep-alive'},

                    callback=self.parse)
            request.meta['text'] = key
            yield request

    def parse(self, response):
        # find the value, courseNum, text and XNXQ
        body = response.body.decode('gbk')
        result = re.findall(r'<option value=([0-9]{6}>[0-9]{6,8}\|.+?)</option>', body)
        for each in result:
            item = CourseItem()
            tmp1 = each.split('>')
            item['value'] = tmp1[0]
            tmp2 = tmp1[1].split('|')
            item['courseNum'] = tmp2[0]
            item['text'] = tmp2[1]
            item['XNXQ'] = response.meta['text']
            yield item
        
        
