#!/bin/bash
# 言律语言 Playground 自动部署脚本
# 适用于Ubuntu服务器

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  言律语言 Playground 部署脚本"
echo "=========================================="
echo ""

# 配置变量
APP_DIR="/var/www/yanlv"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="/var/log/yanlv"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用root用户或sudo运行此脚本"
    exit 1
fi

echo "步骤1: 更新系统..."
apt update -y

echo "步骤2: 安装依赖..."
apt install -y python3 python3-pip python3-venv nginx git

echo "步骤3: 创建应用目录..."
mkdir -p $APP_DIR
mkdir -p $LOG_DIR

echo "步骤4: 克隆代码..."
if [ -d "$APP_DIR/.git" ]; then
    echo "代码已存在，更新代码..."
    cd $APP_DIR
    git pull
else
    echo "克隆新代码..."
    rm -rf $APP_DIR/*
    git clone https://gitcode.com/skywalk163/yanlv.git $APP_DIR
fi

echo "步骤5: 创建虚拟环境..."
cd $APP_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo "步骤6: 安装Python依赖..."
cd playground
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn gevent

echo "步骤7: 配置Gunicorn..."
cat > $APP_DIR/playground/gunicorn.conf.py << 'EOF'
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
keepalive = 120
timeout = 120
errorlog = "/var/log/yanlv/gunicorn.error.log"
accesslog = "/var/log/yanlv/gunicorn.access.log"
EOF

echo "步骤8: 创建Systemd服务..."
cat > /etc/systemd/system/yanlv.service << EOF
[Unit]
Description=YanLv Playground
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR/playground
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn -c gunicorn.conf.py server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "步骤9: 配置Nginx..."
cat > /etc/nginx/sites-available/yanlv << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/yanlv/playground/static;
    }
}
EOF

# 启用Nginx配置
ln -sf /etc/nginx/sites-available/yanlv /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

echo "步骤10: 启动服务..."
# 重载systemd
systemctl daemon-reload

# 启动应用
systemctl start yanlv
systemctl enable yanlv

# 重启Nginx
nginx -t
systemctl restart nginx
systemctl enable nginx

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "访问地址: http://192.168.1.12"
echo ""
echo "常用命令:"
echo "  查看状态: systemctl status yanlv"
echo "  查看日志: journalctl -u yanlv -f"
echo "  重启服务: systemctl restart yanlv"
echo "  停止服务: systemctl stop yanlv"
echo ""
echo "日志文件:"
echo "  应用日志: $LOG_DIR/gunicorn.error.log"
echo "  访问日志: $LOG_DIR/gunicorn.access.log"
echo "  Nginx日志: /var/log/nginx/"
echo ""

# 验证部署
echo "验证部署..."
sleep 3
if systemctl is-active --quiet yanlv; then
    echo "✅ YanLv服务运行正常"
else
    echo "❌ YanLv服务启动失败"
    echo "查看错误日志: journalctl -u yanlv -n 50"
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Nginx服务运行正常"
else
    echo "❌ Nginx服务启动失败"
fi

echo ""
echo "测试访问..."
curl -s http://localhost:5000/api/examples > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ API接口正常"
else
    echo "❌ API接口异常"
fi

echo ""
echo "部署完成！请在浏览器中访问: http://192.168.1.12"
