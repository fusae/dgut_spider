import json
import os
import subprocess


XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
CourseName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/Course.json'

# first, open XNXQ.json and find num and text
fXNXQ = open(XNXQName, 'r')
for eachline in fXNXQ:
    js = json.loads(eachline)
    selXNXQ = js['num']
    XNXQText = js['text']

    # sencod, open Course.json and find value via XNXQText
    fCourse = open(CourseName, 'r')
    for eachline in fCourse:
        courseJs = json.loads(eachline)
        if courseJs['XNXQ'] == selXNXQ:
            selKC = courseJs['value']
            
            # call the spider
            command = 'scrapy crawl XNXQCourse -a selXNXQ=%s -a selKC=%s' % (selXNXQ, selKC)
            subprocess.call(command, shell=True)


