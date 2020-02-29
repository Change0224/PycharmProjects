from  peewee import *

#注意端口号port
db = MySQLDatabase('myPython',host='localhost',port=3306,user='root',password='Change0224')

class BaseModel(Model):

    class Meta():
        database = db


class Topic(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(default="")
    topic_url = CharField(default="")
    content = TextField(default="")
    flag = CharField(default="")
    score = IntegerField(default=0)
    author_id = CharField(default="")
    publish_time = DateTimeField()
    reply_num = IntegerField(default=0)
    checked_num = IntegerField(default=0)
    last_pub_author = CharField(default="")
    last_pub_time = DateTimeField()
    jtl = FloatField(default=0)  #结帖率
    praised_num = IntegerField(default=0) #点赞量




