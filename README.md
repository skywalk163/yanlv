# 言律编程语言

<div align="center">

![言律Logo](https://img.shields.io/badge/言律-中文编程语言-blue)

[![GitHub Stars](https://img.shields.io/github/stars/yanlv/yanlv.svg)](https://github.com/yanlv/yanlv/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/yanlv/yanlv.svg)](https://github.com/yanlv/yanlv/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)

**用中文思考，用中文编程**

[在线体验](https://yanlv.org/playground) | [文档](https://yanlv.org/docs) | [示例](https://yanlv.org/examples) | [贡献指南](CONTRIBUTING.md)

</div>

---

## 📖 简介

言律是一门创新的中文编程语言，让每个中文用户都能用母语自然地表达编程思想。

### 核心特性

- 🇨🇳 **中文优先** - 完全使用中文关键字和语法
- 🔗 **因果链语法** - 用自然语言描述事件和响应关系
- 🔄 **状态流语法** - 直观的状态机定义
- 🎯 **意合式调用** - 智能参数推断
- 🛤️ **多轨制支持** - 嵌入Python、JavaScript、SQL代码
- ⚡ **高性能** - 优化的编译器和运行时

## 🚀 快速开始

### 安装

```bash
pip install yanlv
```

### Hello World

创建文件 `hello.yan`：

```yan
输出"你好，世界！"
```

运行：

```bash
yanlv run hello.yan
```

### 更多示例

```yan
// 变量定义
定义变量x为10
定义变量y为20

// 条件语句 - 使用缩进语法
如果x大于y则
    输出"x大于y"
否则
    输出"y大于等于x"

// 循环 - 使用缩进语法
循环5次执行
    输出i

// 函数 - 使用缩进语法
函数加法参数a b
    返回a加b

输出调用加法参数10 20  // 30
```

### 🎯 语法特性

言律语言采用**Python风格的缩进语法**,无需"结束"关键字:

```yan
// ✅ 推荐: 使用缩进
循环3次执行
    输出"hello"
    定义变量x为10
    输出x

// ❌ 已废弃: 使用"结束"关键字
循环3次执行
    输出"hello"
结束  // 不再需要
```

**优势:**
- 代码更简洁(减少20-30%代码量)
- 学习成本低(与Python一致)
- 强制良好的代码风格
- 现代编辑器自动支持

## 📚 文档

- [教程](docs/教程.md) - 从入门到精通
- [API文档](docs/API文档.md) - 完整API参考
- [示例代码](docs/示例代码.md) - 30+实用示例

## 🛠️ 工具链

- **VS Code插件** - 语法高亮、自动补全、错误诊断
- **在线IDE** - 无需安装，在线编写和运行
- **包管理器** - 安装、发布和管理依赖包

## 📊 项目状态

| 模块 | 完成度 | 状态 |
|------|--------|------|
| 词法分析器 | 95% | ✅ |
| 语法分析器 | 90% | ✅ |
| 解释器 | 85% | ✅ |
| 编译器 | 85% | ✅ |
| VS Code插件 | 90% | ✅ |
| 多轨制 | 90% | ✅ |
| 标准库 | 80% | ✅ |
| 测试覆盖率 | 80% | ✅ |

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

### 贡献方式

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有贡献者的支持！

## 📞 联系方式

- **官网**: https://yanlv.org
- **GitHub**: https://github.com/yanlv/yanlv
- **Issues**: https://github.com/yanlv/yanlv/issues

---

<div align="center">

**用中文思考，用中文编程**

Made with ❤️ by 言律团队

</div>
