
import re
from datetime import datetime
from urllib import parse

import requests
from scrapy import Selector

from csdn_spider.models import Topic, Answer

domin = "https://bbs.csdn.net"
url_list = []



def parse_answer(url):
    # 补充topic表中的内容
    topic = Topic()
    existed_topic = Topic.select().where(Topic.topic_url == url)
    if existed_topic:
        topic = existed_topic[0]

        html = requests.get(url).text
        sel = Selector(text=html)
        content_css = 'div.mod_topic_wrap.post.topic > dl > dd > div.post_body.post_body_min_h'
        content = sel.css(content_css).extract()[0]
        topic.content = content.strip()
        # print(content)
        jtl_css = 'div.mod_topic_wrap.post.topic > dl > dt > div.close_topic::text'
        jtl = 0
        if sel.css(jtl_css).extract():
            jtl = sel.css(jtl_css).extract()[0]
            if re.search("(\d+)%", jtl):
                topic.jtl = float(re.search("(\d+)%", jtl).group(1))
            # print(jtl)
        praised_num_css = 'div.mod_topic_wrap.post.topic> dl > dd > div > div > label > em::text'
        if sel.css(praised_num_css).extract():
            praised_num = sel.css(praised_num_css).extract()[0]
            praised_num = int(praised_num)
            topic.praised_num = praised_num
            # print(praised_num)
        topic.save()
    html = requests.get(url).text
    sel = Selector(text=html)
    all_divs_css = 'div.mod_topic_wrap.post:not(.topic)'
    if sel.css(all_divs_css).extract():
        all_divs = sel.css(all_divs_css)
        for answer_item in all_divs:
            answer = Answer()
            if '?' in url:
                answer.topic_id = (int)(url.split('/')[-1].split('?')[0])
            else:
                answer.topic_id = (int)(url.split("/")[-1])
            author_css = all_divs_css+' div.nick_name a::text'
            if answer_item.css(author_css).extract():
                answer.author = answer_item.css(author_css).extract()[0]
            content_css = 'div.mod_topic_wrap.post:not(.topic) > dl > dd > div.post_body.post_body_min_h'
            if answer_item.css(content_css).extract():
                content = (sel.css(content_css).extract()[0]).strip()
                answer.content = content
            create_time_css = 'div.mod_topic_wrap.post:not(.topic) > dl > dd > div  label.date_time::text'
            if answer_item.css(create_time_css).extract():
                create_time = answer_item.css(create_time_css).extract()[0]
                answer.create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
            praised_num_css = 'div.mod_topic_wrap.post:not(.topic) > dl > dd > div  label > em::text'
            if answer_item.css(praised_num_css).extract():
                answer.praised_num = int(answer_item.css(praised_num_css).extract()[0])
            answer.save()

        next_page_css = '#bbs_title_bar > div  a.pageliststy.next_page::attr(href)'
        if sel.css(next_page_css).extract():
            length = len(sel.css(next_page_css).extract())
            next_url = sel.css(next_page_css).extract()[-1]
            next_url = parse.urljoin(domin, next_url)
            #print("next_url"+next_url)
            if '?' in url and length == 1:
                pass
            else:
                parse_answer(next_url)

