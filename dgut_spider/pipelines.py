# -*- coding: gbk -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pymysql.cursors

fileName = '/home/fusae/PycharmProjects/dgut_spider/dgut_spider/Data'

# To get XNXQ
class XNXQPipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'XNXQ.json'

    def open_spider(self, spider):
        # if XNXQ.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

# First table
# To get courses
class CoursePipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'Course.json'

    def open_spider(self, spider):
        # if course.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


# First table
# to get detail courses, store into databse
class CustomPipeline(object):

    def process_item(self, item, spider):
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


# Second table
# To get title
class TitlePipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'Title.json'

    def open_spider(self, spider):
        # if Title.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

# Second table
# To get detail staff and courses of staff, store into database
class TeacherCoursePipeline(object):
    def __init__(self):
        self.connection = None
    def open_spider(self, spider):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                     user='dgut_admin',
                                     password='admindgut+1s',
                                     db='DGUT',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
#        print(item)
        try:
            with self.connection.cursor() as cursor:
                #Create a new record
                sql1 = "INSERT INTO staff (XNXQ, \
                                          department, \
                                          teacher, \
                                          gender, \
                                          title, \
                                          note1, \
                                          note2) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                # Teacher only insert once
                if item['second']['snum'] == '1':
                    cursor.execute(sql1, (item['first']['XNXQ'],
                                         item['first']['department'],
                                         item['first']['teacher'],
                                         item['first']['gender'],
                                         item['first']['title'],
                                         item['first']['note1'],
                                         item['first']['note2']))
                    self.connection.commit()

                #Create a new record
                cursor.execute("select max(id) from staff")
                teacherId = cursor.fetchone()['max(id)']
                    
                sql2 = "INSERT INTO staffCourse (teacherId, \
                                                 snum, \
                                                 course, \
                                                 credit, \
                                                 teachWay, \
                                                 courseType, \
                                                 classNum, \
                                                 className, \
                                                 stuNum, \
                                                 week, \
                                                 section, \
                                                 location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql2, (teacherId,
                                      item['second']['snum'],
                                      item['second']['course'],
                                      item['second']['credit'],
                                      item['second']['teachWay'],
                                      item['second']['courseType'],
                                      item['second']['classNum'],
                                      item['second']['className'],
                                      item['second']['stuNum'],
                                      item['second']['week'],
                                      item['second']['section'],
                                      item['second']['location']))
                self.connection.commit()

        except Exception as e:
            print('------------------------------------------')
            print(e)
        return item

    def close_spider(self, spider):
        self.connection.close()


# Third table
# To get class
class ClassPipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'Class.json'

    def open_spider(self, spider):
        # if Class.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


# Fourth table
# To get all parameters
class ParamsFourthPipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'ParamsFourth.json'

    def open_spider(self, spider):
        # if Class.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


# Fourth table
# To get all rooms and courses in every room, then store into database
class ClassroomPipeline(object):
    def __init__(self):
        self.connection = None
    def open_spider(self, spider):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                     user='dgut_admin',
                                     password='admindgut+1s',
                                     db='DGUT',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
#        print(item)
        try:
            with self.connection.cursor() as cursor:
                #Create a new record
                sql1 = "INSERT INTO room (XNXQ, \
                                          campus, \
                                          building, \
                                          classroom, \
                                          note1) VALUES (%s, %s, %s, %s, %s)"
                # classroom only insert once
                if item['second']['snum'] == '1':
                    cursor.execute(sql1, (item['first']['XNXQ'],
                                         item['first']['campus'],
                                         item['first']['building'],
                                         item['first']['classroom'],
                                         item['first']['note1']))
                    self.connection.commit()

                #Create a new record
                cursor.execute("select max(id) from room")
                roomId = cursor.fetchone()['max(id)']
                    
                sql2 = "INSERT INTO roomCourse (roomId, \
                                                 courseName, \
                                                 teacher, \
                                                 classTime, \
                                                 num) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql2, (roomId,
                                      item['second']['courseName'],
                                      item['second']['teacher'],
                                      item['second']['classTime'],
                                      item['second']['num']))
                self.connection.commit()

        except Exception as e:
            print('------------------------------------------')
            print(e)
        return item

    def close_spider(self, spider):
        self.connection.close()


# Fifth table
# To get parameter
class FifthParamPipeline(object):
    def __init__(self):
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        os.chdir(fileName)
        self.jsonFile = 'FifthParam.json'

    def open_spider(self, spider):
        # if FifthParam.json file exists, then remove it 
        if os.path.exists(self.jsonFile):
            os.remove(self.jsonFile)
        self.file = open(self.jsonFile, 'a')
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n' # 避免中文输出成unicode
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


# Fifth table
# To get all the free choice courses, then store into database
class FreeChoicePipeline(object):
    def __init__(self):
        self.connection = None
    def open_spider(self, spider):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                     user='dgut_admin',
                                     password='admindgut+1s',
                                     db='DGUT',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
#        print(item)
        try:
            with self.connection.cursor() as cursor:
                #Create a new record
                sql1 = "INSERT INTO freeChoice (XNXQ, \
                                          campus, \
                                          snum, \
                                          course, \
                                          credit, \
                                          teacher, \
                                          title, \
                                          classNum, \
                                          stuNum, \
                                          week, \
                                          classTime, \
                                          location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor.execute(sql1, (item['XNXQ'],
                                      item['campus'],
                                      int(item['snum']),
                                      item['course'],
                                      item['credit'],
                                      item['teacher'],
                                      item['title'],
                                      item['classNum'],
                                      item['stuNum'],
                                      item['week'],
                                      item['classTime'],
                                      item['location']))
                self.connection.commit()


        except Exception as e:
            print('------------------------------------------')
            print(e)
        return item

    def close_spider(self, spider):
        self.connection.close()
