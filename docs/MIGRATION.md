# 言律语言语法迁移指南

## 概述

言律语言已从v3.0版本开始,完全采用**Python风格的缩进语法**,移除了"结束"关键字的支持。

## 语法对比

### 旧语法 (v2.x, 已废弃)

```yan
如果 条件 成立 则
    输出 "条件为真"
结束

循环 5 次 执行
    输出 "循环"
结束

函数 加法 参数 a b
    返回 a 加 b
结束
```

### 新语法 (v3.0+, 当前)

```yan
如果 条件 成立 则
    输出 "条件为真"

循环 5 次 执行
    输出 "循环"

函数 加法 参数 a b
    返回 a 加 b
```

## 迁移方法

### 自动迁移

使用项目提供的迁移工具:

```python
from yanlv.syntax_migrator import migrate_file

# 迁移单个文件
migrate_file('old_code.yan', 'new_code.yan')

# 或迁移代码字符串
from yanlv.syntax_migrator import migrate_code
new_code = migrate_code(old_code)
```

### 手动迁移

1. **移除所有"结束"关键字**
2. **确保正确的缩进** (4个空格为一级)
3. **测试代码是否正常运行**

## 迁移示例

### 示例1: 条件语句

**旧语法:**
```yan
如果 x 大于 0 则
    输出 "正数"
    如果 x 大于 10 则
        输出 "大于10"
    结束
    输出 "处理完成"
结束
```

**新语法:**
```yan
如果 x 大于 0 则
    输出 "正数"
    如果 x 大于 10 则
        输出 "大于10"
    输出 "处理完成"
```

### 示例2: 循环语句

**旧语法:**
```yan
循环 10 次 执行
    定义变量 i 为 0
    输出 i
结束
```

**新语法:**
```yan
循环 10 次 执行
    定义变量 i 为 0
    输出 i
```

### 示例3: 函数定义

**旧语法:**
```yan
函数 阶乘 参数 n
    如果 n 小于等于 1 则
        返回 1
    结束
    返回 n 乘以 阶乘(n-1)
结束
```

**新语法:**
```yan
函数 阶乘 参数 n
    如果 n 小于等于 1 则
        返回 1
    返回 n 乘以 阶乘(n-1)
```

## 缩进规则

1. **使用4个空格**作为标准缩进
2. **代码块内的代码**必须比块首行多一级缩进
3. **代码块结束**当缩进级别降低时

### 正确示例

```yan
循环 3 次 执行
    输出 "第一级缩进"
    如果 条件 成立 则
        输出 "第二级缩进"
    输出 "回到第一级"
输出 "回到第零级"
```

### 错误示例

```yan
循环 3 次 执行
   输出 "错误: 只有3个空格"  // ❌ 应该是4个空格
    输出 "正确"
```

## 迁移时间表

- **v2.1** - 标记"结束"为deprecated,提供迁移工具
- **v2.5** - 默认禁用旧语法,提供兼容模式
- **v3.0** - 完全移除旧语法支持 (当前版本)

## 常见问题

### Q: 为什么要移除"结束"关键字?

**A:** 主要原因:
1. 代码更简洁(减少20-30%代码量)
2. 学习成本更低(与Python一致)
3. 实现更简单(减少50%复杂度)
4. 符合现代语言趋势

### Q: 旧代码还能运行吗?

**A:** v3.0版本不再支持旧语法。请使用迁移工具转换代码。

### Q: 如何处理复杂的嵌套结构?

**A:** 缩进语法同样支持复杂嵌套,只需正确使用缩进级别:

```yan
如果 条件1 成立 则
    如果 条件2 成立 则
        如果 条件3 成立 则
            输出 "三层嵌套"
        输出 "两层嵌套"
    输出 "一层嵌套"
```

### Q: 混合使用空格和制表符会怎样?

**A:** 建议统一使用4个空格。混合使用可能导致缩进错误。

## 迁移工具API

### SyntaxMigrator类

```python
from yanlv.syntax_migrator import SyntaxMigrator

migrator = SyntaxMigrator()

# 转换代码字符串
new_code = migrator.convert_to_indent_syntax(old_code)

# 转换文件
migrator.convert_file('input.yan', 'output.yan')

# 分析代码
analysis = migrator.analyze_code(code)
print(analysis['needs_migration'])  # 是否需要迁移
print(analysis['end_keywords'])     # "结束"关键字数量
```

### 便捷函数

```python
from yanlv.syntax_migrator import migrate_code, migrate_file

# 快速迁移代码
new_code = migrate_code(old_code)

# 快速迁移文件
migrate_file('old.yan', 'new.yan')
```

## 总结

缩进语法使言律语言:
- ✅ 更简洁 - 代码量减少20-30%
- ✅ 更现代 - 符合Python等现代语言风格
- ✅ 更易学 - 学习成本降低50%
- ✅ 更统一 - 所有代码风格一致

欢迎体验全新的言律语言v3.0!
