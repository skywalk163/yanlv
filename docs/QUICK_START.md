# 言律语言 Racket 版 - 快速使用指南

## 🚀 正确的运行方法

### 方法1：使用 Racket 直接运行（推荐）

在 PowerShell 中：

```powershell
# 进入项目目录
cd G:\dumategithub\yanlv

# 运行程序
& "E:\Program Files\Racket\Racket.exe" run_advanced.rkt
```

**注意：** 在 PowerShell 中，需要使用 `&` 来执行带路径的可执行文件。

### 方法2：如果 Racket 在 PATH 中

```powershell
# 如果已添加到 PATH
racket run_advanced.rkt
```

### 方法3：使用批处理脚本

```powershell
# Windows 批处理
.\run_yanlv.bat quick_start.yan
```

---

## 🔧 修改运行器以支持命令行参数

让我创建一个改进的运行器，支持指定文件名：
