import requests
import xlwt
from  scrapy import  Selector

# 创建一个Workbook对象，这就相当于创建了一个Excel文件
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
'''
Workbook类初始化时有encoding和style_compression参数
encoding:设置字符编码，一般要这样设置：w = Workbook(encoding='utf-8')，就可以在excel中输出中文了。
默认是ascii。当然要记得在文件头部添加：
#!/usr/bin/env python
# -*- coding: utf-8 -*-
style_compression:表示是否压缩，不常用。
'''

#创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格。
# 在电脑桌面右键新建一个Excel文件，其中就包含sheet1，sheet2，sheet3三张表
sheet = book.add_sheet('豆瓣电影Top250ByXPATH', cell_overwrite_ok=True)
# 其中的test是这张表的名字,cell_overwrite_ok，表示是否可以覆盖单元格，其实是Worksheet实例化的一个参数，默认值是False

# 向表test中添加数据
sheet.write(0,0,'名称')   # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
sheet.write(0,1,'图片')
sheet.write(0,2,'排名')
sheet.write(0,3,'评分')
sheet.write(0,4,'作者')
sheet.write(0,5,'简介')

n = 1

def parse_result(html):
    sel = Selector(text = html)
    name_xpath = "//*[@id='content']//*[@class='grid_view']/li//span[@class='title'][1]/text()"
    name = sel.xpath(name_xpath).extract()
    pic_xpath = "//*[@id='content']/div/div[1]/ol//li/div/div[1]/a/img/@src"
    pic = sel.xpath(pic_xpath).extract()
    print(pic)
    id_xpath="//*[@id='content']/div/div[1]/ol//li/div/div[1]/em[1]/text()"
    id = sel.xpath(id_xpath).extract()
    score_xpath ="//*[@id='content']/div/div[1]/ol//li/div/div[2]/div[2]/div/span[@class='rating_num']/text()"
    score = sel.xpath(score_xpath).extract()
    author_xpath = "//*[@id='content']/div/div[1]/ol//li/div/div[2]/div[2]/p[1]/text()"
    author = sel.xpath(author_xpath).extract()
    intr_xpath = "//*[@id='content']/div/div[1]/ol//li/div/div[2]/div[2]/p[2]/span/text()"
    intr = sel.xpath(intr_xpath).extract()

    global n
    i = 0
    for tmp in name:
        sheet.write(n,0,name[i])   # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
        sheet.write(n,1,pic[i])
        sheet.write(n,2,id[i])
        sheet.write(n,3,score[i])
        sheet.write(n,4,author[i])
        sheet.write(n,5,intr[i])
        print('爬取电影：' + id[i] + ' | ' + name[i]  +' | ' + score[i]  +' | ' + intr[i] )

        n = n + 1
        i = i + 1

    book.save('豆瓣电影Top250ByXPATH.xls')



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


def main(page):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25)
    html = request_douban(url)
    parse_result(html)

if __name__ == '__main__':
    for page in range(0,10):

        main(page)
