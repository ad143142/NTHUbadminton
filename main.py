from get_field import Get_field
from get_field import get_fieldAPI
from form import open_form

import time
from multiprocessing import Pool
import os
import copy

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def mp_getfieldAPI(cookie, reserve_year, reserve_month, reserve_day, t):
    print("mp_getfieldAPI: start")
    while True:
        cnt = 1
        ret = get_fieldAPI(cookie, reserve_year, reserve_month, reserve_day, t)
        if ret == 0:
            break
        elif ret == 1:
            time.sleep(3 * 2)
            print("第", t, "時間段 第", cnt, "次嘗試時間未到")
            cnt += 1
        elif ret == 2:
            time.sleep(3 * 2)
            print("第", t, "時間段 第", cnt, "次嘗試回傳wait")
            cnt += 1
        else:
            print("API 呼叫失敗")
            break

    return ret

PROCESS_NUM = 2
if __name__ == '__main__':

    account, password = open_form()

    #校友體育館登入網址
    URL = 'https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code'
    ACCOUNT = str(account)
    PASSWORD = str(password)
    MODEL_PATH = "./god.h5"
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
    reserve_day = 21
    times = ['13', '14']
    results = []

    start_reserve_hour = 14
    start_reserve_min = 42
    start_reserve_sec = 0

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
