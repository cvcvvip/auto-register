import requests
import datetime

# 目标URL
URL = "https://user.imayy.cn/b/reg"

# 计算当前日期 (MMDD)
today = datetime.datetime.now().strftime("%m%d")

# 生成邮箱和密码
email = f"anny{today}@gmail.com"
password = "anny333"

# 表单数据
data = {
    "email": email,
    "pass": password,
    "tg": "kl",
    "ver": "1",
    "token": ""  # 如果需要，可以填写
}

# 请求头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://h5.imayy.cn",
    "Referer": "https://h5.imayy.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# 发送POST请求
try:
    response = requests.post(URL, headers=headers, data=data, timeout=10)
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
except requests.RequestException as e:
    print("请求失败:", str(e))
