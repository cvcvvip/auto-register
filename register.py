import requests
import datetime
import json

def main():
    # 1. 生成当天的邮箱（格式：annyMMDD@gmail.com）及固定密码
    today = datetime.datetime.now().strftime("%m%d")
    email = f"aaccy{today}@gmail.com"
    password = "anny333"
    
    print(f"生成的邮箱: {email}")
    print(f"固定密码: {password}")

    # 2. 构造注册请求
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

    # 打印出请求的数据
    print(f"发送注册请求的 URL: {reg_url}")
    print(f"请求数据: {data}")

    # 发送注册请求
    try:
        response = requests.post(reg_url, data=data, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        print(f"注册请求响应状态码: {response.status_code}")

        # 解析响应获取 usertoken
        response_data = response.json()
        print(f"注册响应数据: {response_data}")

        if response_data.get("code") == 200:  # 注册成功
            usertoken = response_data["data"]["usertoken"]
            subscribe_url = f"https://user.imayy.cn/b/subscribe?token={usertoken}"
            print(f"订阅 URL: {subscribe_url}")

            # 模拟浏览器正常访问订阅链接
            sub_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "Referer": "https://h5.imayy.cn/"
            }

            # 获取订阅内容
            sub_response = requests.get(subscribe_url, headers=sub_headers)
            if sub_response.status_code == 200:
                with open("subscribe.txt", "w", encoding="utf-8") as f:
                    f.write(sub_response.text)
                print("订阅内容已保存到 subscribe.txt")
            else:
                print("获取订阅内容失败:", sub_response.status_code)
        else:
            print("注册失败:", response_data.get("msg"))

    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError:
        print("解析注册响应 JSON 失败")

if __name__ == "__main__":
    main()
