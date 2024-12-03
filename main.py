from get_field import Get_field
from get_field import get_fieldAPI

import time
from multiprocessing import Pool
import os
import copy

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.preprocessing.image import load_img, img_to_array

robot = None


def mp_getfieldAPI(cookie, reserve_year, reserve_month, reserve_day, t):
    print("mp_getfieldAPI: start")
    while True:
        cnt = 1
        ret = get_fieldAPI(cookie, reserve_year, reserve_month, reserve_day, t)
        if ret != 1:  # 時間還沒到
            break
        time.sleep(3)
        print("第", cnt, "次嘗試時間未到")
        cnt += 1
    return ret

if __name__ == '__main__':
    #校友體育館登入網址
    test_URL = 'C:\\Users\\bywang\\Desktop\\captcha\\god\\test.html'
    URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code'
    # URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?response_type=code&client_id=eeclass&redirect_uri=https%3A%2F%2Feeclass.nthu.edu.tw%2Fservice%2Foauth%2F&scope=lmsid+userid&state=&ui_locales=zh-TW'
    ACCOUNT = "YOUR_ACCOUNT"
    PASSWORD = "YOUR_PASSWORD"
    MODEL_PATH = "YOUR_MODEL_PATH"

    # robot.open_url(test_URL)
    '''
    robot.get_availble_field(weekday, time)
        weekday: 第幾個星期幾的欄位 (1~5) 5表示最新的日期，非實際星期幾
        time: 第幾個時段
        7:00~8:00	0
        8:00~9:00	1
        9:00~10:00	2
        10:00~11:00	3
        11:00~12:00	4
        12:00~13:00	5
        13:00~14:00	6
        14:00~15:00	7
        15:00~16:00	8
        16:00~17:00	9
        17:00~18:00	10
        18:00~19:00	11
        19:00~20:00	12
        20:00~21:00	13 **
        21:00~22:00	14 **
        22:00~23:00	15

    '''
    reserve_year = 2024
    reserve_month = 12
    reserve_day = 7
    # times = ['13', '14', '8', '9']
    times = ['1', '2']
    results = []

    start_reserve_hour = 10
    start_reserve_min = 55
    start_reserve_sec = 0

    PROCESS_NUM = 2

    robot = Get_field(URL, ACCOUNT, PASSWORD, MODEL_PATH)
    robot.login()
    robot_cookie = robot.get_cookie()
    cnt = 1

    start_time = start_reserve_hour * 3600 + start_reserve_min * 60 + start_reserve_sec
    # 如果現實時間還沒到開始時間，就一直等待到時間到，只檢查時和分

    now = time.mktime(time.localtime())
    while (now % 86400 + 8 * 3600) < start_time:
        now = time.mktime(time.localtime())
        print("等待到達預約時間 {}:{}:{} 現在時間 {}:{}:{}".format(
            start_reserve_hour, start_reserve_min, start_reserve_sec,
            int(((now // 3600 % 24) + 8) % 24), int(now // 60 % 60),
            int(now % 60)))
        time.sleep(1)
    # mp_getfieldAPI(robot, reserve_year, reserve_month, reserve_day, times[0])
    with Pool(PROCESS_NUM) as pool:
        for t in times:
            results.append(
                pool.apply_async(mp_getfieldAPI,
                                 (robot_cookie, reserve_year, reserve_month,
                                  reserve_day, t)))
        pool.close()
        pool.join()

    for idx, ret in enumerate(results):
        print(f"第{idx+1}筆結果: {ret.get()}")
