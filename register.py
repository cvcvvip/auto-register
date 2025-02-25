import requests
import datetime
import json

# 自动生成当天的邮箱
today = datetime.datetime.now().strftime("%m%d")
email = f"anny00{today}@gmail.com"
password = "anny333"

# 发送注册请求
register_url = "https://h5.imayy.cn/reg"
payload = {"email": email, "password": password}
headers = {"Content-Type": "application/json"}

response = requests.post(register_url, json=payload, headers=headers)
print("注册响应:", response.text)

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
