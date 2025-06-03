#!/bin/bash

# 必须root运行
if [[ $EUID -ne 0 ]]; then
   echo "请用 root 用户执行该脚本"
   exit 1
fi

# 伪装域名，改这里即可
DOMAIN="aem.three.com.hk"

echo "开始安装 Xray-core..."
bash <(curl -Ls https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)

UUID=$(cat /proc/sys/kernel/random/uuid)

echo "创建 Xray 配置目录..."
mkdir -p /usr/local/etc/xray

echo "生成 Xray 配置文件..."

cat > /usr/local/etc/xray/config.json <<EOF
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [{
    "port": 443,
    "protocol": "vless",
    "settings": {
      "clients": [
        {
          "id": "$UUID",
          "flow": "xtls-rprx-direct"
        }
      ],
      "decryption": "none",
      "fallbacks": []
    },
    "streamSettings": {
      "network": "tcp",
      "security": "tls",
      "tlsSettings": {
        "serverName": "$DOMAIN",
        "certificates": [
          {
            "certificateFile": "/usr/local/etc/xray/cert.crt",
            "keyFile": "/usr/local/etc/xray/private.key"
          }
        ]
      }
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  }]
}
EOF

echo "生成自签证书..."
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -subj "/CN=$DOMAIN" \
  -keyout /usr/local/etc/xray/private.key \
  -out /usr/local/etc/xray/cert.crt

echo "设置并启动 Xray 服务..."
systemctl enable xray
systemctl restart xray

# 获取VLESS链接格式
# 格式示范：
# vless://UUID@服务器IP:端口?type=tcp&security=xtls&flow=xtls-rprx-direct&sni=域名#备注

IP=$(curl -s https://api.ipify.org)

VLESS_LINK="vless://${UUID}@${IP}:443?type=tcp&security=xtls&flow=xtls-rprx-direct&sni=${DOMAIN}#${DOMAIN}"

echo -e "\n✅ 安装完成！以下是你的节点信息："
echo "伪装域名: $DOMAIN"
echo "服务器IP: $IP"
echo "UUID: $UUID"
echo "VLESS+XTLS订阅链接:"
echo "$VLESS_LINK"

echo -e "\n请确保手机或电脑客户端支持 VLESS + XTLS 连接方式"
