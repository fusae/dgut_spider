import scrapy
from dgut_spider.items import XNXQItem

class XNXQSpider(scrapy.Spider):
    name = 'XNXQ'
        
    def start_requests(self):
        request = scrapy.Request('http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx', callback=self.parse)
        yield request

    def parse(self, response):
        # find the year and semester
        items = []
        # to get description of the every year and semester
        desc = response.xpath('//select[contains(@name, "Sel_XNXQ")]/option/text()').extract()
        # to get the every year and semester num
        num = response.xpath('//select[contains(@name, "Sel_XNXQ")]/option/@value').extract()
        for i in range(len(desc)):
            item = XNXQItem()
            item['text'] = desc[i]
            item['num'] = num[i]
            yield item
        

