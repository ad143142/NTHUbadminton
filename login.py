from god import Decaptcha

import numpy as np
from selenium import webdriver  # 瀏覽器驅動模組
from webdriver_manager.chrome import ChromeDriverManager  # Chrome瀏覽器驅動模組
from selenium.webdriver.chrome.options import Options  # 瀏覽器選項設定模組
from selenium.webdriver.common.by import By  # 定位元素模組
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from PIL import Image
import requests
from io import BytesIO
import base64
import time

class Login():

    def __init__(self, URL, account, password, model_path):
        self.URL = URL
        self.account = account
        self.password = password
        self.model_path = model_path

    def getCaptchaImg(self, driver):
        # 取得驗證碼圖片
        image_ele = driver.find_elements(By.ID, "captcha_image")[0].screenshot_as_base64
        image = Image.open(BytesIO(base64.b64decode(image_ele)))
        # image.show()
        image_array = np.array(image)
        return image_array

    def login(self):
        # 安裝及啟動Chrome瀏覽器
        driver = webdriver.Chrome()
        # 發送請求到Facebook網站
        driver.get(self.URL)
        driver.find_elements(By.NAME, "id")[0].send_keys(self.account)
        driver.find_elements(By.NAME, "password")[0].send_keys(self.password)
        # 取得驗證碼圖片
        image = self.getCaptchaImg(driver)
        # 輸入驗證碼
        decaptcha = Decaptcha(self.model_path)
        captcha = decaptcha.imgDecaptcha([image])
        print("驗證碼=", captcha)
        driver.find_elements(By.ID, "captcha_code")[0].send_keys(captcha)
        # 保持登入狀態
        driver.find_elements(By.NAME, "keep")[0].click()
        # 等待幾秒防止被擋
        time.sleep(3)
        # 登入
        driver.find_elements(By.CLASS_NAME, "btn-login")[0].click()

        return driver
