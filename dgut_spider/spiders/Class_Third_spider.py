import scrapy
from dgut_spider.items import ClassItem

class ClassSpider(scrapy.Spider):
    name = 'Class'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.ClassPipeline': 300
                }
            }

    start_urls = ['http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_ClassSel.aspx']

    def parse(self, response):
        text = response.xpath('//select[contains(@name, "Sel_XZBJ")]/option/text()').extract()
        num = response.xpath('//select[contains(@name, "Sel_XZBJ")]/option/@value').extract()

        for i in range(len(text)):
            item = ClassItem()
            item['text'] = text[i]
            item['num'] = num[i]
            yield item

