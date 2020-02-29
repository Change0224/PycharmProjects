from  peewee import *

#注意端口号port
db = MySQLDatabase('myPython',host='localhost',port=3306,user='root',password='Change0224')

class BaseModel(Model):

    class Meta():
        database = db


class Topic(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField()
    topic_url = CharField()
    content = TextField(default="")
    flag = CharField()
    score = IntegerField()
    author = CharField()
    publish_time = DateTimeField()
    reply_num = IntegerField()
    checked_num = IntegerField()
    last_pub_author = CharField()
    last_pub_time = DateTimeField()
    jtl = FloatField(default=0)  #结帖率
    praised_num = IntegerField(default=0) #点赞量

class Answer(BaseModel):
    topic_id = IntegerField()
    author = CharField()
    content = TextField("")
    create_time = DateTimeField()
    praised_num = IntegerField(default=0) #点赞量

if __name__ == '__main__':
    db.drop_tables([Topic,Answer])
    db.create_tables([Topic,Answer])




