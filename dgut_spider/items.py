# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# -----------------------first-----------------

# Course data
class CourseItem(scrapy.Item):
    value = scrapy.Field()
    text = scrapy.Field()
    courseNum = scrapy.Field()
    XNXQ = scrapy.Field()

# year semester
class XNXQItem(scrapy.Item):
    text = scrapy.Field()
    num = scrapy.Field()

# detail course data
class DetailItem(scrapy.Item):
    XNXQ = scrapy.Field() # 学年学期
    college = scrapy.Field() # 承担单位
    name = scrapy.Field() # 课程
    hours = scrapy.Field() # 总学时
    credit = scrapy.Field() # 总学分
    teacher = scrapy.Field() # 教师
    classTime = scrapy.Field() # 上课时间
    location = scrapy.Field() # 上课地点
    className = scrapy.Field() # 上课班级
    stuNum = scrapy.Field() # 上课人数


# -----------------------second-----------------

# professor title 
class TitleItem(scrapy.Item):
    text = scrapy.Field()
    num = scrapy.Field()
