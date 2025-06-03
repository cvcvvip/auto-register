#!/bin/bash

# 确保以 root 运行
if [[ $EUID -ne 0 ]]; then
   echo "请使用 root 用户执行脚本！"
   exit 1
fi

DOMAIN="aem.three.com.hk"

echo "开始安装 Xray-core..."
bash <(curl -Ls https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)

UUID=$(cat /proc/sys/kernel/random/uuid)

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

echo "设置权限..."
chown -R root:root /usr/local/etc/xray
chmod 600 /usr/local/etc/xray/private.key
chmod 644 /usr/local/etc/xray/cert.crt

echo "启用并重启 Xray 服务..."
systemctl enable xray
systemctl restart xray

IP=$(curl -s https://api.ipify.org)

VLESS_LINK="vless://${UUID}@${IP}:443?type=tcp&security=xtls&flow=xtls-rprx-direct&sni=${DOMAIN}#${DOMAIN}"

echo -e "\n✅ 安装完成！\n"
echo "伪装域名: $DOMAIN"
echo "服务器IP: $IP"
echo "UUID: $UUID"
echo "VLESS+XTLS订阅链接："
echo "$VLESS_LINK"
