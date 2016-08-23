#-*- coding: gbk -*-
import scrapy
import sys
from scrapy.http import FormRequest
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.handlePic import handle
from dgut_spider.items import RoomItem
from dgut_spider.items import RoomCourseMessageItem
from dgut_spider.items import containItem

class GetClassroomSpider(scrapy.Spider):
    name = 'Classroom'
    custom_settings = {
            'ITEM_PIPELINES': {
                'dgut_spider.pipelines.ClassroomPipeline': 200,
                }
            }

    def __init__(self, Sel_JXL='', Sel_ROOM='', Sel_XNXQ='', Sel_XQ=''):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RoomSel.aspx' # first
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RoomSel_rpt.aspx' # third
        self.findSessionId = None # to save the cookies
        self.Sel_XQ = Sel_XQ
        self.Sel_JXL = Sel_JXL
        self.Sel_ROOM = Sel_ROOM
        self.Sel_XNXQ = Sel_XNXQ


    def start_requests(self):
        request = scrapy.Request(self.getUrl,
                callback = self.downloadPic)
        yield request

    def downloadPic(self, response):
        # download the picture
        # find the session id
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=")
        request = scrapy.Request(self.vcodeUrl,
                cookies = {self.findSessionId[0]: self.findSessionId[1]},
                callback = self.getAndHandleYzm)
        yield request

    def getAndHandleYzm(self, response):
        yzm = handle(response.body)

        yield FormRequest(self.postUrl,
                formdata={'Sel_JXL': self.Sel_JXL,
                          'Sel_ROOM': self.Sel_ROOM,
                          'Sel_XNXQ': self.Sel_XNXQ,
                          'Sel_XQ': self.Sel_XQ,
                          'txt_yzm': yzm},
                headers={
                        'Referer': self.getUrl,
                        'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1]
                    },
                callback = self.parse)

    def parse(self, response):
        body = response.body.decode('gbk').encode('utf-8').decode('utf-8')
        num = body.find('alert')
        if num != -1:
            yield scrapy.Request(self.vcodeUrl+'?t='+'%.f' % (datetime.now().microsecond / 1000),
                    headers = {
                        'Referer': self.getUrl,
                        'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1]
                        },
                    callback=self.getAndHandleYzm)
        
        else:

            select = Selector(text=body) # to find campus, teaching building and classroom
            temp3 = select.xpath('//*[@id="pageRpt"]/tr/td/table[2]/tr/td/text()').extract()
            if not temp3: # temp3 is empty, which means there is no class in this room
                sys.exit(0)

            temp3 = temp3[0].split('\xa0\xa0')
            # first table
            roomItem = RoomItem()
            campus = temp3[0].split('：')[1]
            building = temp3[1].split('：')[1]
            classroom = temp3[2].split('：')[1]
            roomItem['campus'] = campus
            roomItem['building'] = building
            roomItem['classroom'] = classroom

            note1 = select.xpath('//*[@id="pageRpt"]/tr/td/table[4]/tr/td/text()').extract()
            if not note1:
                note1 = ''
            else:
                note1 = note1[0]
            roomItem['note1'] = note1
            roomItem['XNXQ'] = self.Sel_XNXQ

            selTr = Selector(text=body)
#            trs = selTr.xpath('//table[contains(@border, "1")]/tr').extract()
            trs = selTr.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr').extract()

            WEEK = [] # to store weekday word
            selWeek = Selector(text=trs[0])
            tds1 = selWeek.xpath('//tr/td/text()').extract()
            weekTds = tds1[1:] # remove empty
            for td in weekTds:
                WEEK.append(td) # add weekday word


            data = {} # for store detail message
            for i in WEEK:
                data[i] = []

            trs = trs[1:] # remove week name
            for tr in trs:
                selTd = Selector(text=tr)
                tds = selTd.xpath('//tr/td[contains(@width, "13%")]').extract()
                # len(tds) == 7
                index = 0
                for td in tds:
                    seltd = Selector(text=td)
                    message = seltd.xpath('//td/text()').extract()
                    if message:
                        data[WEEK[index]].append(message[0])
                    else:
                        pass
                    index += 1

            # now split message from data dict
            ct = 1 # as a serial number of courses
            for k, v in data.items():
                if v:
                    for each in v:
                        each = each.split('\r\n')
                        for i in range(int(len(each) / 3)): # each maybe has one or more CourseMessage, you can print(each) for test
                            # second table
                            courseItem = RoomCourseMessageItem()
                            courseItem['courseName'] = each[i * 3 + 0]
                            courseItem['teacher'] = each[i * 3 + 1].split(' ')[0]
                            courseItem['classTime'] = k + each[i * 3 + 1].split(' ')[1]
                            courseItem['num'] = each[i * 3 + 2].split('：')[1]
                            courseItem['classroom'] = roomItem['classroom']
                            courseItem['snum'] = str(ct)
                            ct += 1

                            # third item to contain first and second
                            contain = containItem()
                            contain['first'] = roomItem
                            contain['second'] = courseItem
    #                        print(contain)

                            yield contain

        



            
