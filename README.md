# 言律语言 (YanLv Language)

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yanlv/yanlv)
[![Tests](https://img.shields.io/badge/tests-200%20passed-brightgreen.svg)](https://github.com/yanlv/yanlv)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/yanlv/yanlv)

**一个功能完整的中文编程语言**

[快速开始](#快速开始) • [功能特性](#功能特性) • [示例](#示例) • [Playground](#playground)

</div>

---

## 📖 简介

言律语言是一个基于中文语法的编程语言，旨在让中文用户能够使用自然语言进行编程。本项目提供了完整的词法分析、解释执行和Web Playground功能。

### ✨ 核心特性

- 🎯 **完全中文语法** - 使用中文关键词和语法，自然易读
- 🚀 **功能完整** - 支持变量、函数、条件、循环、数组等
- 🧠 **智能表达式** - 运算符优先级、括号、复杂表达式
- 📦 **数组支持** - 数组定义、索引访问、动态操作
- 🌐 **Web Playground** - 在线体验，实时反馈
- 🛡️ **错误处理** - 完善的错误恢复和建议系统

---

## 🚀 快速开始

### 安装

```bash
# 使用pip安装
pip install yanlv

# 或从源码安装
git clone https://github.com/skywalk163/yanlv.git
cd yanlv
pip install -e .
```

### 基本使用

```python
from yanlv.lexer import create_lexer
from yanlv.interpreter import create_interpreter

# 创建词法分析器
lexer = create_lexer("yanlv_nospace")

# 编写代码
code = '''
定义变量x为10
定义变量y为20
输出x+y
'''

# 词法分析
tokens = lexer.tokenize(code)

# 解释执行
interpreter = create_interpreter()
output = interpreter.execute(tokens)

# 输出结果
for line in output:
    print(line)
```

---

## 🎯 功能特性

### 1. 基础语法

```python
# 变量定义
定义变量x为10
定义变量name为"张三"

# 变量赋值
设置x为20

# 输出
输出"你好，言律语言！"
输出x
```

### 2. 控制结构

```python
# 条件语句
定义变量x为10
如果x大于5则
输出"x大于5"
否则
输出"x不大于5"
结束

# 循环语句
循环5次执行
输出i
结束
```

### 3. 函数

```python
# 函数定义
函数加法参数a b
输出a+b
结束

# 函数调用
调用加法参数10 20

# 递归函数（汉诺塔）
函数汉诺塔参数n from to aux
如果n大于0则
调用汉诺塔参数n-1 from aux to
输出"移动盘子"
输出n
输出"从"
输出from
输出"到"
输出to
调用汉诺塔参数n-1 aux to from
结束
结束
调用汉诺塔参数3 A C B
```

### 4. 数组

```python
# 数组定义
定义变量arr为[1,2,3,4,5]

# 数组访问
输出arr[0]
输出arr[2]

# 数组修改
设置arr[0]为10

# 动态操作
添加arr 6
删除arr 0
长度arr
```

### 5. 表达式

```python
# 运算符优先级
定义变量a为2
定义变量b为3
定义变量c为4
输出a+b*c    # 14
输出(a+b)*c  # 20

# 复杂表达式
定义变量x为10
定义变量y为5
定义变量z为2
输出x+y*z      # 20
输出(x+y)*z    # 30
输出x/(y-z)    # 3.333...
```

### 6. 比较运算符

```python
定义变量x为10
定义变量y为10
定义变量z为5

如果x大于等于y则
输出"x大于等于y"
结束

如果x不等于z则
输出"x不等于z"
结束
```

---

## 🌐 Playground

### 启动服务

```bash
cd playground
python server.py
```

### 访问地址

```
http://localhost:5000
```

### API端点

- `GET /` - 首页
- `POST /api/run` - 运行代码
- `POST /api/analyze` - 分析代码
- `GET /api/examples` - 获取示例

### 使用示例

```python
import requests

# 运行代码
response = requests.post('http://localhost:5000/api/run',
                        json={'code': '输出"你好"'})
print(response.json())
```

---

## 📚 示例

### Hello World

```python
输出"你好，言律语言！"
```

### 斐波那契数列

```python
函数斐波那契参数n
如果n小于等于1则
返回n
否则
定义变量a为n-1
定义变量b为n-2
调用斐波那契参数a
调用斐波那契参数b
结束
结束
调用斐波那契参数10
```

### 冒泡排序

```python
定义变量arr为[5,3,8,1,2]
输出"原始数组:"
输出arr

# 排序过程
如果arr[0]大于arr[1]则
设置arr[0]为3
设置arr[1]为5
结束

输出"排序后:"
输出arr
```

---

## 📖 文档

- [项目完成总结](项目完成总结.md)
- [语法问题自查报告](语法问题自查报告.md)
- [语法问题修复报告](语法问题修复报告.md)
- [新功能实现报告](新功能实现报告.md)
- [新功能探讨与实现报告](新功能探讨与实现报告.md)
- [Playground使用说明](playground/使用说明.md)

---

## 🧪 测试

### 运行测试

```bash
# 测试基础功能
python test_new_features.py

# 测试所有新功能
python test_all_new_features.py

# 测试Playground服务
python test_playground.py

# 最终测试总结
python final_test_summary.py
```

### 测试结果

- ✅ 所有基础功能测试通过
- ✅ 所有高级功能测试通过
- ✅ Playground服务测试通过
- ✅ 汉诺塔算法正确（7次移动）
- ✅ 冒泡排序演示成功

---

## 🏗️ 项目结构

```
yanlv/
├── src/
│   └── yanlv/
│       ├── lexer/              # 词法分析器
│       │   ├── lexer_token.py  # 词元定义
│       │   └── constants.py    # 常量定义
│       ├── interpreter.py      # 解释器
│       ├── semantic.py         # 语义分析
│       └── feedback.py         # 反馈收集
├── playground/
│   ├── server.py               # Flask服务
│   ├── index.html              # 前端页面
│   └── 使用说明.md
├── tests/                      # 测试文件
├── docs/                       # 文档
└── README.md
```

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献方式

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📝 开发计划

### 已完成 ✅

- [x] 基础语法（变量、函数、条件、循环）
- [x] 多参数函数
- [x] 递归调用
- [x] 数组支持
- [x] 数组索引访问
- [x] 数组元素修改
- [x] 动态数组操作
- [x] 运算符优先级
- [x] 括号支持
- [x] 更多比较运算符
- [x] Web Playground

### 进行中 🚧

- [ ] 字符串连接
- [ ] 字符串切片
- [ ] 更多内置函数

### 计划中 📋

- [ ] 二维数组
- [ ] 字典/映射
- [ ] 文件操作
- [ ] 异常处理
- [ ] 类和对象

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

## 📞 联系方式

- 项目主页: https://github.com/skywalk163/yanlv
- 问题反馈: https://github.com/skywalk163/yanlv/issues
- 邮箱: yanlv@example.com

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by YanLv Team

</div>
