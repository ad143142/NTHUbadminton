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
import datetime
import json


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

    def get_cookie(self):
        return self.cookie

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

        self.cookie = self.driver.get_cookies()[0]['value']

        return self.driver

    def open_url(self, URL):
        # 安裝及啟動Chrome瀏覽器
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        print("ASDASD")
        return self.driver

    def get_available_field(self, weekday, time):
        print("get_availble_field: start")
        weekday_XPath = "//*[@id='frame_2']/table/tbody/tr[1]/td/table[1]/tbody/tr/td[" + weekday + "]/div[1]"
        self.driver.implicitly_wait(1)
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
                print("weekdays:", weekday, "times:", time,
                      "result: available")
                return True
            else:
                print(alert.text)
                alert.accept()

        print("No available")
        return False


def get_fieldAPI(cookie, reserve_year, reserve_month, reserve_day, timeID):
    print("get_fieldAPI: start")
    date_time = datetime.datetime(reserve_year, reserve_month, reserve_day, 0,
                                  0)
    timestamp = str(int(time.mktime(date_time.timetuple())))

    # API URL
    url = 'https://nthualb.url.tw/reservation/api/reserve_field'
    cookie_str = 'PHPSESSID=' + cookie

    order = [3, 4, 2, 5, 1, 6, 0, 7]
    for fieldID in order:
        # API 請求資料
        data = {
            'time': str(timeID),  # 替換為您需要的 timeID
            'field': str(fieldID),  # 替換為您需要的 fieldID
            'date': timestamp  # 替換為您需要的日期
        }

        # 進行 API 請求
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',  # 確保告知伺服器傳送的是 JSON 格式
                'Cookie': cookie_str  # 替換為您的 PHPSESSID
            },
            data=json.dumps(data)  # 將 Python 字典轉為 JSON
        )

        # 處理回應
        if response.status_code == 200:
            print(f"Response: {response.text}")
            if (response.text == "預約失敗，日期錯誤"):
                return 1
            elif (response.text == "reserved"):
                continue
            elif (response.text == "ok"):
                print("預約成功，目前時間為", time.localtime())
                return 0
            else:
                return -1
        else:
            print(f"Failed to call API. Status Code: {response.status_code}")
            return -1
    return 2
