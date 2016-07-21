import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.handlePic import handle
from urllib.parse import urlencode

class GetClassCourseSpider(scrapy.Spider):
    name = 'ClassCourse'

    def __init__(self):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_ClassSel.aspx' # first
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx' # third
        self.CourseUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/drawkbimg.aspx'
        self.findSessionId = None # to save the cookies

    def start_requests(self):
        request = scrapy.Request(self.getUrl,
                callback = self.downloadPic)
        yield request

    def downloadPic(self, response):
        # download the picture
        # find the session id
        self.findSessionId = response.headers.getlist('Set-Cookie')[0].decode().split(';')[0].split('=')
        request = scrapy.Request(self.vcodeUrl,
                cookies = {self.findSessionId[0]: self.findSessionId[1]},
                callback = self.getAndHandleYzm)
        yield request

    def getAndHandleYzm(self, response):
        yzm = handle(response.body)

        yield FormRequest(self.postUrl,
                formdata = {'Sel_XNXQ': '20151',
                            'Sel_XZBJ': '1101201201',
                            'txt_yzm': yzm,
                            'txtzxbj': '',
                            'type': '2'},
                headers = {
                    'Referer': self.getUrl,
                    'Cookies': self.findSessionId[0] + '=' + self.findSessionId[1]
                    },
                callback = self.parse
                )

    def parse(self, response):
        body = response.body.decode('gbk')
        num = body.find('alert')
        if num != -1:
            yield scrapy.Request(self.vcodeUrl+'?t='+'%.f' % (datetime.now().microsecond / 1000),
                    headers = {
                        'Referer': self.getUrl,
                        'Cookies': self.findSessionId[0] + '=' + self.findSessionId[1]
                        },
                    callback = self.getAndHandleYzm
                    )

        else:
            sel = Selector(text = body)
            # to find the src tag, find the url
            self.CourseUrl = sel.xpath('//img/@src').extract()[0]
            self.CourseUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/' + self.CourseUrl

            headers = {#'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1],
                'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_ClassSel_rpt.aspx',
                   'User-Agert': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
                }
            request = Request(self.CourseUrl, headers = headers, callback = self.parseData
                    )
            yield request

    def parseData(self, response):
        with open('three', 'wb') as f:
            f.write(response.body)
        

