import base64
import random
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

#1、获取有缺口的图片，并下载
#2、获取完整的图片，并下载
#3、对比两张图片，找出缺口移动的像素
#4、拖动元素

class LoginBiliBili:

    def __init__(self, username, password):
        """
        初始化数据

        :param username: bilibili账号
        :param password: 密码
        """
        self.username = username
        self.password = password
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = wait(self.browser, 50) #等待的最大时间

    def open(self):
        """
        打开浏览器, 进入登陆界面
        输入用户名, 密码
        点击登陆

        :return: None
        """
        self.browser.get(self.url)

        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-username")))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-passwd")))
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.btn.btn-login')))

        username.clear()
        username.send_keys(self.username)
        password.clear()
        password.send_keys(self.password)
        submit.click()

        time.sleep(2)

    def get_geetest_image(self):
        """
        获取极验验证码图片
        :return: c_image(王者验证图) ic_image(有缺失的验证图)
        """
        """
       完整的验证图
       页面源码:
       <canvas class="geetest_canvas_fullbg geetest_fade geetest_absolute" 
       height="160" width="260" style="display: none;"></canvas>
       """
        js = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'
        # 图片数据
        complete_img_data = self.browser.execute_script(js)
        # base64 编码的图片信息
        complete_img_base64 = complete_img_data.split(',')[1]
        # 转成bytes类型
        complete_img = base64.b64decode(complete_img_base64)
        # 加载图片 return 回去对比
        c_image = Image.open(BytesIO(complete_img))
        #c_image.show()
        # 保存图片 (可不必保存)
        c_image.save('c_image.png')

        """
        有缺口的验证图
        页面源码:
        <canvas class="geetest_canvas_bg geetest_absolute" height="160" width="260"></canvas>
        <canvas class="geetest_canvas_slice geetest_absolute" width="260" height="160" style="opacity: 1; display: block;"></canvas>
        """

        #js = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png")'
        js = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'
        #执行js脚本，获取图片base64编码
        incomplete_img_data = self.browser.execute_script(js)
        incomplete_img_base64 = incomplete_img_data.split(',')[1]
        # 转为bytes类型
        incomplete_img = base64.b64decode(incomplete_img_base64)
        ic_image = Image.open(BytesIO(incomplete_img))
        ic_image.save('ic_image.png')

        return c_image, ic_image

    def is_pixel_similar(self, c_image, ic_image, x, y):
        """
        比较两张图片的像素点

        注意: 像素点比较是有偏差的, 需要允许一定范围的误差,
            我们可以设置一个阈值
        :param ic_image:
        :param c_image:
        :param x:
        :param y:
        :return: 当像素点不相同时, 返回 False
        """
        # 获取两张图片执行位置的像素点
        c_pixel = c_image.load()[x, y]
        ic_pixel = ic_image.load()[x,y]

        # 阈值 允许误差
        threshold = 10
        # 对比
        if abs(c_pixel[0] - ic_pixel[0]) < threshold and \
                abs(c_pixel[1] - ic_pixel[1]) < threshold and \
                abs(c_pixel[2] - ic_pixel[2]) < threshold:
            return True
        return False

    def get_slice_gap(self, c_image, ic_image):
        """
        获取缺口的偏移量

        通过比较两张图片的所有像素点, 获取两张图片是从哪里开始不同
        从而得到 移动块 要在 x 方向移动的距离

        :param c_image: 完整的图片
        :param ic_image: 有缺失的图片
        :return: 缺口的偏移量
        """
        # ic_image.size:['width', 'height']
        for x in range(ic_image.size[0]):
            for y in range(ic_image.size[1]):
                if not self.is_pixel_similar(c_image, ic_image, x, y):
                    return x

    def get_path(self,distance):
        result = []
        current = 0
        mid = distance * 3 / 4
        t = 0.1
        v = 0
        while current < distance:
            if current < mid:
                a = random.randint(2,3)
                #a = 10
            else:
                a = -random.randint(6,7)
                #a = -5
            v0 = v
            v = v0 + a * t
            s = v0 * t + 0.5 * a * t * t
            current += s
            result.append(round(s))
        return result
    def drag_slider(self, gap):
        """
        拖动滑块

        :param gap: 需要拖动的距离
        :return: None
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.geetest_slider_button')))
        # 抓住滑块
        ActionChains(self.browser).click_and_hold(on_element=slider).perform()
        # 移动 只在水平方向上移动
        for x in self.get_path(gap-8):
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        # 释放滑块
        ActionChains(self.browser).release().perform()


    def login_success(self):
        """
        判断是否登陆成功
        :return: 成功返回 True 失败返回False
        """
        try:
            # 登录成功后 界面上会有一个消息按钮
            return bool(
                self.wait.until(EC.presence_of_element_located((By.XPATH, 'span:contains("消息")')))
            )
        except :
            return False

    def login(self):
        """
        开始

        :return: None
        """
        self.open()
        c_image, ic_image = self.get_geetest_image()
        gap = self.get_slice_gap(c_image,ic_image)
        self.drag_slider(gap)
        time.sleep(3)

        # if self.login_success():
        #     print('登陆成功')
        # else:
        #     self.login()
        while(not self.login_success()):
            self.login()
            break
        print('登陆成功')

if __name__ == '__main__':
    login = LoginBiliBili('18611732698', 'LJJ8180039abc')
    login.login()

