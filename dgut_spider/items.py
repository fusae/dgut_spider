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
    XNXQ = scrapy.Field() # ѧ��ѧ��
    teacher = scrapy.Field() # ��ʦ
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

# the third item which contain first and second item
class containItem(scrapy.Item):
    first = scrapy.Field() # for fist table
    second = scrapy.Field() # for second table

# -----------------------third-----------------
# name and its' code
class ClassItem(scrapy.Item):
    text = scrapy.Field()
    num = scrapy.Field()


# -----------------------fourth-----------------
# campus, teaching building and classroom
class ClassroomItem(scrapy.Item):
    XQ = scrapy.Field()     # У��
    JXL = scrapy.Field()    # ��ѧ¥
    room = scrapy.Field()   # ����

# some attributes of room
class RoomItem(scrapy.Item):
    XNXQ = scrapy.Field()       # ѧ��ѧ��
    campus = scrapy.Field()     # У��
    building = scrapy.Field()   # ��ѧ¥
    classroom = scrapy.Field()  # ����
    note1 = scrapy.Field()      # ע1

# some course message of this room
class RoomCourseMessageItem(scrapy.Item):
    snum = scrapy.Field()       # ���кţ��ڲ������ݿ�ʱ��ʶ���������
    classroom = scrapy.Field()  # ����
    courseName = scrapy.Field() # �γ�
    teacher = scrapy.Field()    # ��ʦ
    classTime = scrapy.Field()  # �Ͽ�ʱ��
    num = scrapy.Field()        # �Ͽ�����

# the third item which contain first and second item
class containItem(scrapy.Item):
    first = scrapy.Field() # for fist table
    second = scrapy.Field() # for second table


# -----------------------fifth-----------------

# parameters to post
class FifthParamItem(scrapy.Item):
    value = scrapy.Field()
    text = scrapy.Field()

# detail message about the free choice course
class FreeChoiceItem(scrapy.Item):
    XNXQ = scrapy.Field() # ѧ��ѧ��
    campus = scrapy.Field() # campus
    snum = scrapy.Field() # serial number
    course = scrapy.Field() # the name of course
    credit = scrapy.Field() # the credit
    teacher = scrapy.Field() # teacher
    title = scrapy.Field() # title
    classNum = scrapy.Field() # class num
    stuNum = scrapy.Field() # the number of students
    week = scrapy.Field() # how many weeks does the course spend
    classTime = scrapy.Field() # class time
    location = scrapy.Field() # the locaton where have class

