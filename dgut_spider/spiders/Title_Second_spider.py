import scrapy
from dgut_spider.items import TitleItem

class TitleSpider(scrapy.Spider):
    name = 'Title'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.TitlePipeline': 300
                }
            }

    start_urls = ['http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx']

    def parse(self, response):
        
        desc = response.xpath('//select[contains(@id, "sel_zc")]/option/text()').extract()
        num = response.xpath('//select[contains(@id, "sel_zc")]/option/@value').extract()
        
        num = num[1:]
        for i in range(len(desc)):
            item = TitleItem()
            item['text'] = desc[i]
            item['num'] = num[i]
            yield item
