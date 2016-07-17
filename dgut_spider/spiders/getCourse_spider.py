# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import json
import os
from PIL import Image
from PIL import ImageEnhance, ImageFilter
import pytesseract
import io
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.items import DetailItem

class GetXNXQCourseSpider(scrapy.Spider):
    name = 'XNXQCourse'

    def __init__(self, selXNXQ='', selKC=''):
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel_rpt.aspx' # the form data summit to this url
        self.XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
        self.CourseName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/Course.json'
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx'
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx' # first we get this url
        self.findSessionId = None # to save the cookies
        self.selXNXQ = selXNXQ # the data to be posted
        self.selKC = selKC # the data to be posted

    def handlePic(self, content):
        # img = Image.open('yzm.gif') # This will make an error
        img = Image.open(io.BytesIO(content)) 
        img = img.convert('RGBA')
        pix = img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 95 or pix[x, y][1] < 95 or pix[x, y][2] < 95:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)

        img.save('temp.jpg')

        im = Image.open("temp.jpg")
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert('1')
        im.save('temp2.jpg')
        text = pytesseract.image_to_string(Image.open('temp2.jpg'))

        os.remove('temp.jpg')
        os.remove('temp2.jpg')
        text = text.replace(' ','')
        text = text.upper()

        return text


    def start_requests(self):
        request = scrapy.Request(self.getUrl, 
        headers= { 
            'Host': 'jwxt.dgut.edu.cn',

            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

            'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

            'Accept-Encoding': 'gzip, deflate',

            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0'},

        callback=self.downloadPic)
        yield request

    def downloadPic(self, response):
        # download the picture
        # find the session id
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=") 
        request = scrapy.Request(self.vcodeUrl, 
#                cookies={self.findSessionId[0]:self.findSessionId[1], 
#                    'path': '/'},
                   headers = { 
                            'Host': 'jwxt.dgut.edu.cn',

                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

                            'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

                            'Accept-Encoding': 'gzip, deflate',


                            'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx',

                            'Cookie': self.findSessionId[0]+'='+self.findSessionId[1],

                            'Connection': 'keep-alive'},
                callback=self.getAndHandleYzm)
        yield request

    def getAndHandleYzm(self, response):
#        with open('yzm.gif', 'wb') as f:
#            f.write(response.body)
        yzm = self.handlePic(response.body)
#            print(yzm)
#        yzm = input("yzm:")
#        print(yzm)


        yield FormRequest(self.postUrl,
#                formdata={'Sel_XNXQ': '20151',
#                          'Sel_KC': '011691',
#                          'txt_yzm': yzm},
#                cookies={self.findSessionId[0]:self.findSessionId[1],
#                    'path': '/'},
#                meta={'dont_merge_cookies': True},
                formdata={'Sel_XNXQ': self.selXNXQ,
                          'Sel_KC': self.selKC,
                          'txt_yzm': yzm},
                headers = { 
                        'Host': 'jwxt.dgut.edu.cn',

                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

                        'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

                        'Accept-Encoding': 'gzip, deflate',

                        'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx',

                        'Cookie': self.findSessionId[0]+'='+self.findSessionId[1],

                        'Connection': 'keep-alive'},

                callback=self.parse)

    def parse(self, response):
        body = response.body.decode('gb2312')
        num = body.find('alert')
        if num != -1:
            # means CAPTCHA validation fails, need to re-request the CAPTCHA

            yield scrapy.Request(self.vcodeUrl+'?t='+'%.f' % (datetime.now().microsecond/1000),
        headers= { 
            'Host': 'jwxt.dgut.edu.cn',

            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

            'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

            'Accept-Encoding': 'gzip, deflate',

            'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx',

            'Cookie': self.findSessionId[0]+'='+self.findSessionId[1],

            'Connection': 'keep-alive'},

            callback=self.getAndHandleYzm)
        else:
            # parse data
#            print(body)
            sel = Selector(text=body)
            # DGUT Title
            title = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[1]/tr[1]/td/b/font/text()').extract()[0])
            # XNXQ
            XNXQ = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[1]/tr[2]/td/text()').extract()[0])
            # need to be cut 
            temp1 = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[2]/tr/td/text()').extract()[0])

            # MON-SUN
            MON = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[2]/text()').extract()[0])
            TUE = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[3]/text()').extract()[0])
            WED = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[4]/text()').extract()[0])
            THU = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[5]/text()').extract()[0])
            FRI = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[6]/text()').extract()[0])
            SAT = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[7]/text()').extract()[0])
            SUN = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[1]/td[8]/text()').extract()[0])
            weekName = [MON, TUE, WED, THU, FRI, SAT, SUN]
#            print(weekName)

            # ONE to SIX
            ONE = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[2]/td[2]/text()').extract()[0])
            TWO = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[3]/td[1]/text()').extract()[0])
            THR = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[4]/td[2]/text()').extract()[0])
            FOU = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[5]/td[1]/text()').extract()[0])
            FIV = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[6]/td[2]/text()').extract()[0])
            SIX = (sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[7]/td[1]/text()').extract()[0])
            courseNum = []
            courseNum.append(ONE)
            courseNum.append(TWO)
            courseNum.append(THR)
            courseNum.append(FOU)
            courseNum.append(FIV)
            courseNum.append(SIX)
#            print(courseNum)

            firstCourse = []
            thirdCourse = []
            fifthCourse = []
            for i in range(3, 10):
                firstCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[2]/td[%d]/text()' % i).extract())
                thirdCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[4]/td[%d]/text()' % i).extract())
                fifthCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[6]/td[%d]/text()' % i).extract())


            secondCourse = []
            fourthCourse = []
            sixthCourse = []
            for i in range(2, 9):
                secondCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[3]/td[%d]/text()' % i).extract())
                fourthCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[5]/td[%d]/text()' % i).extract())
                sixthCourse.append(sel.xpath('//*[@id="pageRpt"]/tr/td/table[3]/tr[7]/td[%d]/text()' % i).extract())
            
#            print(firstCourse)
#            print(secondCourse)
#            print(thirdCourse)
#            print(fourthCourse)
#            print(fifthCourse)
#            print(sixthCourse)
            
            # call like course[MON][ONE] which means the first course on the monday
            course = {}
            for i in range(len(weekName)): # i: 0-6
                tmp = {}
                tmp[ONE] = firstCourse[i]
                tmp[TWO] = secondCourse[i]
                tmp[THR] = thirdCourse[i]
                tmp[FOU] = fourthCourse[i]
                tmp[FIV] = fifthCourse[i]
                tmp[SIX] = sixthCourse[i]
#                print(tmp)

                # to save shoule be cleared keys
                clearList = []
                # now clear those empty courses
                for each in tmp:
                    # if tmp[each] is a empty list
                    if not tmp[each]:
                        clearList.append(each)
                
                # now clear
                for each in clearList:
                    tmp.pop(each)

                # add it to the course dictionary, but not empty
                if not tmp:
                    continue;
                course[weekName[i]] = tmp


            # now seperate some sentences into few parts
            # some gbk decode problems
            temp1 = temp1.replace(u'\xa0', u' ')
            temp1 = (temp1.split('  '))
            # now turn list into dict
            d = {}
            for each in temp1:
                each = each.split('：')
                d[each[0]] = each[1]

            
            
#            print(title)
#            print(course)
#            print(len(course))


            for key, value in course.items():
                KEY = key # I don't know what is bug, but seems the key can change, just use the KEY to equal key
                item = DetailItem()
                item['XNXQ'] = XNXQ
                item['college'] = d['承担单位']
                item['name'] = d['课程']
                item['hours'] = d['总学时']
                item['credit'] = d['总学分']
                teacher = None # Teacher's name
                classTime = None # class time
                location = None # where to have class
                className = None # class name
                stuNum = None # the number of students
                temp2 = None # for store temp data

                for akey, avalue in value.items():
                    avalue = str(avalue[0]) # list -> str
                    # there are some classes which have comma
                    if ',' in avalue:
                        avalue = avalue.split(' ', 4)
                        teacher = avalue[0]
                        classTime = KEY + ': ' + avalue[1] + avalue[2]
                        location = avalue[3]
                        temp2 = avalue[4]
                    else:
                        avalue = avalue.split(' ', 3) # seperate into few parts
                        teacher = avalue[0] # teacher
                        classTime = KEY + ': ' + avalue[1] # classTime
                        location = avalue[2] # location
                        temp2 = avalue[3] # needed to be seperate again
                    temp2 = temp2.split('\r\n')
                    if '；' in temp2[0]: # it means whether there is a class
                        className = temp2[0].split('；')[1]
                    else:
                        className = 'None'
                    stuNum = temp2[1].split('：')[1]
                    item['teacher'] = teacher
                    item['classTime'] = classTime
                    item['location'] = location
                    item['className'] = className
                    item['stuNum'] = stuNum

                    # convert gb2312 to utf-8
                    for key, value in item.items():
                        value = value.encode('utf-8').decode('utf-8')
                    yield item

#                print('%s: %s' % (key, value))



