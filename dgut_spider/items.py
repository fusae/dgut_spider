# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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

