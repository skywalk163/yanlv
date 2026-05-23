# 言律语言 Playground 部署到 192.168.1.12

## 快速部署步骤

### 方式一：自动部署（推荐）

#### 步骤1：上传部署脚本到服务器

```bash
# 在本地执行，上传部署脚本
scp deploy/deploy.sh root@192.168.1.12:/root/
```

#### 步骤2：SSH连接到服务器

```bash
ssh root@192.168.1.12
```

#### 步骤3：运行部署脚本

```bash
# 添加执行权限
chmod +x /root/deploy.sh

# 运行部署
/root/deploy.sh
```

#### 步骤4：验证部署

在浏览器中访问：`http://192.168.1.12`

---

### 方式二：手动部署

如果自动部署失败，可以手动执行以下步骤：

#### 步骤1：连接服务器

```bash
ssh root@192.168.1.12
```

#### 步骤2：更新系统

```bash
apt update && apt upgrade -y
```

#### 步骤3：安装依赖

```bash
apt install -y python3 python3-pip python3-venv nginx git
```

#### 步骤4：克隆代码

```bash
mkdir -p /var/www/yanlv
cd /var/www/yanlv
git clone https://gitcode.com/skywalk163/yanlv.git .
```

#### 步骤5：安装Python依赖

```bash
python3 -m venv venv
source venv/bin/activate
cd playground
pip install -r requirements.txt
pip install gunicorn gevent
```

#### 步骤6：启动应用

```bash
# 测试启动
python server.py
```

如果测试成功，按Ctrl+C停止，然后配置为系统服务。

#### 步骤7：配置系统服务

```bash
# 创建服务文件
cat > /etc/systemd/system/yanlv.service << 'EOF'
[Unit]
Description=YanLv Playground
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/yanlv/playground
Environment="PATH=/var/www/yanlv/venv/bin"
ExecStart=/var/www/yanlv/venv/bin/python server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl start yanlv
systemctl enable yanlv
```

#### 步骤8：配置Nginx（可选）

```bash
# 创建Nginx配置
cat > /etc/nginx/sites-available/yanlv << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/yanlv /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# 重启Nginx
nginx -t
systemctl restart nginx
```

---

## 验证部署

### 1. 检查服务状态

```bash
# 查看YanLv服务状态
systemctl status yanlv

# 查看Nginx服务状态
systemctl status nginx
```

### 2. 检查端口

```bash
# 检查5000端口
netstat -tulpn | grep 5000

# 检查80端口
netstat -tulpn | grep 80
```

### 3. 测试API

```bash
# 测试本地访问
curl http://localhost:5000/api/examples

# 测试外部访问
curl http://192.168.1.12/api/examples
```

### 4. 查看日志

```bash
# 查看应用日志
journalctl -u yanlv -f

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 常用管理命令

### 服务管理

```bash
# 启动服务
systemctl start yanlv

# 停止服务
systemctl stop yanlv

# 重启服务
systemctl restart yanlv

# 查看状态
systemctl status yanlv

# 查看日志
journalctl -u yanlv -f
```

### 更新代码

```bash
cd /var/www/yanlv
git pull
systemctl restart yanlv
```

### 查看资源使用

```bash
# 安装htop
apt install htop

# 查看系统资源
htop

# 查看进程
ps aux | grep python
```

---

## 故障排除

### 问题1：服务无法启动

```bash
# 查看详细错误
journalctl -u yanlv -n 100

# 手动启动测试
cd /var/www/yanlv/playground
source ../venv/bin/activate
python server.py
```

### 问题2：端口被占用

```bash
# 查看端口占用
netstat -tulpn | grep 5000

# 杀掉占用进程
kill -9 <PID>
```

### 问题3：无法访问

```bash
# 检查防火墙
ufw status

# 开放端口
ufw allow 5000
ufw allow 80

# 检查服务
systemctl status yanlv
systemctl status nginx
```

### 问题4：依赖安装失败

```bash
# 更新pip
pip install --upgrade pip

# 重新安装依赖
cd /var/www/yanlv/playground
pip install -r requirements.txt --force-reinstall
```

---

## 访问地址

部署成功后，可以通过以下地址访问：

- **直接访问：** http://192.168.1.12:5000
- **通过Nginx：** http://192.168.1.12

---

## 下一步

部署完成后，您可以：

1. ✅ 在浏览器中访问 http://192.168.1.12
2. ✅ 测试运行言律语言代码
3. ✅ 查看API文档
4. ✅ 配置域名（可选）
5. ✅ 配置SSL证书（可选）

---

## 需要帮助？

如果部署过程中遇到问题：

1. 查看日志：`journalctl -u yanlv -n 100`
2. 检查服务：`systemctl status yanlv`
3. 测试端口：`netstat -tulpn | grep 5000`
4. 手动测试：`python server.py`

---

**祝部署顺利！** 🚀
