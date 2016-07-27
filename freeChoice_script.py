import json
import os
import subprocess

XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
XQXXName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/FifthParam.json'

# first, open XNXQ.json and find num and text
fXNXQ = open(XNXQName, 'r')
for eachline in fXNXQ:
    js = json.loads(eachline)
    selXNXQ = js['num']

    # second, open FifthParam.json and find other parameter
    fParam = open(XQXXName, 'r')
    for eachline in fParam:
        paramJs = json.loads(eachline)
        selXQ = paramJs['value']

        # call the spider
        command = 'scrapy crawl FreeChoice -a Sel_XNXQ=%s -a Sel_XQXX=%s' % (selXNXQ, selXQ)
        subprocess.call(command, shell=True)
