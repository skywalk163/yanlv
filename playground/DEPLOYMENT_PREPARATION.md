# 言律语言 Playground 部署指南

## 部署前准备工作清单

### 1. 云服务器准备

#### 1.1 选择云服务商

推荐选项：
- **华为云** - 国内访问快，稳定性好
- **阿里云** - 生态完善，文档丰富
- **腾讯云** - 性价比高
- **Railway/Render** - 免费部署选项

#### 1.2 服务器配置要求

**最低配置：**
- CPU: 1核
- 内存: 1GB
- 硬盘: 10GB
- 带宽: 1Mbps

**推荐配置：**
- CPU: 2核
- 内存: 2GB
- 硬盘: 20GB
- 带宽: 5Mbps

#### 1.3 操作系统

推荐：
- Ubuntu 20.04/22.04 LTS
- CentOS 7/8
- Debian 11

---

### 2. 域名准备（可选但推荐）

#### 2.1 购买域名

- 国内：阿里云、腾讯云、华为云
- 国外：GoDaddy、Namecheap

#### 2.2 域名备案（国内服务器必须）

- 准备材料：
  - 身份证正反面照片
  - 网站备案信息
  - 服务器购买凭证
- 备案时间：7-20个工作日

#### 2.3 域名解析

配置DNS解析：
```
类型: A记录
主机记录: playground (或 @)
记录值: 服务器IP地址
TTL: 600
```

---

### 3. SSL证书准备（推荐）

#### 3.1 免费证书

- **Let's Encrypt** - 免费，自动续期
- **阿里云/腾讯云免费证书** - 1年有效期

#### 3.2 证书申请

使用Certbot自动申请：
```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d your-domain.com
```

---

### 4. 代码准备

#### 4.1 检查依赖

确保 `playground/requirements.txt` 完整：
```txt
flask>=2.0.0
flask-cors>=3.0.0
jieba>=0.42.0
gunicorn>=20.0.0  # 生产服务器
gevent>=21.0.0    # 异步支持
```

#### 4.2 环境变量配置

创建 `.env` 文件：
```bash
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
PORT=5000
HOST=0.0.0.0
```

#### 4.3 安全检查

- [ ] 移除调试模式
- [ ] 设置强密钥
- [ ] 配置CORS白名单
- [ ] 添加访问频率限制

---

### 5. 数据库准备（可选）

如果需要持久化数据：

#### 5.1 选择数据库

- **SQLite** - 轻量级，适合小型应用
- **PostgreSQL** - 功能强大，推荐
- **MySQL** - 流行，生态好

#### 5.2 数据库配置

```python
# config.py
DATABASE_URL = "postgresql://user:password@localhost/yanlv"
```

---

### 6. 监控和日志

#### 6.1 日志配置

```python
# logging配置
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yanlv.log'),
        logging.StreamHandler()
    ]
)
```

#### 6.2 监控工具

推荐：
- **Prometheus + Grafana** - 开源监控方案
- **Sentry** - 错误追踪
- **华为云/阿里云监控** - 云服务商监控

---

### 7. CI/CD配置

#### 7.1 自动化部署

创建 `.github/workflows/deploy.yml`：
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/yanlv
            git pull
            pip install -r requirements.txt
            sudo systemctl restart yanlv
```

---

### 8. 成本估算

#### 8.1 云服务器成本

| 配置 | 华为云 | 阿里云 | 腾讯云 |
|------|--------|--------|--------|
| 1核1G | ¥50/月 | ¥60/月 | ¥40/月 |
| 2核2G | ¥100/月 | ¥120/月 | ¥80/月 |
| 2核4G | ¥200/月 | ¥240/月 | ¥160/月 |

#### 8.2 其他成本

- 域名：¥50-100/年
- SSL证书：免费
- 带宽：¥0.8/GB（按流量计费）

**最低成本：约¥50-100/月**

---

### 9. 部署前检查清单

#### 必须完成：

- [ ] 购买云服务器
- [ ] 配置服务器安全组（开放80、443、5000端口）
- [ ] 安装Python 3.8+
- [ ] 安装依赖包
- [ ] 配置防火墙
- [ ] 设置系统服务自动启动

#### 推荐完成：

- [ ] 购买域名
- [ ] 完成域名备案（国内）
- [ ] 申请SSL证书
- [ ] 配置HTTPS
- [ ] 设置监控告警
- [ ] 配置自动备份

---

### 10. 快速部署方案

#### 方案A：传统部署（推荐新手）

1. 购买云服务器
2. SSH连接服务器
3. 安装依赖
4. 运行应用

**优点：** 简单直接，易于调试
**缺点：** 需要手动维护

#### 方案B：Docker部署（推荐）

1. 创建Docker镜像
2. 推送到镜像仓库
3. 在服务器上运行容器

**优点：** 环境一致，易于迁移
**缺点：** 需要学习Docker

#### 方案C：Serverless部署（免费）

使用Railway、Render、Vercel等平台

**优点：** 免费，自动扩展
**缺点：** 有使用限制

---

### 11. 部署时间估算

| 任务 | 时间 |
|------|------|
| 购买服务器 | 10分钟 |
| 配置服务器 | 30分钟 |
| 安装依赖 | 20分钟 |
| 部署应用 | 30分钟 |
| 域名配置 | 1小时 |
| SSL配置 | 30分钟 |
| 测试验证 | 1小时 |

**总计：约3-4小时**（不含备案时间）

---

### 12. 下一步行动

#### 立即可做：

1. **选择云服务商** - 根据预算和需求选择
2. **注册账号** - 完成实名认证
3. **准备域名** - 购买并备案（如需要）

#### 部署时做：

1. 购买服务器
2. 配置环境
3. 部署应用
4. 配置域名和SSL
5. 测试验证

---

### 13. 常见问题

**Q: 必须要域名吗？**
A: 不必须，可以直接用IP访问。但域名更专业，便于记忆。

**Q: 必须要SSL吗？**
A: 不必须，但推荐。HTTPS更安全，浏览器不会警告。

**Q: 国内服务器必须备案吗？**
A: 是的，使用国内服务器必须完成ICP备案，否则会被封禁。

**Q: 有免费部署方案吗？**
A: 有，可以使用Railway、Render等平台，有免费额度。

---

### 14. 推荐部署流程

**对于个人/学习项目：**
```
Railway/Render免费部署 → 测试验证 → 如需稳定再购买服务器
```

**对于正式/商业项目：**
```
购买域名 → 购买服务器 → 备案 → 部署 → 配置SSL → 上线
```

---

## 准备好了吗？

完成以上准备工作后，就可以开始部署了！

详细部署步骤请查看：[DEPLOYMENT_STEPS.md](./DEPLOYMENT_STEPS.md)

---

**需要帮助？**
- 查看文档：[README.md](./README.md)
- 提交问题：[GitCode Issues](https://gitcode.com/skywalk163/yanlv/issues)
