# 言律语言部署指南

## 📦 部署概述

本指南介绍如何将言律语言部署到生产环境。

---

## 🚀 快速部署

### 1. 发布到PyPI

#### 准备工作

```bash
# 安装发布工具
pip install build twine

# 确保所有测试通过
pytest

# 检查代码质量
flake8 src/yanlv
black --check src/yanlv
mypy src/yanlv
```

#### 构建包

```bash
# 清理旧的构建文件
rm -rf dist/ build/ *.egg-info

# 构建包
python -m build

# 检查包
twine check dist/*
```

#### 发布到PyPI

```bash
# 发布到TestPyPI（测试）
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ yanlv

# 发布到PyPI（正式）
twine upload dist/*
```

### 2. 创建GitHub Release

#### 使用GitHub CLI

```bash
# 创建标签
git tag v2.0.0
git push origin v2.0.0

# 创建Release
gh release create v2.0.0 \
  --title "言律语言 v2.0.0" \
  --notes-file RELEASE_NOTES.md \
  dist/*
```

#### 或使用GitHub Web界面

1. 访问 https://github.com/yanlv/yanlv/releases/new
2. 选择标签 v2.0.0
3. 填写标题和说明
4. 上传dist/目录中的文件
5. 发布

---

## 📋 部署检查清单

### 发布前检查

- [ ] 所有测试通过 (`pytest`)
- [ ] 代码质量检查通过 (`flake8`, `black`, `mypy`)
- [ ] 文档更新完成
- [ ] 版本号更新 (setup.py, pyproject.toml)
- [ ] CHANGELOG更新
- [ ] README更新

### 构建检查

- [ ] 构建成功 (`python -m build`)
- [ ] 包检查通过 (`twine check dist/*`)
- [ ] 本地安装测试通过

### 发布检查

- [ ] TestPyPI发布成功
- [ ] TestPyPI安装测试通过
- [ ] PyPI发布成功
- [ ] PyPI安装测试通过
- [ ] GitHub Release创建成功

---

## 🔧 配置文件说明

### setup.py

传统Python包配置文件，包含：
- 包基本信息
- 依赖管理
- 入口点配置
- 分类信息

### pyproject.toml

现代Python包配置文件，包含：
- 构建系统配置
- 项目元数据
- 工具配置（black, mypy, pytest）

### requirements.txt

依赖列表，用于开发环境。

---

## 🌐 在线文档部署

### 使用ReadTheDocs

1. 访问 https://readthedocs.org/
2. 导入项目：https://github.com/yanlv/yanlv
3. 配置构建：
   - Python版本：3.8
   - 配置文件：docs/conf.py
4. 构建文档

### 配置Sphinx

```bash
# 安装Sphinx
pip install sphinx sphinx-rtd-theme

# 初始化文档
cd docs
sphinx-quickstart

# 构建文档
make html
```

---

## 🐳 Docker部署（可选）

### 创建Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY src/ ./src/
COPY setup.py .
COPY pyproject.toml .

# 安装包
RUN pip install -e .

# 设置入口点
ENTRYPOINT ["yanlv"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t yanlv:2.0.0 .

# 运行容器
docker run -it yanlv:2.0.0

# 推送到Docker Hub
docker push yanlv:2.0.0
```

---

## 📊 监控和日志

### 性能监控

```python
from yanlv.lexer import create_lexer

lexer = create_lexer("jieba", verbose=True)
tokens = lexer.tokenize(source_code)

# 获取性能统计
stats = lexer.get_performance_stats()
print(f"处理时间: {stats['total_time']:.3f}秒")
print(f"词元数量: {stats['tokens_processed']}")
```

### 错误监控

```python
from yanlv.error_handling import EnhancedErrorHandler

handler = EnhancedErrorHandler()
# ... 处理错误 ...

# 获取错误统计
stats = handler.get_statistics()
print(f"总错误数: {stats['total_errors']}")
print(f"恢复率: {stats['recovery_rate']:.2%}")
```

---

## 🔄 持续集成

### GitHub Actions配置

已配置在 `.github/workflows/ci-cd.yml`：

- **测试**：多Python版本测试
- **Lint**：代码质量检查
- **构建**：自动构建包
- **部署**：自动发布到PyPI

### 触发条件

- Push到main分支：完整测试 + 部署
- Push到develop分支：完整测试
- Pull Request：完整测试

---

## 🚨 故障排查

### 常见问题

#### 1. 安装失败

```bash
# 检查Python版本
python --version  # 需要 >= 3.8

# 检查依赖
pip install -r requirements.txt

# 清理缓存
pip cache purge
```

#### 2. 导入错误

```bash
# 重新安装
pip uninstall yanlv
pip install yanlv

# 检查路径
python -c "import sys; print(sys.path)"
```

#### 3. 性能问题

```python
# 启用缓存
lexer = create_lexer("jieba", enable_cache=True, cache_size=5000)

# 使用高级优化
from yanlv.performance_optimizer import OptimizationLevel
optimizer = PerformanceOptimizer(OptimizationLevel.ADVANCED)
```

---

## 📞 支持

### 获取帮助

- **文档**: https://yanlv.readthedocs.io
- **Issues**: https://github.com/yanlv/yanlv/issues
- **邮件**: yanlv@example.com

### 报告问题

请提供以下信息：
- Python版本
- 操作系统
- 错误信息
- 复现步骤

---

## 📝 维护

### 定期任务

- **每周**: 检查依赖更新
- **每月**: 性能测试和优化
- **每季度**: 安全审计

### 更新流程

1. 更新代码
2. 运行测试
3. 更新版本号
4. 更新文档
5. 发布新版本

---

## 🎯 最佳实践

### 性能优化

- 启用缓存
- 使用批处理
- 配置合适的缓存大小

### 错误处理

- 使用增强错误处理器
- 配置合适的恢复策略
- 记录错误日志

### 用户反馈

- 启用反馈收集
- 定期分析反馈
- 根据反馈优化

---

<div align="center">

**部署完成！**

如有问题，请参考文档或联系支持。

</div>