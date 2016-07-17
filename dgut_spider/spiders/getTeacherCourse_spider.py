# -*- coding: gb2312 -*-
import scrapy
from scrapy.http import FormRequest
import json
import os
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.handlePic import handle
from dgut_spider.items import DetailProfItem
from dgut_spider.items import DetailProfCourseItem

class GetTeacherCourseSpider(scrapy.Spider):
    name = 'TeacherCourse'

    def __init__(self):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx' # first
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB_rpt.aspx' # third
        self.findSessionId = None # to save the cookies
        self.XNXQ = '20151'

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
                formdata={'Sel_XNXQ': self.XNXQ,
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

        # get all the note text data
        noteTables = sel.xpath('//table[@style="border:0px;"]').extract()

        noteList = [] # to store all the note text
        for noteTable in noteTables:
            if '<b>'  in noteTable:
                sele = Selector(text = noteTable)
                note = (sele.xpath('//table/tr/td/b/text()').extract())
                noteText = (sele.xpath('//table/tr/td/text()').extract())
                # combine note and noteText
                if not noteText:
                    noteText.append('')
                    noteText.append('')
                else:
                    if len(noteText) == 1:
                        noteText.append('')
                noteList.append(noteText)


        # get all the course data
        courseTables = sel.xpath('//table[@class="page_table"]/tbody').extract()
        
        AllDetailCourse = [] # all the teachers' course
        for table in courseTables:
            everyTeacherC = [] # every teacher's course
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
                detailCourse = []
                for each in tmpList:
                    if not each:
                        each = ''
                    else:
                        each = each[0]
                    detailCourse.append(each)

                everyTeacherC.append(detailCourse)

            AllDetailCourse.append(everyTeacherC)

        # get department, teacher, gender and title
        sel = Selector(text = body)
        temp1 = sel.xpath('//*[@group="group"]/table/tr/td/text()').extract() 


        # fill two tables, which will store in the database
        i = 0
        # every professor
        for each in temp1:
            tables = [] # all the data in every for loop to send to the pipeline 

            each = each.replace(u'\xa0', u'  ')
            each = each.split('   ')
            depart = each[0].split('：')
            teacher = each[1].split('：')
            gender = each[2].split('：')
            title = each[3].split('：')

            # first table
            profItem = DetailProfItem()
            profItem['XNXQ'] = self.XNXQ
            profItem['department'] = depart[1] # department
            profItem['teacher'] = teacher[1] # teacher
            profItem['gender'] = gender[1]
            profItem['title'] = title[1]
            profItem['note1'] = noteList[i][0]
            profItem['note2'] = noteList[i][1]
            tables.append(profItem) # add the first table

            # second table
            # every professor's courses
            profCourses = []
            for j in range(len(AllDetailCourse[i])): # how many course for every professor
                profCourseItem = DetailProfCourseItem() # every course for every professor
                profCourseItem['snum'] = AllDetailCourse[i][j][0] # i means i-th professor, j means j-th course, third num means what position of the course
                profCourseItem['course'] = AllDetailCourse[i][j][1]
                profCourseItem['credit'] = AllDetailCourse[i][j][2]
                profCourseItem['teachWay'] = AllDetailCourse[i][j][3]
                profCourseItem['courseType'] = AllDetailCourse[i][j][4]
                profCourseItem['classNum'] = AllDetailCourse[i][j][5]
                profCourseItem['className'] = AllDetailCourse[i][j][6]
                profCourseItem['stuNum'] = AllDetailCourse[i][j][7]
                profCourseItem['week'] = AllDetailCourse[i][j][8]
                profCourseItem['section'] = AllDetailCourse[i][j][9]
                profCourseItem['location'] = AllDetailCourse[i][j][10]
                profCourses.append(profCourseItem) # every professor's courses

            tables.append(profCourses) # add the second table
            print(tables)
            print('--------------------------------')
            i += 1
