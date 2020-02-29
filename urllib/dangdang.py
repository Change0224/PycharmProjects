import requests
import re
import json
def request_dandan(url):
    header = {
        "User-Agent" :  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:72.0) Gecko/20100101 Firefox/72.0"
    }

    response = requests.get(url,headers = header)

    if response.status_code == 200 :
        return response.text

def parse_result(html):
    #pattern = r'.*?list_num.*?(\d+).</div>.*?pic.*?<img src="(.*?)"'
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
     # pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)".*?class="tuijian">(.*?)<.*?class="publisher_info".*?target="_blank">(.*?)<',re.S)
    results = re.findall(pattern,html)
    return results



def write_item_to_file(item):
    print('开始写入数据 ====> ' + str(item))
    with open('book.txt', 'a', encoding='UTF-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()


def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dandan(url)
    items = parse_result(html) # 解析过滤我们想要的信息

    for item in items:
        write_item_to_file(item)

if __name__ == '__main__':
    for i in range(1,26):
        main(i)