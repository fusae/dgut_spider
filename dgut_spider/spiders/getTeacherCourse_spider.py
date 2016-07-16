import scrapy
from scrapy.http import FormRequest
import json
import os
from datetime import datetime
from scrapy.selector import Selector
from dgut_spider.handlePic import handle
# the item that store crawled data

class GetTeacherCourseSpider(scrapy.Spider):
    name = 'TeacherCourse'

    def __init__(self):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx' # first
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB_rpt.aspx'
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
                    'Host': 'jwxt.dgut.edu.cn',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh,en-US;q=0.8,zh-CN;q=0.5,en;q=0.3',
                    'Referer': 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/TeacherKBFB.aspx',
                    'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1],
                    'Connection': 'keep-alive'
                    },


                callback=self.parse)

    def parse(self, response):
        print(response.body.decode('gb2312'))





