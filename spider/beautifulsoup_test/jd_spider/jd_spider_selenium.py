import json
import re
import time

from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from jd_spider.models import Good, GoodEvaluateSummary, GoodEvaluate


def parse_value(num_str):
    '''
    将字符串类型的数字转换成数字
    :param num_str:字符串类型的数字，可能包含"万"
    :return:成功返回数字，默认返回0
    '''
    nums = 0
    re_math = re.search("(\d+)",num_str)
    if re_math:
        nums = int(re_math.group(1))
        if "万" in num_str:
            nums *= 10000

    return nums



def parse_good(good_id):
    good = Good(id = good_id)
    browser = webdriver.Chrome()
    url = 'https://item.jd.com/{}.html'.format(good_id)
    browser.get(url)
    #获取执行过js后的html:browser.page_source
    sel = Selector(text=browser.page_source)
    name_css = '.sku-name::text'
    if sel.css(name_css).extract():
        good.name = ''.join(sel.css(name_css).extract()).strip()
    content_css = '#detail > div.tab-con'
    if sel.css(content_css).extract():
        good.content = sel.css(content_css).extract()
    if sel.xpath('//div[@id="summary-service"]/a/text()').extract():
        good.supplier = sel.xpath('//div[@id="summary-service"]/a/text()').extract()[0]
    else:
        if sel.xpath('//div[@id="summary-service"]/span/text()').extract():
            good.supplier = sel.xpath('//div[@id="summary-service"]/span/text()').extract()[0]

    image_list_xpath ="//div[@class='spec-list']//img/@src"
    if sel.xpath(image_list_xpath).extract():
        image_list =sel.xpath(image_list_xpath).extract()
        #json.dumps()用于将字典形式的数据转化为字符串，json.loads()用于将字符串形式的数据转化为字典
        good.image_list = json.dumps(image_list)
    price_xpath = "//span[@class='price J-p-{}']/text()".format(good_id)
    if sel.xpath(price_xpath).extract():
        good.price = float(sel.xpath(price_xpath).extract()[0])
    #点击规格与包装
    ggbz_xpath = "//li[contains(text(),'规格与包装')]"
    browser.find_element_by_xpath(ggbz_xpath).click()
    time.sleep(3)
    sel = Selector(text=browser.page_source)

    ggbz_css = '#detail > div.tab-con'
    if sel.css(ggbz_css).extract():
        good.ggbz = sel.css(ggbz_css).extract()


    #点击商品评价
    comment_xpath = "//li[contains(text(),'商品评价')]"
    browser.find_element_by_xpath(comment_xpath).click()
    time.sleep(3)
    sel = Selector(text=browser.page_source)

    good_rate_xpath = "//div[@class='percent-con']/text()"
    if sel.xpath(good_rate_xpath).extract():
        good.good_rate = int(sel.xpath(good_rate_xpath).extract()[0])

    summary_xpath = "//ul[@class='filter-list']//a"
    if sel.xpath(summary_xpath):
        summary_as = sel.xpath(summary_xpath)
        for summary in summary_as:
            name = summary.xpath('./text()').extract()[0]
            nums = summary.xpath('./em/text()').extract()[0]
            nums = parse_value(nums)

            if name == '全部评价':
                good.comments_nums = nums
            if name == '晒图':
                good.has_image_comment_nums = nums
            if name == '视频晒单':
                good.has_video_comment_nums = nums
            if name == '追评':
                good.has_add_comment_nums = nums
            if name == "好评":
                good.well_comment_nums = nums
            if name == '中评':
                good.middle_comment_nums = nums
            if name == '差评':
                good.bad_comment_nums = nums
    #保存商品信息
    existed_good = Good.select().where(Good.id == good.id)
    if existed_good:
        good.save()
    else:
        good.save(force_insert=True)
    #评价标签
    tag_list = sel.xpath("//div[@class='percent-info']//div//span/text()").extract()
    for tag in tag_list:
        re_match = re.match("(.*)\((\d+)\)",tag)
        tag_name = re_match.group(1)
        tag_num = int(re_match.group(2))
        #保存评价标签
        existed_summarys = GoodEvaluateSummary.select().where(GoodEvaluateSummary.good == good, GoodEvaluateSummary.tag == tag_name)
        if existed_summarys:
            goodEvaluateSummary = existed_summarys[0]
        else:
            goodEvaluateSummary = GoodEvaluateSummary(good = good)
        goodEvaluateSummary.tag = tag_name
        goodEvaluateSummary.num = tag_num
        goodEvaluateSummary.save()
    has_next_page = True
    while has_next_page:
        all_evaluates_xpath = '//div[@class="comment-item"]'
        all_evaluates = sel.xpath(all_evaluates_xpath)
        for comment in all_evaluates:
            evaluate = GoodEvaluate(good = good)
            evaluate.id = comment.xpath('./@data-guid').extract()[0]
            evaluate.user_head_url = comment.xpath(".//div[@class='user-info']/img/@src").extract()[0]
            evaluate.user_name = "".join(comment.xpath(".//div[@class='user-info']/text()").extract()).strip()
            buy_info =comment.xpath('.//div[@class="order-info"]//span/text()').extract()
            evaluate.get_info = "".join(buy_info[:-1])
            evaluate.evaluate_time = time.strptime(buy_info[-1],"%Y-%m-%d %H:%M")
            evaluate.content = comment.xpath('.//p[@class="comment-con"]/text()').extract()[0]
            star = comment.xpath('.//div[starts-with(@class,"comment-star")]/@class').extract()
            evaluate.star = int(re.search('(\d)',"".join(star)).group(1))
            comment_num = comment.xpath('.//div[@class="comment-op"]//a[@target="_blank"]/text()').extract()[0]
            evaluate.comment_num = int(comment_num)
            praised_num = comment.xpath('.//div[@class="comment-op"]//a[@class="J-nice"]/text()').extract()[0]
            evaluate.praised_num = int(praised_num)
            image_list = comment.xpath('.//a[@class="J-thumb-img"]//img/@src').extract()
            evaluate.image_list = json.dumps(image_list)
            video_list = comment.xpath('.//a[@class="J-thumb-img current"]//img/@src').extract()
            evaluate.video_list = json.dumps(video_list)
            #保存评价内容
            existed_evaluate = GoodEvaluate.select().where(GoodEvaluate.id == evaluate.id)
            if existed_evaluate:
                evaluate.save()
            else:
                evaluate.save(force_insert=True)

        next_page_xpath ='//div[@class="com-table-footer"]//a[@class="ui-pager-next"]'
        try:
            next_page = browser.find_element_by_xpath(next_page_xpath)
            #next_page.click()由于该元素被其他元素遮挡，导致ElementClickInterceptedException
            next_page.send_keys('\n')
            sel = Selector(text=browser.page_source)
            time.sleep(3)
        except NoSuchElementException:
            print("找不到下一页，获取评论完毕")
            has_next_page = False

if __name__ == '__main__':
    parse_good('4622537')