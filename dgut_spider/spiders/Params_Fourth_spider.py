import scrapy
from scrapy.selector import Selector
from dgut_spider.items import ClassroomItem
import re

class ParamsFourthSpider(scrapy.Spider):
    name = 'ParamsFourth'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.ParamsFourthPipeline': 300
                }
            }


    def __init__(self):
        self.getCampusUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RoomSel.aspx' # first
        self.getTeachBuildUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/Private/List_JXL.aspx?' # second
        self.getClassroomUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/Private/List_ROOM.aspx?' # third
        self.findSessionId = None


    def start_requests(self):
        request = scrapy.Request(self.getCampusUrl, callback=self.parseCampus)
        yield request

    def parseCampus(self, response):
        CampusValue = response.xpath('//select[contains(@name, "Sel_XQ")]/option/@value').extract()
        CampusText = response.xpath('//select[contains(@name, "Sel_XQ")]/option/text()').extract()
        CampusValue = CampusValue[1:]
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=")

        for i in CampusValue:
            index = CampusValue.index(i)
            getTeachBuildUrl = self.getTeachBuildUrl + 'id=%s&width=240' % i
            request = scrapy.Request(getTeachBuildUrl, 
                                     headers = {
                                         'Cookies': self.findSessionId[0] + '=' + self.findSessionId[1],
                                         'Referer': self.getCampusUrl
                                         },
                                     callback = self.parseTeachBuilding)
            
            request.meta['XQ'] = i
            yield request


    def parseTeachBuilding(self, response):
        body = response.body.decode('gbk')
        r = re.findall(r"innerHTML='(.*)';</script>", body)
        if r:
            sel = Selector(text=r[0])
            TeachBuildValue = sel.xpath('//select[contains(@name, "Sel_JXL")]/option/@value').extract()
            TeachBuildValue = TeachBuildValue[1:]
            TeachBuildText = sel.xpath('//select[contains(@name, "Sel_JXL")]/option/text()').extract()

            for i in TeachBuildValue:
                index = TeachBuildValue.index(i)

                getClassroomUrl = self.getClassroomUrl + 'id=%s&width=240' % i
                request = scrapy.Request(getClassroomUrl, 
                                         headers = {
                                             'Cookies': self.findSessionId[0] + '=' + self.findSessionId[1],
                                             'Referer': self.getCampusUrl
                                             },
                                         callback = self.parseClassroom)
                XQ = response.meta['XQ']
                request.meta['XQ'] = XQ
                request.meta['JXL'] = i
                yield request


    def parseClassroom(self, response):
        body = response.body.decode('gbk')
        r = re.findall(r"innerHTML='(.*)';</script>", body)
        if r:
            sel = Selector(text=r[0])
            ClassroomValue = sel.xpath('//select[contains(@name, "Sel_ROOM")]/option/@value').extract()
            ClassroomValue = ClassroomValue[1:]
            ClassroomText = sel.xpath('//select[contains(@name, "Sel_ROOM")]/option/text()').extract()

            for i in ClassroomValue:
                index = ClassroomValue.index(i)
                item = ClassroomItem()
                item['XQ'] = response.meta['XQ']
                item['JXL'] = response.meta['JXL']
                item['room'] = i
                yield item

