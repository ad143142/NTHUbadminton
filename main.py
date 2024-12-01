from get_field import Get_field

import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.preprocessing.image import load_img, img_to_array

#校友體育館登入網址
# test_URL = 'C:\\Users\\bywang\\Desktop\\captcha\\god\\國立清華大學 校友體育館.html'
URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code'
# URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state=&ui_locales=zh-TW'
ACCOUNT = "YOUR_ACCOUNT"
PASSWORD = "YOUR_PASSWORD"
MODEL_PATH = "YOUR_MODEL_PATH"

robot = Get_field(URL, ACCOUNT, PASSWORD, MODEL_PATH)
robot.login()
# robot.open_url(test_URL)
'''
robot.get_availble_field(weekday, time)
    weekday: 第幾個星期幾的欄位 (1~5) 5表示最新的日期，非實際星期幾
    time: 第幾個時段 (1~9)
    7:00~8:00	1
    8:00~9:00	2
    9:00~10:00	3
    10:00~11:00	4
    11:00~12:00	5
    12:00~13:00	6
    13:00~14:00	7
    14:00~15:00	8
    15:00~16:00	9
    16:00~17:00	10
    17:00~18:00	11
    18:00~19:00	12
    19:00~20:00	13
    20:00~21:00	14
    21:00~22:00	15
    22:00~23:00	16

'''
robot.get_availble_field('5', '9')
robot.get_availble_field('5', '10')


while True:
    pass
