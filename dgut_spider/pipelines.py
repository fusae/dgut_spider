# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pymysql.cursors

fileName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data'

class CustomPipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        

    def process_item(self, item, spider):
        if spider.name == 'XNXQ':
            self.file = open('XNXQ.json', 'a') # 注意多次运行，会追加相同的内容
            line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
            self.file.write(line)
            return item

        if spider.name == 'Course':
            self.file = open('Course.json', 'a')
            line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
            self.file.write(line)
            return item

        if spider.name == 'XNXQCourse':
            # Connect to the database
            connection = pymysql.connect(host='localhost',
                                         user='dgut_admin',
                                         password='admindgut+1s',
                                         db='DGUT',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO course (XNXQ, \
                                               college, \
                                               name, \
                                               hours, \
                                               credit, \
                                               teacher, \
                                               classTime, \
                                               location, \
                                               className, \
                                               stuNum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (item['XNXQ'],
                                         item['college'],
                                         item['name'],
                                         item['hours'],
                                         item['credit'],
                                         item['teacher'],
                                         item['classTime'],
                                         item['location'],
                                         item['className'],
                                         item['stuNum']))

                    connection.commit()

            finally:
                connection.close()

            return item


        if spider.name == 'Title':
            # write to a file
            self.file = open('Title.json', 'a')
            line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
            self.file.write(line)
            return item


