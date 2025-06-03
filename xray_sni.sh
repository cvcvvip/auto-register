#!/bin/bash

# 安装 Xray-core
bash <(curl -Ls https://raw.githubusercontent.com/XTLS/Xray-install/main/install-release.sh)

# 生成 Xray 配置文件
UUID=$(cat /proc/sys/kernel/random/uuid)

mkdir -p /usr/local/etc/xray

cat > /usr/local/etc/xray/config.json <<EOF
{
  "inbounds": [{
    "port": 443,
    "protocol": "vless",
    "settings": {
      "clients": [
        {
          "id": "$UUID",
          "flow": "xtls-rprx-vision"
        }
      ],
      "decryption": "none",
      "fallbacks": []
    },
    "streamSettings": {
      "network": "tcp",
      "security": "tls",
      "tlsSettings": {
        "serverName": "aem.three.com.hk",
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

# 创建伪造证书（自签）
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -subj "/CN=aem.three.com.hk" \
  -keyout /usr/local/etc/xray/private.key \
  -out /usr/local/etc/xray/cert.crt

# 设置开机自启并重启 Xray
systemctl enable xray
systemctl restart xray

echo "✅ Xray 安装完毕"
echo "✅ UUID: $UUID"
echo "✅ 伪装域名: aem.three.com.hk"
