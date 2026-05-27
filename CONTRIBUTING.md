# 贡献指南

感谢您对言律编程语言的关注！我们欢迎任何形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发设置](#开发设置)
- [提交规范](#提交规范)
- [代码风格](#代码风格)
- [测试](#测试)
- [文档](#文档)

## 行为准则

本项目采用贡献者公约作为行为准则。参与本项目即表示您同意遵守其条款。请阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 了解详情。

## 如何贡献

### 报告Bug

如果您发现了bug，请创建一个Issue，包含：

1. **清晰的标题** - 简明扼要地描述问题
2. **详细描述** - 包含重现步骤
3. **预期行为** - 您期望发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息** - Python版本、操作系统等
6. **代码示例** - 如果可能，提供最小重现示例

### 建议新功能

如果您有新功能的建议，请创建一个Issue，包含：

1. **清晰的标题** - 描述建议的功能
2. **详细描述** - 功能的详细说明
3. **使用场景** - 为什么需要这个功能
4. **示例代码** - 如果可能，展示如何使用

### 提交代码

1. **Fork仓库**
   ```bash
   git clone https://github.com/your-username/yanlv.git
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行更改**
   - 编写代码
   - 添加测试
   - 更新文档

4. **运行测试**
   ```bash
   pytest tests/
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加某个特性"
   ```

6. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 填写PR模板
   - 等待审核

## 开发设置

### 环境要求

- Python 3.8+
- pip
- git

### 安装开发环境

```bash
# 克隆仓库
git clone https://github.com/yanlv/yanlv.git
cd yanlv

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装项目
pip install -e .
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_lexer.py

# 运行测试并生成覆盖率报告
pytest --cov=yanlv
```

## 提交规范

我们使用 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范：

### 提交格式

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(lexer): 添加新的关键字支持

添加了"异步"和"等待"关键字，支持异步编程。

Closes #123
```

## 代码风格

### Python代码

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- 使用4空格缩进
- 最大行长度：100字符
- 使用类型提示

### 代码检查

```bash
# 使用flake8检查
flake8 src/yanlv/

# 使用black格式化
black src/yanlv/

# 使用isort排序导入
isort src/yanlv/
```

## 测试

### 测试要求

- 所有新功能必须添加测试
- Bug修复必须添加回归测试
- 测试覆盖率不低于80%

### 测试结构

```
tests/
├── test_lexer.py          # 词法分析器测试
├── test_parser.py         # 语法分析器测试
├── test_interpreter.py    # 解释器测试
├── test_stdlib.py         # 标准库测试
└── ...
```

### 编写测试

```python
import unittest

class TestFeature(unittest.TestCase):
    def test_basic(self):
        """测试基本功能"""
        # 准备
        input_data = "..."
        
        # 执行
        result = function(input_data)
        
        # 断言
        self.assertEqual(result, expected)
```

## 文档

### 文档要求

- 所有公共API必须有文档字符串
- 使用中文编写文档
- 包含使用示例

### 文档字符串格式

```python
def function(param1, param2):
    """
    函数描述
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
    
    Returns:
        返回值说明
    
    Raises:
        Exception: 异常说明
    
    Example:
        >>> function(1, 2)
        3
    """
    pass
```

## 发布流程

### 版本号

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- MAJOR: 不兼容的API修改
- MINOR: 向下兼容的功能新增
- PATCH: 向下兼容的问题修正

### 发布步骤

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建git标签
4. 构建发布包
5. 发布到PyPI

## 获取帮助

- **文档**: https://yanlv.org/docs
- **Issues**: https://github.com/yanlv/yanlv/issues
- **讨论**: https://github.com/yanlv/yanlv/discussions

## 许可证

通过贡献代码，您同意您的代码将在MIT许可证下授权。

---

再次感谢您的贡献！🎉
