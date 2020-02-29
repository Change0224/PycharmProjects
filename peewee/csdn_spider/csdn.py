from datetime import datetime


import requests
from scrapy import Selector

from csdn_spider.models import Topic


def request_html(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    response = requests.get(url)
    if response.status_code == 200 :
        html = response.text
    else:
        print("爬取网页失败")

    return html

def parse_result(html):
    sel = Selector(text = html)

    tr_css = 'div.forums_table_c > table > tbody > tr'
    tr = sel.css(tr_css)
    for num in range(1,len(tr)+1):
        tmp = Topic()
        #是否结帖
        flag_css=tr_css+':nth-child(%s) > td.forums_topic_flag > span::text'%(num)
        if sel.css(flag_css).extract():
            flag = sel.css(flag_css).extract()[0]
            tmp.flag = flag
            #print("状态:"+topic.flag)
        #悬赏分数
        score_css = tr_css+':nth-child(%s) > td.forums_score > em::text'%(num)
        if sel.css(score_css).extract():
            score = int(sel.css(score_css).extract()[0])
            tmp.score = score
            #print("分数："+str(topic.score))
        #主题
        title_css = tr_css+':nth-child(%s) > td.forums_topic > a.forums_title'%(num)
        if sel.css(title_css+"::text").extract():
            title = sel.css(title_css+"::text").extract()[0]
            tmp.title = title
            #print("主题："+topic.title)
        if sel.css(title_css+"::attr(href)").extract():
            topic_url = sel.css(title_css+"::attr(href)").extract()[0]
            tmp.topic_url = topic_url
            tmp.id = (int)(topic_url.split("/")[-1])
            #print("id："+str(topic.id))
        #提问者
        author_id_css = tr_css+':nth-child(%s) > td.forums_author > a::attr(href)'%(num)
        if sel.css(author_id_css).extract():
            author_url = sel.css(author_id_css).extract()[0]
            tmp.author = author_url.split("/")[-1]
            #print("author："+topic.author)
        #提问时间
        publish_time_css = tr_css+':nth-child(%s) > td.forums_author > em::text'%(num)
        if sel.css(publish_time_css).extract():
            publish_time = sel.css(publish_time_css).extract()[0]
            publish_time = datetime.strptime(publish_time,"%Y-%m-%d %H:%M")
            tmp.publish_time = publish_time
            #print("publish_time："+str(topic.publish_time))
        reply_css = tr_css+':nth-child(%s) > td.forums_reply > span::text'%(num)
        if sel.css(reply_css).extract():
            reply_tmp = sel.css(reply_css).extract()
            #回复数量
            reply_num = int(reply_tmp[0].split('/')[0])
            tmp.reply_num = reply_num
            #print("reply_num："+str(reply_num))
            #点击量
            checked_num = int(reply_tmp[0].split('/')[1])
            tmp.checked_num = checked_num
            #print("checked_num："+str(checked_num))
        #最后回复者
        last_pub_author_css = tr_css+':nth-child(%s) > td.forums_last_pub > a::text'%(num)
        if sel.css(last_pub_author_css).extract():
            last_pub_author=sel.css(last_pub_author_css).extract()[0]
            tmp.last_pub_author = last_pub_author
            #print("last_pub_author："+topic.last_pub_author)
        #最后回复时间
        last_pub_time_css=tr_css+':nth-child(%s) > td.forums_last_pub > em::text'%(num)
        if sel.css(last_pub_time_css).extract:
            last_pub_time=sel.css(last_pub_time_css).extract()[0]
            last_pub_time = datetime.strptime(last_pub_time,"%Y-%m-%d %H:%M")
            tmp.last_pub_time = last_pub_time
            #print("last_pub_time："+str(topic.last_pub_time))

        print(tmp.save())



if __name__ == '__main__':
    html = request_html('https://bbs.csdn.net/forums/ios')
    parse_result(html)