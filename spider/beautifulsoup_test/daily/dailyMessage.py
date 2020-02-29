import json
import time
from datetime import datetime

import requests
from scrapy import Selector
from twilio.rest import Client  # 需要装twilio库

# 爬取爱词霸每日鸡汤
def get_iciba_everyday_chicken_soup():
    date = datetime.now().strftime("%Y-%m-%d")
    url = 'http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title={}'.format(date)
    re = requests.get(url)
    html_dict = json.loads(re.text)
    English = html_dict['content']
    Chinese = html_dict['note']
   # everyday_soup = English +"\n" +Chinese
    everyday_soup = Chinese
    return everyday_soup

def get_tianqi_everyday(city):
    url = 'https://www.tianqi.com/{}/'.format(city)
    headers = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    }
    re = requests.get(url,headers = headers)
    sel = Selector(text=re.text)
    week = sel.css('dd.week::text').extract()[0]+'\n'
    weather_tmp = (sel.xpath("//p[@class='now']/b/text()").extract()[0])+'℃\n'
    shidu_tmp = sel.xpath('//dd[@class="shidu"]/b/text()').extract()
    shidu = '\t'.join(shidu_tmp)
    weather = week + weather_tmp + shidu
    return  weather

def send_message(everyday_soup):
    # 获取当前时间并格式化显示方式：
    send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    account_sid = 'ACbabfd4dbd9cebbd88070e15f3a0b5f5e'  # api参数 复制粘贴过来
    auth_token = '15e34bd59bb16ef28c8c4ec2dd441db4'   # api参数 复制粘贴过来
    client = Client(account_sid, auth_token)  # 账户认证
    message = client.messages.create(
        to="+8618611732698",  # 接受短信的手机号 注意写中国区号 +86
        from_="+12056712441",  # api参数 Number(领取的虚拟号码
        body="\n王者荣耀\n"+everyday_soup)  #自定义短信内容
    print('接收短信号码：'+message.to)
    # 打印发送时间和发送状态：
    print('发送时间：%s \n状态：发送成功！' % send_time)
    print('短信内容：\n'+message.body)  # 打印短信内容
    print('短信SID：' + message.sid)  # 打印SID


if __name__ == '__main__':
    everyday_soup = get_iciba_everyday_chicken_soup()
    weather = get_tianqi_everyday('beijing')
    send_message("上星星么？")
