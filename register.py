import requests
import datetime
import json

def main():
    # 1. 生成当天的邮箱（格式：annyMMDD@gmail.com）及固定密码
    today = datetime.datetime.now().strftime("%m%d")
    email = f"001anny{today}@gmail.com"
    password = "anny333"

    # 2. 构造注册请求
    reg_url = "https://user.imayy.cn/b/reg"
    # 注意：抓包信息显示注册接口使用的字段名为 pass 而不是 password
    data = {
        "email": email,
        "pass": password,
        "tg": "kl",
        "ver": "1",
        "token": ""
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Origin": "https://h5.imayy.cn",
        "Referer": "https://h5.imayy.cn/"
    }

# 解析响应获取 usertoken
try:
    response_data = response.json()
    if response_data.get("code") == 200:  # 注册成功
        usertoken = response_data["data"]["usertoken"]
        subscribe_url = f"https://user.imayy.cn/b/subscribe?token={usertoken}"
        
        # 获取订阅内容
        sub_response = requests.get(subscribe_url)
        if sub_response.status_code == 200:
            with open("subscribe.txt", "w", encoding="utf-8") as f:
                f.write(sub_response.text)
            print("订阅内容已保存到 subscribe.txt")
        else:
            print("获取订阅内容失败:", sub_response.status_code)
    else:
        print("注册失败:", response_data.get("msg"))

except json.JSONDecodeError:
    print("解析注册响应 JSON 失败")
