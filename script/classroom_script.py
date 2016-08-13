# -*- coding: utf-8 -*-
import json
import os
import subprocess

XNXQName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/XNXQ.json'
ParamsName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data/ParamsFourth.json'
LOGPATH = '/home/fusae/PycharmProjects/dgut_spider/spider_log/classroom.log'

# first, open XNXQ.json and find num and text
fXNXQ = open(XNXQName, 'r')
for eachline in fXNXQ:
    js = json.loads(eachline)
    selXNXQ = js['num']

    # second, open ParamsFourth.json and find other parameters
    fParams = open(ParamsName, 'r')
    for eachline in fParams:
        paramJs = json.loads(eachline)
        Sel_JXL = paramJs['JXL']
        if Sel_JXL == '117': # 暂不处理第一行
            continue
        Sel_ROOM = paramJs['room']
        Sel_XQ = paramJs['XQ']

        # call the spider
        command = 'scrapy crawl Classroom -a Sel_JXL=%s -a Sel_ROOM=%s -a Sel_XNXQ=%s -a Sel_XQ=%s 2>&1 | tee -a %s' % (Sel_JXL, Sel_ROOM, selXNXQ, Sel_XQ, LOGPATH)
        subprocess.call(command, shell=True)
