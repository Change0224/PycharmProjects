from datetime import date

from  peewee import *

db = MySQLDatabase('myPython',host='localhost',port=3306,user='root',password='Change0224')


#表继承于Model
#所有字段默认不为空；若没有设置主键，则默认添加字段id作为主键
class Message(Model):
    context = TextField()
    read_count = IntegerField(default=3)

    class Meta:
        database = db


if __name__ == '__main__':
    #创建表
    db.create_tables([Message])
    message = Message()
    message.context="1314521"
    message.save()
    pass



