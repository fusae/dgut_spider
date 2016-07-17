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
    XNXQ = scrapy.Field() # ѧ��ѧ��
    college = scrapy.Field() # �е���λ
    name = scrapy.Field() # �γ�
    hours = scrapy.Field() # ��ѧʱ
    credit = scrapy.Field() # ��ѧ��
    teacher = scrapy.Field() # ��ʦ
    classTime = scrapy.Field() # �Ͽ�ʱ��
    location = scrapy.Field() # �Ͽεص�
    className = scrapy.Field() # �Ͽΰ༶
    stuNum = scrapy.Field() # �Ͽ�����


# -----------------------second-----------------

# professor title 
class TitleItem(scrapy.Item):
    text = scrapy.Field()
    num = scrapy.Field()

# detail professor title 
class DetailProfItem(scrapy.Item):
    XNXQ = scrapy.Field() # ѧ��ѧ��
    department = scrapy.Field() # ����
    teacher = scrapy.Field() # ��ʦ
    gender = scrapy.Field() # �Ա�
    title = scrapy.Field() # ְ��
    note1 = scrapy.Field() # ע1
    note2 = scrapy.Field() # ע2

# detail professor course message
class DetailProfCourseItem(scrapy.Item):
    snum = scrapy.Field() # serial number
    course = scrapy.Field() # �γ�
    credit = scrapy.Field() # ѧ��
    teachWay = scrapy.Field() # �ڿη�ʽ
    courseType = scrapy.Field() # �γ����
    classNum = scrapy.Field() # �Ͽΰ��
    className = scrapy.Field() # �Ͽΰ༶
    stuNum = scrapy.Field() # �Ͽ�����
    week = scrapy.Field() # �ܴ�
    section = scrapy.Field() # �ڴ�
    location = scrapy.Field() # �ص�
