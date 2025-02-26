import random
import string
import datetime
import requests
import json
import os

def main():
    # 生成2位字母和2位数字
    random_letters = ''.join(random.choices(string.ascii_lowercase, k=2))  # 生成2位小写字母
    random_digits = ''.join(random.choices(string.digits, k=2))  # 生成2位数字

    # 获取当前日期，格式为mmdd
    today = datetime.datetime.now().strftime("%m%d")

    # 拼接邮箱地址
    email = f"uuss{random_letters}{random_digits}{today}@gmail.com"
    password = "anny333"

    # 构造注册请求
    reg_url = "https://user.imayy.cn/b/reg"
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

    response = requests.post(reg_url, data=data, headers=headers)
    print("注册请求响应状态码:", response.status_code)
    print("注册响应数据:", response.json())
    
    # 你可以在这里继续添加处理订阅内容的逻辑


    # 解析响应获取 usertoken
    try:
        response_data = response.json()
        if response_data.get("code") == 200:  # 注册成功
            usertoken = response_data["data"]["usertoken"]
            cities = {
                "订阅": "https://user.imayy.cn/b/subscribe?token={}".format(usertoken),
                "香港": "https://user.imayy.cn/b/subscribe?token={}&city=%E9%A6%99%E6%B8%AF".format(usertoken),
                "新加坡": "https://user.imayy.cn/b/subscribe?token={}&city=%E6%96%B0%E5%8A%A0%E5%9D%A1".format(usertoken),
                "日本": "https://user.imayy.cn/b/subscribe?token={}&city=%E6%97%A5%E6%9C%AC".format(usertoken),
                "韩国": "https://user.imayy.cn/b/subscribe?token={}&city=%E9%9F%A9%E5%9B%BD".format(usertoken),
                "美国": "https://user.imayy.cn/b/subscribe?token={}&city=%E7%BE%8E%E5%9B%BD".format(usertoken),
                "澳大利亚": "https://user.imayy.cn/b/subscribe?token={}&city=%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A".format(usertoken),
                "荷兰": "https://user.imayy.cn/b/subscribe?token={}&city=%E8%8D%B7%E5%85%B0".format(usertoken),
                "英国": "https://user.imayy.cn/b/subscribe?token={}&city=%E8%8B%B1%E5%9B%BD".format(usertoken),
                "德国": "https://user.imayy.cn/b/subscribe?token={}&city=%E5%BE%B7%E5%9B%BD".format(usertoken),
                "西班牙": "https://user.imayy.cn/b/subscribe?token={}&city=%E8%A5%BF%E7%8F%AD%E7%89%99".format(usertoken),
                "加拿大": "https://user.imayy.cn/b/subscribe?token={}&city=%E5%8A%A0%E6%8B%BF%E5%A4%A7".format(usertoken),
            }

            # 创建一个空字符串来存储所有城市的订阅内容
            all_subscriptions = ""

            # 获取所有城市的订阅内容并合并
            for city, url in cities.items():
                print(f"获取 {city} 的订阅内容...")
                sub_response = requests.get(url)
                if sub_response.status_code == 200:
                    all_subscriptions += f"===== {city} 订阅内容 =====\n"
                    all_subscriptions += sub_response.text + "\n\n"
                    print(f"{city} 订阅内容已获取")
                else:
                    print(f"获取 {city} 订阅内容失败:", sub_response.status_code)

            # 将合并的订阅内容保存到一个文件中
            with open("all_subscriptions.txt", "w", encoding="utf-8") as f:
                f.write(all_subscriptions)
            print("所有城市的订阅内容已保存到 all_subscriptions.txt")

            # 提交到 GitHub 仓库
            os.system("git add .")
            os.system('git commit -m "更新所有城市合并后的订阅文件"')
            os.system("git push")

        else:
            print("注册失败:", response_data.get("msg"))

    except json.JSONDecodeError:
        print("解析注册响应 JSON 失败")

if __name__ == "__main__":
    main()
