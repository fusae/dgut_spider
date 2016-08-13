#!/usr/local/bin/python3.5
import subprocess
import os

spiderNames = ["XNXQ", "Course", "Title", "Class", "ParamsFourth", "FifthParam"]

while (True):
    for name in spiderNames:
        command = "scrapy crawl " + name
        subprocess.call(command, shell=True)

    path = '/home/fusae/PycharmProjects/dgut_spider/script'
    if os.path.exists(path):
        files = os.listdir(path)
        for each in files:
            if each != 'params_script.py':
                command = "python3 " + each
                subprocess.call(command, shell=True)

