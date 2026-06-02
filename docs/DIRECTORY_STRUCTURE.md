# 言律语言项目目录结构

## 📁 目录说明

```
yanlv/
├── .github/              # GitHub配置
├── docs/                 # 文档
│   ├── *.md             # Markdown文档
│   └── *.txt            # 文本文档
├── examples/             # 示例代码
│   └── *.yan            # 言律示例程序
├── libraries/            # 库文件
│   └── *.yan            # 言律库文件
├── racket/               # Racket实现
│   ├── yanlv_import.rkt # 导入导出版（推荐）
│   ├── yanlv_macro.rkt  # 宏系统版
│   ├── yanlv_surname.rkt# 百家姓版
│   ├── yanlv_enhanced.rkt# 增强版
│   ├── yanlv_repl.rkt   # 交互模式
│   ├── yanlv_playground.rkt# Web界面
│   └── yanlv_reader_*.rkt# 读取器
├── src/                  # Python源码
│   └── yanlv/           # 主要实现
├── stdlib/               # 标准库
├── tests/                # 测试文件
│   ├── test_*.py        # Python测试
│   └── test_*.yan       # 言律测试
├── tools/                # 工具脚本
│   └── *.py             # 辅助工具
├── .gitignore           # Git忽略配置
├── hello.yan            # 快速开始示例
├── quick_start.yan      # 快速开始
└── README.md            # 项目说明
```

---

## 🚀 快速开始

### 运行示例

**Python版本:**
```bash
yanlv 运行 hello.yan
```

**Racket版本:**
```powershell
racket racket/yanlv_import.rkt hello.yan
```

---

## 📚 文档

所有文档位于 `docs/` 目录：

- `WHY_YANLV.md` - 为什么选择言律
- `RACKET_PROGRESS.md` - Racket版本进度
- `MACRO_FINAL_SUMMARY.md` - 宏系统总结
- `IMPORT_COMPLETE.md` - 导入库总结
- `FUNCTION_CALL_COMPLETE.md` - 函数调用总结

---

## 🧪 测试

所有测试位于 `tests/` 目录：

**运行测试:**
```bash
pytest tests/
```

---

## 📦 库文件

所有库文件位于 `libraries/` 目录：

**使用库:**
```言律
导入 "libraries/math_library.yan"
```

---

## 🔧 Racket版本

所有Racket实现位于 `racket/` 目录：

**推荐使用:**
- `yanlv_import.rkt` - 导入导出版（最新）
- `yanlv_macro.rkt` - 宏系统版
- `yanlv_repl.rkt` - 交互模式
- `yanlv_playground.rkt` - Web界面

---

## 🛠️ 工具

所有工具脚本位于 `tools/` 目录：

- 分析工具
- 验证工具
- 转换工具

---

## 📝 示例

所有示例代码位于 `examples/` 目录：

- 基础示例
- 高级示例
- 实用示例

---

## 🎯 目录整理原则

1. **根目录保持简洁** - 只保留核心配置文件
2. **文档集中管理** - 所有文档在 `docs/`
3. **测试独立目录** - 所有测试在 `tests/`
4. **实现分离** - Python在 `src/`，Racket在 `racket/`
5. **库文件统一** - 所有库在 `libraries/`

---

## 📊 文件统计

- **文档:** `docs/` 目录
- **测试:** `tests/` 目录
- **Racket实现:** `racket/` 目录
- **Python实现:** `src/` 目录
- **库文件:** `libraries/` 目录
- **示例:** `examples/` 目录

---

**目录结构清晰，便于维护和使用！** 🎯
