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

    def __init__(self, *args, **kwargs):
        super(GetXNXQCourseSpider, self).__init__(*args, **kwargs)
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel_rpt.aspx' # the form data summit to this url
        self.XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
        self.CourseName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/Course.json'
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx'
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx' # first we get this url
        self.findSessionId = None # to save the cookies
        self.selXNXQ = None # the data to be posted
        self.selKC = None # the data to be posted

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

    def getParmsFromFile(self, response):
#    def start_requests(self):
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=") 
        f = open('file', 'w')
        # first, open XNXQ.json and find num and text
        fXNXQ = open(self.XNXQName, 'r')

        for eachline in fXNXQ:
            js = json.loads(eachline)
            self.selXNXQ = js['num']
            XNXQText = js['text']

            # second, open Course.json and find value via XNXQText
            fCourse = open(self.CourseName, 'r')

            for eachline in fCourse:
                courseJs = json.loads(eachline)
                if courseJs['XNXQ'] == XNXQText:
                    self.selKC = courseJs['value']
#                    print(self.selXNXQ, self.selKC)
                    line = '%s %s\n' % (self.selXNXQ, self.selKC)
                    f.write(line)
                    
                    
                    request = scrapy.Request(self.vcodeUrl+'?t='+'%.f' % (datetime.now().microsecond/1000), 
                    headers= { 
                        'Host': 'jwxt.dgut.edu.cn',

                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

                        'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

                        'Accept-Encoding': 'gzip, deflate',

                        'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_LessonSel.aspx',

                        'Cookie': self.findSessionId[0]+'='+self.findSessionId[1],

                        'Connection': 'keep-alive'},

                    callback=self.downloadPic)
                    yield request

#                    yield self.after_start_requests()



    def start_requests(self):
#    def after_start_requests(self):
        request = scrapy.Request(self.getUrl, 
        headers= { 
            'Host': 'jwxt.dgut.edu.cn',

            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',

            'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',

            'Accept-Encoding': 'gzip, deflate',

            'Connection': 'keep-alive',

            'Cache-Control': 'max-age=0'},

        callback=self.getParmsFromFile)
        yield request

    def downloadPic(self, response):
        # download the picture
        # find the session id
#        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(";")[0].split("=") 
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
        body = response.body.decode('gbk')
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
            print(body)
            sel = Selector(text=body)
            print(sel.xpath('//*[@id="pageRpt"]/tr/td/table[1]/tr[1]/td/b/font/text()').extract()[0])
            print(sel.xpath('//*[@id="pageRpt"]/tr/td/table[1]/tr[2]/td/text()').extract()[0])
            print(sel.xpath('//*[@id="pageRpt"]/tr/td/table[2]/tr/td/text()').extract()[0])

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

            # Ò»toÁù
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
#                        print(tmp)

                course[weekName[i]] = tmp
            
            item = DetailItem()
            item['table'] = course
            print(item['table'])

#            for key, value in course.items():
#                print('%s: %s' % (key, value))
            




            

