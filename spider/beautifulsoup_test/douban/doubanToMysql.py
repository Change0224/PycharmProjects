import requests
import pymysql
from bs4 import BeautifulSoup


def parse_result(html,db,cursor):

    soup = BeautifulSoup(html,features='html.parser')
    """
    html 表示被解析的html格式的内容
    html.parser表示解析用的解析器
    """
    list = soup.find(class_='grid_view').find_all('li')

    for item in list:

        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        # item_index = item.find(class_='').string
        item_index = item.find('em').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        if(item.find(class_='inq')!=None):
            item_intr = item.find(class_='inq').string

        print('爬取电影：' + item_index + ' | ' + item_name  +' | ' + item_score  +' | ' + item_intr )

        sql = "insert into movies (id,name,score,intr) values (%s,'%s',%s,'%s')" %(item_index,item_name,item_score,pymysql.escape_string(item_intr))

        # db.ping(reconnect=True)
        # cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

def request_douban(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    response = requests.get(url,headers=header)
    if response.status_code == 200:
        html = response.text
        return html
    else:
        print("获取网页失败")



if __name__ == '__main__':
    '''
    创建mysql连接
    '''
    #打开数据库连接，参数1:主机或IP；参数2:数据库账户名；参数3:数据库密码；参数4:数据库库名
    db = pymysql.connect('127.0.0.1','root','Change0224','myPython')
    #使用cursor()方法创建游标
    cursor = db.cursor()
    sql = "drop table if exists movies"
    #使用exectute()方法执行sql查询
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

    for page in range(0,10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25)
        html = request_douban(url)
        parse_result(html,db,cursor)

    cursor.close()
    db.close()

