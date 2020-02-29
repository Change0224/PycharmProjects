import json

import requests
from scrapy import Selector

from jd_spider.models import Good

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'Referer': 'https://item.jd.com/4622537.html'
}

#商品价格
#print(requests.get('https://p.3.cn/prices/mgets?&skuIds=J_4622537').text)
#评价总数
#print(requests.get('https://club.jd.com/comment/productCommentSummaries.action?referenceIds=4819554').text)
#
# url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1907&productId=4819554&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
# print(requests.get(url,headers=headers).text)

def parse_good(good_id):

    good = Good()

    url = 'https://item.jd.com/{}.html'.format(good_id)
    html = requests.get(url).text
    sel = Selector(text = html)
    #获取商品名称
    name_css = 'div.sku-name::text'
    if len(sel.css(name_css).extract()) == 2:
        good.name = sel.css(name_css).extract()[1].strip()

    #获取发货方
    supplier_css = '#summary-service > span'
    tmp = sel.css(supplier_css).extract()
    if sel.css(supplier_css).extract():
        good.supplier = sel.css(supplier_css).extract()

    #规格与包装
    ggbz_css = 'div.Ptable::text'
    if sel.css(ggbz_css).extract():
        good.ggbz = sel.css(ggbz_css).extract()
    ggbz_css = 'div.package-list::text'
    if sel.css(ggbz_css).extract():
        good.ggbz.append(sel.css(ggbz_css).extract())

    pass

    #获取商品价格
    url = 'https://p.3.cn/prices/mgets?&skuIds=J_{}'.format(good_id)
    price_text = requests.get(url,headers=headers).text.strip()
    price_list = json.loads(price_text)
    if price_list:
        price = float(price_list[0]['p'])
    print(price)

if __name__ == '__main__':
    parse_good('4622537')