import json
import os
import subprocess

XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
TitleName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/Title.json'

# first, open XNXQ.json and find num and text
fXNXQ = open(XNXQName, 'r')
for eachline in fXNXQ:
    js = json.loads(eachline)
    selXNXQ = js['num']

    # second, open Title.json and find title code
    fTitle = open(TitleName, 'r')
    for eachline in fTitle:
        titleJs = json.loads(eachline)
        titleCode = titleJs['num'] # title code

        # call the spider
        command = 'scrapy crawl TeacherCourse -a selXNXQ=%s -a titleCode=%s' % (selXNXQ, titleCode)
        subprocess.call(command, shell=True)
