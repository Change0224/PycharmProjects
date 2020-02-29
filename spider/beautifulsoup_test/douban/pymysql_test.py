
import pymysql

#第一步:创建mysql连接
from pymysql import ProgrammingError

db = pymysql.connect('127.0.0.1','root','Change0224','myPython')
#第二步:使用cursor()方法创建一个游标对象
cursor = db.cursor()
sql = "drop table if exists movies"
#第三步：使用execute()执行语句
cursor.execute(sql)
sql = '''
        create table movies (
        id int(8) not null auto_increment,
        name  varchar(50) not null,
        score float not null,
        intr varchar(50) not null,
        PRIMARY key (id)) engine = InnoDB
    '''
cursor.execute(sql)


data = [(1,'肖申克的救赎',9.7,'希望让人自由。'),
        (2,'霸王别姬',9.6,'风华绝代。'),
        (3,'喜剧之王',8.7,'我是一个演员。'),
        (4,'告白',8.7,'没有一人完全善，也没有一人完全恶。'),
        (5,'超能陆战队',8.7,'Balalala~~~'),
        (6,'神偷奶爸',8.6,'Mr. I Don\'t Care其实也有Care的时候。')]


sql = 'insert into movies (id,name,score,intr) values (%s,%s,%s,%s)'

try:
    # 批量插入多条语句
    cursor.executemany(sql,data)
    #第四步：提交数据
    db.commit()
except  ProgrammingError as error:
    #发生错误时回滚
    print("开始回滚")
    print(error)
    db.rollback()
#第五步：关闭游标,关闭连接
cursor.close()
db.close()