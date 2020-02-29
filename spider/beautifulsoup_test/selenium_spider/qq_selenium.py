import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
WAIT = WAIT(browser, 2) #等待的最大时间
browser.get("https://www.qq.com")

log_ele = browser.find_element_by_css_selector('#top-login > div.item.item-login.fl > a')

log_ele.click()

browser.switch_to.frame(browser.find_element_by_css_selector('#ptlogin_iframe'))

log_ele = browser.find_element_by_css_selector('#switcher_plogin')
log_ele.click()
#
# username = browser.find_element_by_css_selector('#u')
# password = browser.find_element_by_css_selector('#p')
# button = browser.find_element_by_css_selector('#login_button')
#
# username.send_keys('501215295')
# password.send_keys('JUSTFORYOU1212')
# button.click()




try:
    username = WAIT.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#u"))
    )
    password = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#p")))
    submit = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login_button')))

    username.send_keys('501215295')
    password.send_keys('JUSTFORYOU1212')
    submit.click()
    time.sleep(60)
finally:
    browser.close()