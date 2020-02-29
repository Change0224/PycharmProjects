from datetime import date

from  peewee import *


#注意端口号port
db = MySQLDatabase('myPython',host='localhost',port=3306,user='root',password='Change0224')


#表继承于Model
#所有字段默认不为空；若没有设置主键，则默认添加字段id作为主键
class Person(Model):
    name = CharField()
    birthday = DateField()
    praised_num = IntegerField(default=0)

    class Meta:
        database = db
        table_name = 'person'

if __name__ == '__main__':
#创建表
    # if db.table_exists('person'):
    #     print("该表存在")
    #     db.drop_tables([Person])
    #     db.create_tables([Person])
    # else:
    #     db.create_tables([Person])

#添加数据
    # bob = Person(name='bob',birthday=date(2020,12,23))
    # bob.save()
    # mary = Person(name='mary',birthday=date(2012,12,12))
    # mary.save()


#查询数据
    #注意：1、where语句中字段需写为 类名.字段  eg:Person.name
    #     2、where语句中等值判断为== 并非=

    #查询数据（只获取一条）,且当get()方法取不到数据的时候会报错，需要配合使用try except
    #方法一：select().get()
    bob = Person.select().where(Person.name=='bob').get()
    print(bob)
    #方法二：Model.get()
    bob = Person.get(Person.name=='bob')
    print(bob)

    #查询结果会有多条的方法：
    #query是一个ModelSelect对象，可以当作list操作（实际上不是list)
    #query可以当作list操作的原因是，实现了getitem
    #因此可以写作query = Person.select().where(Person.name=='mary')[1:2] 带范围的指向，而非指定下标。切片式
    query = Person.select().where(Person.name=='mary')[1:]
    for person in query:
        print(person.name,person.birthday)

#修改数据
    tom = Person()
    tom.birthday = date(2021,12,12)
    tom.name = 'tom'
    tom.save()
    print("save保存"+str(bob.save())) #save()方法在没有数据的时候新增数据，存在的时候修改数据
    pass

#删除数据
    #1、根据id删除某行
    Person.delete_by_id(7)
    Person.delete_by_id(8)
    Person.delete_by_id(5)
    #2、根据某条件删除数据
    # bob = Person.select().where(Person.name=='bob').get()
    # #方法一：
    # bob.delete_instance()
    # #方法二：
    # Person.delete_instance(bob)


