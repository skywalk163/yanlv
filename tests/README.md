# 言律语言测试文档

## 测试体系概述

言律语言采用分层测试策略，包括：

1. **单元测试** - 测试单个组件的功能
2. **集成测试** - 测试组件之间的协作
3. **示例测试** - 测试示例文件的执行

## 测试目录结构

```
yanlv/
├── tests/
│   ├── unit/              # 单元测试
│   │   ├── test_lexer.py       # 词法分析器测试
│   │   └── test_interpreter.py # 解释器测试
│   └── integration/       # 集成测试
│       └── test_examples.py    # 示例文件测试
├── run_tests.py           # 测试运行脚本
└── .github/
    └── workflows/
        └── ci.yml         # CI配置
```

## 运行测试

### 运行所有测试

```bash
python run_tests.py
```

### 只运行单元测试

```bash
python run_tests.py unit
```

### 只运行集成测试

```bash
python run_tests.py integration
```

### 运行特定测试文件

```bash
python -m pytest tests/unit/test_lexer.py -v
python -m unittest tests.unit.test_lexer
```

## 测试覆盖范围

### 单元测试

#### 词法分析器测试 (`test_lexer.py`)

- ✅ 简单输出语句
- ✅ 变量定义
- ✅ 字符串字面量
- ✅ 条件语句
- ✅ 循环语句
- ✅ 函数定义
- ✅ 数组定义
- ✅ 多行代码
- ✅ 因果链语法
- ✅ 高级定义语法
- ✅ 主题块语法

#### 解释器测试 (`test_interpreter.py`)

- ✅ 简单输出
- ✅ 变量定义
- ✅ 算术运算
- ✅ 条件语句
- ✅ 循环语句
- ✅ 数组操作
- ✅ 因果链
- ✅ 高级定义
- ✅ 组合条件
- ✅ 范围条件

### 集成测试

#### 示例文件测试 (`test_examples.py`)

- ✅ 简单测试文件
- ✅ 条件和循环示例
- ✅ 字符串处理示例
- ✅ 数学计算示例
- ✅ 简单因果链
- ✅ Playground示例

## CI/CD 流程

### GitHub Actions 工作流

CI流程在以下情况自动触发：

- 推送到 `main`、`master` 或 `develop` 分支
- 创建Pull Request到这些分支

### CI步骤

1. **测试作业** (`test`)
   - 在多个Python版本上运行（3.8, 3.9, 3.10, 3.11）
   - 运行单元测试
   - 运行集成测试
   - 运行所有测试

2. **代码检查作业** (`lint`)
   - 使用flake8进行代码风格检查
   - 检查语法错误
   - 检查代码复杂度

3. **构建作业** (`build`)
   - 构建Python包
   - 上传构建产物

## 添加新测试

### 添加单元测试

1. 在 `tests/unit/` 目录创建测试文件
2. 继承 `unittest.TestCase`
3. 使用 `test_` 前缀命名测试方法

示例：

```python
import unittest
from yanlv.compiler import YanLuCompiler

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.compiler = YanLuCompiler()
    
    def test_new_feature(self):
        code = '你的测试代码'
        result = self.compiler.run(code)
        self.assertEqual(len(result), 1)
```

### 添加集成测试

1. 在 `tests/integration/` 目录创建测试文件
2. 测试完整的代码执行流程
3. 验证输出结果

## 测试最佳实践

### 1. 测试命名

- 测试文件：`test_<功能>.py`
- 测试类：`Test<功能>`
- 测试方法：`test_<场景>`

### 2. 测试结构

```python
def test_<场景>(self):
    # 准备
    code = '...'
    
    # 执行
    result = self.compiler.run(code)
    
    # 验证
    self.assertEqual(len(result), 1)
    self.assertIn('期望输出', result[0])
```

### 3. 使用断言

- `assertEqual(a, b)` - 相等
- `assertIn(a, b)` - 包含
- `assertTrue(x)` - 为真
- `assertGreater(a, b)` - 大于
- `assertRaises(Error)` - 抛出异常

### 4. 测试覆盖

- 正常情况
- 边界情况
- 错误情况
- 空输入

## 持续改进

### 测试覆盖率

使用coverage.py检查测试覆盖率：

```bash
pip install coverage
coverage run run_tests.py
coverage report
coverage html
```

### 性能测试

添加性能测试：

```python
import time

def test_performance(self):
    start = time.time()
    # 执行代码
    end = time.time()
    self.assertLess(end - start, 1.0)  # 应该在1秒内完成
```

## 故障排查

### 测试失败

1. 查看错误信息
2. 检查测试代码
3. 检查被测代码
4. 使用调试器

### CI失败

1. 查看GitHub Actions日志
2. 本地重现问题
3. 修复并重新提交

## 总结

言律语言的测试体系确保：

- ✅ 代码质量
- ✅ 功能正确性
- ✅ 向后兼容性
- ✅ 持续集成

通过自动化测试，每次代码修改都会自动验证，避免手动测试的繁琐和遗漏。
