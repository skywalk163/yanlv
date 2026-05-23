# 言律语言 Playground 详细部署步骤

## 部署方案选择

### 方案一：华为云部署（推荐）

#### 步骤1：购买华为云ECS

1. 登录 [华为云控制台](https://console.huaweicloud.com/)
2. 选择"弹性云服务器 ECS"
3. 点击"购买弹性云服务器"
4. 配置选择：
   - 区域：华北-北京四（或其他就近区域）
   - 规格：通用计算型 | 1vCPU | 1GB
   - 镜像：Ubuntu 20.04 server 64bit
   - 系统盘：高IO | 40GB
   - 网络：默认VPC
   - 安全组：放通22、80、443、5000端口
   - 密码：设置root密码
5. 点击"立即购买"

#### 步骤2：连接服务器

```bash
# 使用SSH连接
ssh root@your-server-ip

# 或使用华为云控制台的远程登录功能
```

#### 步骤3：安装依赖

```bash
# 更新系统
apt update && apt upgrade -y

# 安装Python 3.8+
apt install python3 python3-pip python3-venv -y

# 安装Nginx
apt install nginx -y

# 安装Git
apt install git -y
```

#### 步骤4：部署应用

```bash
# 创建应用目录
mkdir -p /var/www/yanlv
cd /var/www/yanlv

# 克隆代码
git clone https://gitcode.com/skywalk163/yanlv.git .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
cd playground
pip install -r requirements.txt
pip install gunicorn gevent
```

#### 步骤5：配置Gunicorn

创建 `gunicorn.conf.py`：
```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
keepalive = 120
timeout = 120
```

#### 步骤6：配置Systemd服务

创建 `/etc/systemd/system/yanlv.service`：
```ini
[Unit]
Description=YanLv Playground
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/yanlv/playground
Environment="PATH=/var/www/yanlv/venv/bin"
ExecStart=/var/www/yanlv/venv/bin/gunicorn -c gunicorn.conf.py server:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
# 重载systemd
systemctl daemon-reload

# 启动服务
systemctl start yanlv

# 设置开机自启
systemctl enable yanlv

# 查看状态
systemctl status yanlv
```

#### 步骤7：配置Nginx

创建 `/etc/nginx/sites-available/yanlv`：
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 或服务器IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置：
```bash
# 创建软链接
ln -s /etc/nginx/sites-available/yanlv /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重载Nginx
systemctl reload nginx
```

#### 步骤8：配置SSL（可选）

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx -y

# 申请证书
certbot --nginx -d your-domain.com

# 自动续期
certbot renew --dry-run
```

#### 步骤9：验证部署

```bash
# 检查服务状态
systemctl status yanlv
systemctl status nginx

# 检查端口
netstat -tulpn | grep :5000
netstat -tulpn | grep :80

# 测试访问
curl http://localhost:5000/api/examples
```

---

### 方案二：Railway免费部署

#### 步骤1：准备代码

创建 `Procfile`：
```
web: cd playground && python server.py
```

创建 `runtime.txt`：
```
python-3.8.10
```

更新 `requirements.txt`：
```txt
flask>=2.0.0
flask-cors>=3.0.0
jieba>=0.42.0
gunicorn>=20.0.0
```

#### 步骤2：部署到Railway

1. 访问 [Railway](https://railway.app/)
2. 使用GitHub登录
3. 点击"New Project"
4. 选择"Deploy from GitHub repo"
5. 选择 `yanlv` 仓库
6. Railway会自动检测并部署

#### 步骤3：配置环境变量

在Railway控制台设置：
- `FLASK_ENV` = `production`
- `FLASK_DEBUG` = `0`

#### 步骤4：获取访问地址

Railway会自动分配一个域名，如：
`https://yanlv-production.up.railway.app`

---

### 方案三：Render免费部署

#### 步骤1：创建render.yaml

```yaml
services:
  - type: web
    name: yanlv-playground
    env: python
    buildCommand: pip install -r playground/requirements.txt
    startCommand: cd playground && python server.py
    envVars:
      - key: FLASK_ENV
        value: production
```

#### 步骤2：部署到Render

1. 访问 [Render](https://render.com/)
2. 连接GitHub账号
3. 创建新的Web Service
4. 选择 `yanlv` 仓库
5. Render会自动部署

---

### 方案四：Docker部署

#### 步骤1：创建Dockerfile

创建 `playground/Dockerfile`：
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "server.py"]
```

#### 步骤2：构建镜像

```bash
# 构建镜像
docker build -t yanlv-playground ./playground

# 测试运行
docker run -p 5000:5000 yanlv-playground
```

#### 步骤3：推送到镜像仓库

```bash
# 登录Docker Hub
docker login

# 标记镜像
docker tag yanlv-playground your-username/yanlv-playground:latest

# 推送镜像
docker push your-username/yanlv-playground:latest
```

#### 步骤4：在服务器上运行

```bash
# 拉取镜像
docker pull your-username/yanlv-playground:latest

# 运行容器
docker run -d \
  --name yanlv \
  -p 5000:5000 \
  --restart always \
  your-username/yanlv-playground:latest
```

---

## 部署后配置

### 1. 配置防火墙

```bash
# Ubuntu UFW
ufw allow 22      # SSH
ufw allow 80      # HTTP
ufw allow 443     # HTTPS
ufw allow 5000    # 应用端口
ufw enable

# 或华为云安全组配置
# 在控制台配置入站规则
```

### 2. 配置日志

```bash
# 查看应用日志
journalctl -u yanlv -f

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 3. 配置监控

```bash
# 安装htop
apt install htop

# 查看系统资源
htop

# 查看进程
ps aux | grep gunicorn
```

### 4. 配置备份

```bash
# 创建备份脚本
cat > /root/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /root/backup/yanlv-$DATE.tar.gz /var/www/yanlv
# 保留最近7天的备份
find /root/backup -name "yanlv-*.tar.gz" -mtime +7 -delete
EOF

chmod +x /root/backup.sh

# 配置定时任务
crontab -e
# 添加：0 2 * * * /root/backup.sh
```

---

## 常见问题排查

### 问题1：服务无法启动

```bash
# 查看详细日志
journalctl -u yanlv -n 100

# 检查端口占用
netstat -tulpn | grep 5000

# 手动启动测试
cd /var/www/yanlv/playground
source ../venv/bin/activate
python server.py
```

### 问题2：无法访问

```bash
# 检查防火墙
ufw status

# 检查Nginx
nginx -t
systemctl status nginx

# 检查应用
systemctl status yanlv

# 测试本地访问
curl http://localhost:5000
```

### 问题3：性能问题

```bash
# 增加worker数量
# 编辑 gunicorn.conf.py
workers = 4  # 根据CPU核心数调整

# 重启服务
systemctl restart yanlv
```

---

## 更新部署

```bash
# SSH到服务器
ssh root@your-server-ip

# 进入项目目录
cd /var/www/yanlv

# 拉取最新代码
git pull

# 更新依赖
source venv/bin/activate
cd playground
pip install -r requirements.txt

# 重启服务
systemctl restart yanlv

# 查看状态
systemctl status yanlv
```

---

## 访问地址

部署完成后，可以通过以下地址访问：

- **直接访问：** `http://your-server-ip:5000`
- **通过Nginx：** `http://your-domain.com`
- **HTTPS：** `https://your-domain.com`（配置SSL后）

---

## 成功标志

部署成功的标志：
- ✅ 服务状态为active (running)
- ✅ 可以访问主页
- ✅ API接口正常响应
- ✅ 可以运行代码
- ✅ 日志无错误信息

---

**恭喜！部署完成！** 🎉

现在可以开始使用在线Playground了。
