import requests
import datetime

# 生成当天的邮箱
today_date = datetime.datetime.now().strftime("%m%d")
email = f"anny{today_date}@gmail.com"
password = "anny333"

# 目标注册 API（需要替换成实际 API）
url = "https://h5.imayy.cn/reg"

# 构造请求数据
data = {
    "email": email,
    "password": password
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 输出结果
print(f"注册邮箱: {email}")
print(f"注册密码: {password}")
print(f"响应状态: {response.status_code}")
print(f"响应内容: {response.text}")
