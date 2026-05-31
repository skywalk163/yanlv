# 言律语言 Racket 版 - 正确使用方法

## ✅ 正确的运行方式

### 方法1：使用命令行运行器（推荐）

```powershell
# 在 PowerShell 中
cd G:\dumategithub\yanlv

# 运行示例文件
& "E:\Program Files\Racket\Racket.exe" yanlv.rkt hello.yan
```

### 方法2：如果 Racket 在 PATH 中

```powershell
racket yanlv.rkt hello.yan
```

### 方法3：查看帮助

```powershell
racket yanlv.rkt
```

会显示：
```
╔══════════════════════════════════════╗
║   言律语言高级语法执行器 v3.0      ║
╚══════════════════════════════════════╝

用法: racket yanlv.rkt <文件名.yan>

示例:
  racket yanlv.rkt quick_start.yan
  racket yanlv.rkt test_advanced.yan

可用文件:
  - quick_start.yan      快速开始示例
  - test_advanced.yan    高级语法测试
  - test_complete.yan    完整测试套件
```

---

## 🎯 成功运行示例

### 示例1：基础输出

创建 `hello.yan`：
```言律
# 输出字符串
输出 "你好世界"

# 定义数字变量
定 年龄 是 25
输出 年龄

# 算术运算
定 a 是 10
定 b 是 3
输出 a 加 b
```

运行：
```powershell
racket yanlv.rkt hello.yan
```

输出：
```
╔══════════════════════════════════════╗
║   言律语言高级语法执行器 v3.0      ║
╚══════════════════════════════════════╝

📄 文件: hello.yan

⚡ 执行结果:
─────────────────────────────────────
你好世界
25
13

✅ 执行完成
```

---

## 📝 语法规则

### 1. 字符串必须用引号

```言律
# ✅ 正确
输出 "你好世界"
定 名字 是 "张三"

# ❌ 错误
输出 你好世界
定 名字 是 张三
```

### 2. 关键词之间需要空格

```言律
# ✅ 正确
定 年龄 是 25
输出 年龄

# ❌ 错误
定年龄是25
输出年龄
```

### 3. 因果链用句号结束

```言律
# ✅ 正确
分数 大于 80，输出 "良好"。

# ❌ 错误
分数 大于 80，输出 "良好"
```

---

## 🚀 快速测试

### 测试1：基础功能

```powershell
racket yanlv.rkt hello.yan
```

### 测试2：高级语法

```powershell
racket yanlv.rkt test_advanced.yan
```

---

## 💡 常见问题

### Q: PowerShell 报错 "Unexpected token"

**A:** 在 PowerShell 中，需要用 `&` 执行带路径的程序：

```powershell
# ✅ 正确
& "E:\Program Files\Racket\Racket.exe" yanlv.rkt hello.yan

# ❌ 错误
"E:\Program Files\Racket\Racket.exe" yanlv.rkt hello.yan
```

### Q: 提示 "undefined identifier"

**A:** 字符串需要用引号：

```言律
# ✅ 正确
定 名字 是 "张三"

# ❌ 错误
定 名字 是 张三
```

### Q: 解析结果不正确

**A:** 确保关键词之间有空格：

```言律
# ✅ 正确
定 年龄 是 25

# ❌ 错误
定年龄是25
```

---

## 📚 下一步

1. **运行更多示例**
   ```powershell
   racket yanlv.rkt hello.yan
   ```

2. **创建自己的程序**
   - 创建新文件 `my_program.yan`
   - 编写言律代码
   - 运行 `racket yanlv.rkt my_program.yan`

3. **学习更多语法**
   - 查看 README_RACKET.md
   - 查看 USAGE_GUIDE.md

---

## 🎉 开始编程吧！

现在你已经知道如何正确使用言律语言了！

```powershell
# 运行你的第一个程序
racket yanlv.rkt hello.yan
```

**祝你编程愉快！** 🚀
