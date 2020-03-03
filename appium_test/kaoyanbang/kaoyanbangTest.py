import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC

cap = {
    "platformName": "Android",
    "platformVersion": "6.0.1",
    "deviceName": "emulator-5554",
    "appPackage": "com.tal.kaoyan",
    "appActivity": "com.tal.kaoyan.ui.activity.SplashActivity"

}


driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",cap)
wait = WAIT(driver,5)
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"))).click()
#点击跳过按钮

skip_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@text='跳过 > ']")))
skip_button.click()
#获取用户名输入框，并输入用户名
username = wait.until(EC.presence_of_element_located((By.XPATH,"//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_email_edittext']")))
username.send_keys("Change0224")
#获取密码输入框，并输入密码
password = wait.until(EC.presence_of_element_located((By.XPATH,"//android.widget.EditText[@resource-id='com.tal.kaoyan:id/login_password_edittext']")))
password.send_keys("LJJ8180039")
#点击登录按钮
submit = wait.until(EC.element_to_be_clickable((By.XPATH,"//android.widget.Button[@resource-id='com.tal.kaoyan:id/login_login_btn']")))
submit.click()

#点击研讯按钮
time.sleep(8)

wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@text='研讯']"))).click()

time.sleep(3)
x = driver.get_window_size()["width"]
y = driver.get_window_size()["height"]
driver.swipe(int(x*0.5),int(y*0.75),int(x*0.5),int(y*0.25))
