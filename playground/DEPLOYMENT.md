# Playground 部署指南

## 更新内容

### 1. 添加首页路由 ✅
- 访问 `http://localhost:5000/` 现在会返回 HTML 页面
- 如果没有 HTML 文件，返回 API 信息 JSON

### 2. 创建前端页面 ✅
- `index.html` - 完整的 Web IDE 界面
- 支持代码编辑、运行、分析
- 提供示例代码
- 显示词元和统计信息

## 使用方法

### 启动服务器

```bash
# Ubuntu
cd /var/www/yanlv/playground
python3 server.py

# Windows
cd g:\dumategithub\yanlv\playground
python server.py
```

### 访问 Playground

打开浏览器访问: http://localhost:5000

## API 端点

### 1. 首页
```
GET /
```
返回 HTML 页面或 API 信息

### 2. 运行代码
```
POST /api/run
Content-Type: application/json

{
  "code": "输出 '你好'"
}
```

响应:
```json
{
  "success": true,
  "output": "=> 你好",
  "stats": {
    "tokens": 3,
    "lines": 1,
    "exec_time": 1.23,
    "variables": 0
  }
}
```

### 3. 分析代码
```
POST /api/analyze
Content-Type: application/json

{
  "code": "输出 \"测试\""
}
```

响应:
```json
{
  "success": true,
  "tokens": [
    {
      "type": "IDENTIFIER",
      "value": "输出",
      "line": 0,
      "column": 0
    },
    {
      "type": "STRING",
      "value": "\"测试\"",
      "line": 0,
      "column": 0
    },
    {
      "type": "EOF",
      "value": "",
      "line": 0,
      "column": 0
    }
  ],
  "total_tokens": 3
}
```

### 4. 获取示例
```
GET /api/examples
```

响应:
```json
{
  "success": true,
  "examples": [
    {
      "name": "输出语句",
      "code": "输出 'Hello, 言律语言！'\n输出 '这是一个中文编程语言'"
    },
    ...
  ]
}
```

### 5. 提交反馈
```
POST /api/feedback
Content-Type: application/json

{
  "segment": "输出",
  "system": "OUTPUT",
  "user": "PRINT"
}
```

### 6. 获取统计
```
GET /api/stats
```

## 测试 API

### 使用 curl

```bash
# 测试首页
curl http://localhost:5000/

# 运行代码
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{"code": "输出 \"测试\""}'

# 分析代码
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "输出 \"测试\""}'

# 获取示例
curl http://localhost:5000/api/examples
```

### 使用浏览器

直接访问 http://localhost:5000 使用 Web IDE

## 前端功能

### 代码编辑器
- 语法高亮（计划中）
- 行号显示（计划中）
- 自动补全（计划中）

### 运行功能
- 执行代码
- 显示输出
- 统计信息

### 分析功能
- 词法分析
- 词元列表
- 类型标注

### 示例代码
- 输出语句
- 变量定义
- 条件语句
- 循环语句
- 函数定义

## 部署到生产环境

### 使用 Gunicorn (Ubuntu)

```bash
# 安装 Gunicorn
pip3 install gunicorn

# 启动服务
cd /var/www/yanlv/playground
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name yanlv.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 使用 systemd 服务

创建 `/etc/systemd/system/yanlv.service`:

```ini
[Unit]
Description=YanLv Playground
After=network.target

[Service]
User=skywalk
WorkingDirectory=/var/www/yanlv/playground
ExecStart=/usr/bin/python3 server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl start yanlv
sudo systemctl enable yanlv
```

## 故障排除

### 问题1: 404 Not Found
**原因**: 缺少首页路由
**解决**: 已添加首页路由，更新 server.py

### 问题2: ModuleNotFoundError
**原因**: 缺少依赖
**解决**:
```bash
pip3 install jieba typing-extensions flask flask-cors
```

### 问题3: 端口被占用
**解决**:
```bash
# 查找占用端口的进程
lsof -i :5000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
python3 server.py --port 5001
```

## 下一步

1. ✅ 添加首页路由
2. ✅ 创建前端页面
3. 🔄 添加语法高亮
4. 🔄 添加自动补全
5. 🔄 添加错误提示
6. 🔄 添加代码保存功能

## 文件结构

```
playground/
├── server.py          # 后端服务
├── index.html         # 前端页面
├── requirements.txt   # 依赖列表
└── DEPLOYMENT.md      # 本文档
```
