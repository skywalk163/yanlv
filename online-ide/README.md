# 言律在线IDE

一个基于Web的言律编程语言在线开发环境。

## 功能特性

- ✅ 代码编辑器
- ✅ 实时运行
- ✅ 代码编译（Python/JavaScript）
- ✅ 示例代码
- ✅ 语法高亮
- ✅ 键盘快捷键

## 使用方法

### 本地运行

1. 克隆仓库
```bash
git clone https://github.com/yanlv/yanlv.git
cd yanlv/online-ide
```

2. 启动本地服务器
```bash
# 使用Python
python -m http.server 8080

# 或使用Node.js
npx serve
```

3. 打开浏览器访问
```
http://localhost:8080
```

### 直接使用

直接在浏览器中打开 `index.html` 文件即可使用。

## 快捷键

- `Ctrl + Enter` - 运行代码
- `Tab` - 插入空格

## 功能说明

### 运行代码

点击"运行"按钮或按 `Ctrl+Enter`，将执行编辑器中的言律代码。

### 编译代码

1. 选择目标语言（Python或JavaScript）
2. 点击"编译"按钮
3. 查看编译结果
4. 点击"复制"按钮复制生成的代码

### 示例代码

点击"示例"按钮，选择预置的示例代码：
- Hello World
- 变量定义
- 循环示例
- 函数示例
- 数组操作
- 斐波那契

## 技术栈

- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **JavaScript** - 交互逻辑

## 浏览器支持

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 后续计划

- [ ] 集成真实编译器
- [ ] 添加语法高亮
- [ ] 添加自动补全
- [ ] 添加错误提示
- [ ] 添加文件管理
- [ ] 添加代码分享
- [ ] 添加主题切换

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT
