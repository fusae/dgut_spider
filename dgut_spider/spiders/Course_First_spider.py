import scrapy
from dgut_spider.items import CourseItem
import os
import re
import json
from scrapy.selector import Selector

XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'

class CourseSpider(scrapy.Spider):
    name = 'Course'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.CoursePipeline': 300
                }
            }

    def __init__(self):
        self.fXNXQ = open(XNXQName, 'r')
        self.XNXQ = None

 
    def start_requests(self):
        for eachline in self.fXNXQ:
            js = json.loads(eachline)
            self.XNXQ = js['num']
            url = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/Private/List_XNXQKC.aspx?xnxq=%s' % self.XNXQ
            request = scrapy.Request(url, callback=self.parse)
            request.meta['XNXQ'] = self.XNXQ
            yield request

    def parse(self, response):
        # find the value, courseNum, text and XNXQ
        body = response.body.decode('gbk')
        r = re.findall(r"innerHTML='(.*)';</script>", body)
        if r:
            sel = Selector(text=r[0])
            value = sel.xpath('//select[contains(@name, "Sel_KC")]/option/@value').extract()
            tmpText = sel.xpath('//select[contains(@name, "Sel_KC")]/option/text()').extract()
            tmpText = tmpText[1:]
            text = []
            courseNum = []
            for each in tmpText:
                each = each.split('|')
                courseNum.append(each[0])
                text.append(each[1])

            for i in range(len(value)):
                item = CourseItem()
                item['value'] = value[i]
                item['courseNum'] = courseNum[i]
                item['text'] = text[i]
                item['XNXQ'] = response.meta['XNXQ']
                yield item

