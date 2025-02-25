import requests
import datetime
import json

def main():
    # 1. 生成当天的邮箱（格式：annyMMDD@gmail.com）及固定密码
    today = datetime.datetime.now().strftime("%m%d")
    email = f"anny11{today}@gmail.com"
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
    
    try:
        reg_response = requests.post(reg_url, data=data, headers=headers, timeout=10)
        print("注册响应状态码:", reg_response.status_code)
        print("注册响应内容:", reg_response.text)
    except Exception as e:
        print("注册请求异常:", e)
        return

    # 3. 解析注册响应，提取 usertoken
    try:
        reg_json = reg_response.json()
    except Exception as e:
        print("无法解析注册响应为 JSON:", e)
        return

    if reg_json.get("code") != 0:
        print("注册失败，错误信息:", reg_json.get("msg", "未知错误"))
        return

    # 根据抓包信息，usertoken 可能位于 reg_json["data"]["usertoken"]
    usertoken = reg_json.get("data", {}).get("usertoken")
    if not usertoken:
        print("未在响应中找到 usertoken")
        return

    # 4. 拼接订阅链接
    subscribe_url = f"https://user.imayy.cn/b/subscribe?token={usertoken}"
    print("拼接后的订阅链接:", subscribe_url)

    # 5. 获取订阅链接的内容并保存到文件
    try:
        sub_response = requests.get(subscribe_url, headers=headers, timeout=10)
        print("订阅请求状态码:", sub_response.status_code)
        if sub_response.status_code == 200:
            with open("subscribe.txt", "w", encoding="utf-8") as f:
                f.write(sub_response.text)
            print("订阅内容已保存到 subscribe.txt")
        else:
            print("获取订阅内容失败，状态码:", sub_response.status_code)
    except Exception as e:
        print("获取订阅内容异常:", e)

if __name__ == '__main__':
    main()
