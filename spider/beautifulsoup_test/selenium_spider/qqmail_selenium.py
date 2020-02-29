import time

from selenium import webdriver

browser = webdriver.Chrome()

browser.get("https://mail.qq.com/cgi-bin/loginpage")

browser.switch_to.frame(browser.find_element_by_css_selector('#login_frame'))
log_ele = browser.find_element_by_css_selector('#switcher_plogin')

log_ele.click()

username = browser.find_element_by_css_selector('#u')
password = browser.find_element_by_css_selector('#p')
button = browser.find_element_by_css_selector('#login_button')

username.send_keys('501215295')
password.send_keys('JUSTFORYOU1212')
button.click()