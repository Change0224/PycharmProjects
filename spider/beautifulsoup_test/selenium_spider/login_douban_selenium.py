from telnetlib import EC

from selenium import webdriver

browser = webdriver.Chrome()

browser.get("https://www.douban.com/")

browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))
log_ele = browser.find_element_by_css_selector('li.account-tab-account')

log_ele.click()

username = browser.find_element_by_css_selector('#username')
password = browser.find_element_by_css_selector('#password')
button = browser.find_element_by_css_selector('a.btn.btn-account')

username.send_keys('18611732698')
password.send_keys('LJJ8180039abc')
button.click()



