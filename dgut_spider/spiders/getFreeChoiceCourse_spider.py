import scrapy
from dgut_spider.handlePic import handle
from datetime import datetime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from dgut_spider.items import FreeChoiceItem


class FreeChoiceSpider(scrapy.Spider):
    name = "FreeChoice"

    def __init__(self):
        self.getUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RXKBSel.aspx' # first 
        self.vcodeUrl = 'http://jwxt.dgut.edu.cn/jwweb/sys/ValidateCode.aspx' # second
        self.postUrl = 'http://jwxt.dgut.edu.cn/jwweb/ZNPK/KBFB_RXKBSel_rpt.aspx' # third
        self.findSessionId = None # to save cookies


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
                formdata={
                        'Sel_XNXQ': '20151',
                        'Sel_XQXX': '1',
                        'txt_yzm': yzm
                        },
                headers = {
                        'Referer': self.getUrl,
                        'Cookie': self.findSessionId[0] + '=' + self.findSessionId[1]
                    },
                callback=self.parse)

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
            sel = Selector(text=body)
            table = sel.xpath('/html/body/table[2]/td').extract()


            i = 0
            j = 10
            while i != len(table):
                everyRow = table[i:j] # len(tmp) == 10, it means every row, 10 column data
                
                tmpList = []
                rowList = []
                for each in everyRow:
                    selText = Selector(text=each)
                    data = selText.xpath('//td/text()').extract()
                    tmpList.append(data)

                # if tmpList[index] is empty, then make tmpList[index] == ''
                for each in tmpList:
                    if not each: # empty list
                        rowList.append('')
                    else:
                        rowList.append(each[0])

                item = FreeChoiceItem()
                item['snum'] = rowList[0]
                item['course'] = rowList[1]
                item['credit'] = rowList[2]
                item['teacher'] = rowList[3]
                item['title'] = rowList[4]
                item['classNum'] = rowList[5]
                item['stuNum'] = rowList[6]
                item['week'] = rowList[7]
                item['classTime'] = rowList[8]
                item['location'] = rowList[9]

                print(item)

                i += 10
                j += 10
                