def parse_result(url):
    html = requests.get(url).text
    sel = Selector(text = html)

    tr_css = 'div.forums_table_c > table > tbody > tr'
    tr = sel.css(tr_css)
    for num in range(1,len(tr)+1):
        topic = Topic()
        #是否结帖
        flag_css=tr_css+':nth-child(%s) > td.forums_topic_flag > span::text'%(num)
        if sel.css(flag_css).extract():
            flag = sel.css(flag_css).extract()[0]
            topic.flag = flag
            #print("状态:"+topic.flag)
        #悬赏分数
        score_css = tr_css+':nth-child(%s) > td.forums_score > em::text'%(num)
        if sel.css(score_css).extract():
            score = int(sel.css(score_css).extract()[0])
            topic.score = score
            #print("分数："+str(topic.score))
        #主题
        title_css = tr_css+':nth-child(%s) > td.forums_topic > a.forums_title'%(num)
        if sel.css(title_css+"::text").extract():
            title = sel.css(title_css+"::text").extract()[0]
            topic.title = title
            #print("主题："+topic.title)
        if sel.css(title_css+"::attr(href)").extract():
            topic_url = sel.css(title_css+"::attr(href)").extract()[0]
            topic_url = parse.urljoin(domin,topic_url)
            topic.topic_url = topic_url
            topic.id = (int)(topic_url.split("/")[-1])
            #print("id："+str(topic.id))
        #提问者
        author_css = tr_css+':nth-child(%s) > td.forums_author > a'%(num)
        if sel.css(author_css).extract():
            author_url = sel.css(author_css+"::attr(href)").extract()[0]
            author_url = parse.urljoin(domin,author_url)
            topic.author = author_url.split("/")[-1]
            #print("author："+topic.author)
        #提问时间
        publish_time_css = tr_css+':nth-child(%s) > td.forums_author > em::text'%(num)
        if sel.css(publish_time_css).extract():
            publish_time = sel.css(publish_time_css).extract()[0]
            publish_time = datetime.strptime(publish_time,"%Y-%m-%d %H:%M")
            topic.publish_time = publish_time
            #print("publish_time："+str(topic.publish_time))
        reply_css = tr_css+':nth-child(%s) > td.forums_reply > span::text'%(num)
        if sel.css(reply_css).extract():
            reply_tmp = sel.css(reply_css).extract()
            #回复数量
            reply_num = int(reply_tmp[0].split('/')[0])
            topic.reply_num = reply_num
            #print("reply_num："+str(reply_num))
            #点击量
            checked_num = int(reply_tmp[0].split('/')[1])
            topic.checked_num = checked_num
            #print("checked_num："+str(checked_num))
        #最后回复者
        last_pub_author_css = tr_css+':nth-child(%s) > td.forums_last_pub > a::text'%(num)
        if sel.css(last_pub_author_css).extract():
            last_pub_author=sel.css(last_pub_author_css).extract()[0]
            topic.last_pub_author = last_pub_author
            #print("last_pub_author："+topic.last_pub_author)
        #最后回复时间
        last_pub_time_css=tr_css+':nth-child(%s) > td.forums_last_pub > em::text'%(num)
        if sel.css(last_pub_time_css).extract():
            last_pub_time=sel.css(last_pub_time_css).extract()[0]
            last_pub_time = datetime.strptime(last_pub_time,"%Y-%m-%d %H:%M")
            topic.last_pub_time = last_pub_time
            #print("last_pub_time："+str(topic.last_pub_time))
        print(topic.title)
        existed_topic = Topic.select().where(Topic.id == topic.id)
        if existed_topic:
            topic.save()
        else:
            if topic.topic_url:
            # 如果topic存在，防止某个url中没有帖子
                topic.save(force_insert=True)
                parse_answer(topic_url)

    next_page_css = 'div.forums_table_c > table > thead > tr > td a.pageliststy.next_page::attr(href)'
    if sel.css(next_page_css).extract():
        length = len(sel.css(next_page_css).extract())
        next_url = sel.css(next_page_css).extract()[-1]
        next_url = parse.urljoin(domin,next_url)

        if '?' in url and length == 1:
            pass
        else:
            #print(next_url)
            parse_answer(next_url)




def get_nodes_json():
    url = 'https://bbs.csdn.net/dynamic_js/left_menu.js?csdn'
    left_menu_text = requests.get(url).text
    nodes_str_match = re.search('forumNodes:(.*])',left_menu_text)
    if nodes_str_match:
        nodes_str = nodes_str_match.group(1)
        #nodes_list = eval(nodes_str)  ##nodes_str 中含有null。python无法处理null这样的字符串，所以报错。
        #nodes_str 中含有null。python无法处理null这样的字符串，所以报错。
        #解决办法一：
        # nodes_list = json.loads(nodes_str)
        # print(type(nodes_list))
        #解决办法二：
        nodes_str = nodes_str.replace('null','None')
        nodes_list = eval(nodes_str)
        return nodes_list
    return []


def process_nodes_list(nodes_list):
    #将js的格式提取url到list中
    for item in nodes_list:
        if 'url' in item :
            if item['url']:
                url_list.append(item['url'])
            if 'children' in item:
                process_nodes_list(item['children'])


def get_level1_list(node_list):
    level1_url=[]
    for item in node_list:
        if  'url' in item and item['url']:
            level1_url.append(item['url'])
    return level1_url


def get_last_list():
    node_list = get_nodes_json()
    process_nodes_list(node_list)
    level1_url = get_level1_list(node_list)
    last_urls = []
    for url in url_list:
        if url not in level1_url:
            last_urls.append(parse.urljoin(domin,url))
            last_urls.append(parse.urljoin(domin,url+"/recommend"))
            last_urls.append(parse.urljoin(domin,url+"/closed"))

    return last_urls



if __name__ == '__main__':
    last_urls = get_last_list()

    for url in last_urls:
        parse_result(url)


