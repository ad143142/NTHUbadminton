from login import Login

import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.preprocessing.image import load_img, img_to_array

#校友體育館登入網址
URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code'
# URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state=&ui_locales=zh-TW'
ACCOUNT = None
PASSWORD = None
MODEL_PATH = 'C:\\Path to model\\god.h5'

login = Login(URL, ACCOUNT, PASSWORD, MODEL_PATH)
login.login()

while True:
    pass
