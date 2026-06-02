# 言律语言 (Yanlv Language)

> 中文原生编程语言，让编程像说话一样自然

---

## 🚀 快速开始

### Python版本

```bash
# 安装
pip install yanlv

# 运行
yanlv 运行 hello.yan
```

### Racket版本

```powershell
# 运行
racket racket/yanlv_import.rkt hello.yan

# 交互模式
racket racket/yanlv_repl.rkt

# Web界面
racket racket/yanlv_playground.rkt
```

---

## 📝 示例代码

```言律
# 变量定义
定义变量赵为10
定义变量钱为20

# 输出
输出 赵加钱

# 条件判断
赵 大于 5，输出 "大于5"。

# 宏定义
定义宏 双倍(赵) 为 赵加赵
输出 双倍(赵)

# 导入库
导入 "libraries/math_library.yan"
输出 圆周率
```

---

## ✨ 特性

- ✅ **中文语法** - 完全使用中文编程
- ✅ **百家姓变量** - 使用姓氏作为变量名
- ✅ **宏系统** - 强大的宏定义和展开
- ✅ **导入导出** - 模块化编程
- ✅ **交互模式** - REPL实时执行
- ✅ **Web界面** - Playground在线编程

---

## 📚 文档

- [为什么选择言律](docs/WHY_YANLV.md)
- [Racket版本进度](docs/RACKET_PROGRESS.md)
- [宏系统说明](docs/MACRO_FINAL_SUMMARY.md)
- [导入库功能](docs/IMPORT_COMPLETE.md)
- [函数调用语法](docs/FUNCTION_CALL_COMPLETE.md)

---

## 📁 目录结构

```
yanlv/
├── docs/        # 文档
├── examples/    # 示例
├── libraries/   # 库文件
├── racket/      # Racket实现
├── src/         # Python实现
├── tests/       # 测试
└── tools/       # 工具
```

详见 [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)

---

## 🧪 测试

```bash
# Python测试
pytest tests/

# Racket测试
racket racket/yanlv_import.rkt tests/test_stable.yan
```

---

## 📦 版本

- **Python版本** - 完整实现，所有功能
- **Racket版本** - 核心功能，性能优秀

---

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议！

---

## 📄 许可证

MIT License

---

**让编程像说话一样自然！** 🎯
