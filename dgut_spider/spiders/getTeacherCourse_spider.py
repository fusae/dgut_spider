import scrapy
from scrapy.http import FormRequest
import json
import os
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.handlePic import handle
from dgut_spider.items import DetailProfItem
import re

class GetTeacherCourseSpider(scrapy.Spider):
    name = 'TeacherCourse'

    def __init__(self):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx' # first
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB_rpt.aspx' # third
        self.findSessionId = None # to save the cookies

    def start_requests(self):
        request = scrapy.Request(self.getUrl,
               callback = self.downloadPic)
        yield request

    def downloadPic(self, response):
        # download the picture
        # find the session id
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=")
        request = scrapy.Request(self.vcodeUrl,
                cookies= {self.findSessionId[0]: self.findSessionId[1]},
                callback = self.getAndHandleYzm)
        yield request
    
    def getAndHandleYzm(self, response):
        yzm = handle(response.body)
        
        yield FormRequest(self.postUrl,
                formdata={'Sel_XNXQ': '20151',
                          'sel_zc': '011',
                          'txt_yzm': yzm,
                          'type': '2'},
                headers={
                    'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx',
                    'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1],
                    },


                callback=self.parse)

    def parse(self, response):
        body = response.body.decode('gb2312')
        num = body.find('alert')
        if num != -1:
            # means CAPTCHA validation fails, need to re-request the CAPTCHA
            yield scrapy.Request(self.vcodeUrl+'?t='+'%.f' % (datetime.now().microsecond / 1000),
            headers={
                    'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx',
                    'Cookie': self.findSessionId[0]+'='+self.findSessionId[1]
                    },
            callback=self.getAndHandleYzm)

        else:
            # parse data
            self.parseData(body)



    def parseData(self, body):
        # parse body data
        sel = Selector(text=body)

        XXNQ = '20151' # test

        # department, teacher, gender and title
        temp1 = sel.xpath('//*[@group="group"]/table/tr/td/text()').extract() 
        
        for each in temp1:
            each = each.replace(u'\xa0', u'  ')
            print(each.split('   '))

        # get all the note data by regular expressions
        noteTables = sel.xpath('//table[@style="border:0px;"]').extract()
        for noteTable in noteTables:
            if '<b>'  in noteTable:
                sele = Selector(text = noteTable)
                note = (sele.xpath('//table/tr/td/b/text()').extract())
                noteText = (sele.xpath('//table/tr/td/text()').extract())

        # get all the course data
        courseTables = sel.xpath('//table[@class="page_table"]/tbody').extract()
        
        for table in courseTables:

            s = Selector(text = table)
            trs = s.xpath('//tr').extract()
            for tr in trs:
                sel = Selector(text = tr)
                snum = (sel.xpath('//td[1]/text()').extract())
                course = (sel.xpath('//td[2]/text()').extract())
                credit = (sel.xpath('//td[3]/text()').extract())
                teachWay = (sel.xpath('//td[4]/text()').extract())
                courseType = (sel.xpath('//td[5]/text()').extract())
                classNum = (sel.xpath('//td[6]/text()').extract())
                className = (sel.xpath('//td[7]/text()').extract())
                stuNum = (sel.xpath('//td[8]/text()').extract())
                week = (sel.xpath('//td[9]/text()').extract())
                section = (sel.xpath('//td[10]/text()').extract())
                location = (sel.xpath('//td[11]/text()').extract())

                tmpList = []
                tmpList.append(snum)
                tmpList.append(course)
                tmpList.append(credit)
                tmpList.append(teachWay)
                tmpList.append(courseType)
                tmpList.append(classNum)
                tmpList.append(className)
                tmpList.append(stuNum)
                tmpList.append(week)
                tmpList.append(section)
                tmpList.append(location)

                # to know whether every variable is empty
                detailList = []
                for each in tmpList:
                    if not each:
                        each = ''
                    else:
                        each = each[0]
                    detailList.append(each)

                print(detailList)


