from god import Decaptcha

import numpy as np
from selenium import webdriver  # 瀏覽器驅動模組
from webdriver_manager.chrome import ChromeDriverManager  # Chrome瀏覽器驅動模組
from selenium.webdriver.chrome.options import Options  # 瀏覽器選項設定模組
from selenium.webdriver.common.by import By  # 定位元素模組
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import requests
from io import BytesIO
import base64
import time


class Get_field():

    def __init__(self, URL, account, password, model_path):
        self.URL = URL
        self.account = account
        self.password = password
        self.model_path = model_path

    def getCaptchaImg(self, driver):
        # 取得驗證碼圖片
        image_ele = driver.find_elements(
            By.ID, "captcha_image")[0].screenshot_as_base64
        image = Image.open(BytesIO(base64.b64decode(image_ele)))
        # image.show()
        image_array = np.array(image)
        return image_array

    def login(self):
        # 安裝及啟動Chrome瀏覽器
        self.driver = webdriver.Chrome()
        # 發送請求到Facebook網站
        self.driver.get(self.URL)
        self.driver.find_elements(By.NAME, "id")[0].send_keys(self.account)
        self.driver.find_elements(By.NAME,
                                  "password")[0].send_keys(self.password)
        # 取得驗證碼圖片
        image = self.getCaptchaImg(self.driver)
        # 輸入驗證碼
        decaptcha = Decaptcha(self.model_path)
        captcha = decaptcha.imgDecaptcha([image])
        print("驗證碼=", captcha)
        self.driver.find_elements(By.ID, "captcha_code")[0].send_keys(captcha)
        # 保持登入狀態
        self.driver.find_elements(By.NAME, "keep")[0].click()
        # 等待幾秒防止被擋
        time.sleep(3)
        # 登入
        self.driver.find_elements(By.CLASS_NAME, "btn-login")[0].click()

        return self.driver

    def open_url(self, URL):
        # 安裝及啟動Chrome瀏覽器
        self.driver = webdriver.Chrome()
        self.driver.get(URL)

        return self.driver

    def get_availble_field(self, weekday, time):
        print("get_availble_field: start")
        weekday_XPath = "//*[@id='frame_2']/table/tbody/tr[1]/td/table[1]/tbody/tr/td[" + weekday + "]/div[1]"
        table_header = self.driver.find_elements(By.XPATH, weekday_XPath)[0]
        table_header.click()

        table_XPath = "//*[@id='reservation']/tbody/tr[" + time + "]"
        table_data = self.driver.find_elements(By.XPATH, table_XPath)[0]

        available = table_data.find_elements(
            By.XPATH, "./td//*[@id='reservation_available']")

        driver_wait = WebDriverWait(self.driver, timeout=5, poll_frequency=0.1)
        for i in reversed(range(0, len(available))):
            available[i].click()
            # 該預約最晚可以於 [date] 進行取消，是否確定預約?
            alert = driver_wait.until(EC.alert_is_present())
            print(alert.text)
            alert.accept()
            alert = driver_wait.until(EC.alert_is_present())
            if (alert.text == "預約成功"):
                print(alert.text)
                alert.accept()
                return True
            else:
                print(alert.text)
                alert.accept()
        
        print("No available")
        return False
