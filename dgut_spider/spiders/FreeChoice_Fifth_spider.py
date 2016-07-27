import scrapy
from dgut_spider.items import FifthParamItem

class FreeChoiceCourseSpider(scrapy.Spider):
    name = "FifthParam"
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.FifthParamPipeline': 300
                }
            }

    start_urls = ['http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RXKBSel.aspx']

    def parse(self, response):
        values = response.xpath('//select[contains(@name, "Sel_XQXX")]/option/@value').extract()
        values = values[1:]
        texts = response.xpath('//select[contains(@name, "Sel_XQXX")]/option/text()').extract()

        i = 0
        for value in values:
            item = FifthParamItem()
            item['value'] = value
            item['text'] = texts[i]
            i += 1
            yield item

