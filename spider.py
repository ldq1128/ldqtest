import requests
import json
import time
import pandas as pd

headers = {
    'origin': 'https://www.lagou.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    ,
    'referer': 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
}


# 获取cookies值
def get_cookie():
    # 原始网页的URL,即url_start
    url = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
    s = requests.Session()
    s.get(url, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    return cookie


# 定义获取页数的函数
def get_page(url, params):
    html = requests.post(url, data=params, headers=headers, cookies=get_cookie(), timeout=5)
    # 将网页的Html文件加载为json文件
    json_data = json.loads(html.text)
    # 解析json文件，后跟中括号为解析的路径
    total_Count = json_data['content']['positionResult']['totalCount']
    page_number = int(total_Count / 15) if int(total_Count / 15) < 92 else 92
    # 调用get_info函数，传入url和页数
    get_info(url, page_number)


# 定义获取与python有关职位信息函数
def get_info(url, page):
    for pn in range(1, page + 1):
        # post请求参数
        params = {
            "first": "true",
            "pn": str(pn),
            "kd": "python"
        }
        # 获取信息并捕获异常
        try:
            html = requests.post(url, data=params, headers=headers, cookies=get_cookie(), timeout=5)
            print(url, html.status_code)
            # 将网页的Html文件加载为json文件
            json_data = json.loads(html.text)
            # 解析json文件，后跟中括号为解析的路径
            results = json_data['content']['positionResult']['result']
            df = pd.DataFrame(results)
            if pn == 1:
                total_df = df
            else:
                total_df = pd.concat([total_df, df], axis=0)
            # 睡眠2秒
            time.sleep(2)
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            pass
        total_df.to_csv('Python_jobs.csv', sep=',', header=True, index=False)


url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
params = {
    "first": "true",
    "pn": 1,
    "kd": "python"
}
get_page(url, params)
