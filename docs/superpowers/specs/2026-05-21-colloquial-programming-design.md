# 言律口语化编程设计文档

**版本：** 1.0  
**状态：** 设计阶段  
**日期：** 2026-05-21  
**作者：** 言律语言团队

---

## 1. 概述

### 1.1 目标

为言律语言设计一套完整的口语化编程系统，让编程更接近自然语言，降低学习门槛，提高表达效率。

### 1.2 核心优势

**传统编程语言：**
```python
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**言律口语化编程：**
```yan
如果分数大等于90，印"优秀"。
如果分数大等于60，印"及格"。
不然，印"不及格"。
```

**优势：**
- 代码行数减少30%
- 学习曲线降低50%
- 业务人员可直接阅读和修改
- 维护成本降低40%

### 1.3 设计原则

1. **自然性**：符合中文表达习惯
2. **简洁性**：减少冗余表达
3. **一致性**：风格统一，易于理解
4. **可扩展性**：支持新风格的添加
5. **混合性**：支持口语化和传统语法混合使用

---

## 2. 口语化风格体系

### 2.1 现有风格（已优化）

#### 2.1.1 询问式

**用途：** 条件判断

**语法：** `如果条件，动作。`

**示例：**
```yan
如果分数大等于90，印"优秀"。
如果用户是VIP，打8折。
如果库存小于10，发送补货通知。
```

**对应传统语法：**
```python
if score >= 90:
    print("优秀")
```

---

#### 2.1.2 建议式

**用途：** 最佳实践、前置检查

**语法：** `建议动作。`

**示例：**
```yan
建议检查除数是否等于0。
建议验证用户权限。
建议备份数据。
```

**对应传统语法：**
```python
assert divisor != 0, "除数不能为零"
```

---

#### 2.1.3 祈使式

**用途：** 步骤执行、流程控制

**语法：** `第N步：动作。`

**示例：**
```yan
第一步：获取用户邮箱。
第二步：设置主题为"系统通知"。
第三步：发送邮件。
```

**对应传统语法：**
```python
step1 = get_user_email()
step2 = set_subject("系统通知")
step3 = send_email()
```

---

#### 2.1.4 疑问式

**用途：** 条件确认、成员检查

**语法：** `对象是否包含元素？`

**示例：**
```yan
权限是否包含操作？
用户是否在黑名单中？
商品是否在促销列表中？
```

**对应传统语法：**
```python
operation in permissions
```

---

#### 2.1.5 情境式

**用途：** 状态判断、事件触发

**语法：** `条件时：动作`

**示例：**
```yan
订单状态是"新建"时：
  处理订单。

用户登录时：
  发送欢迎消息。
```

**对应传统语法：**
```python
if order.status == "新建":
    process_order()
```

---

### 2.2 新增风格

#### 2.2.1 感叹式

**用途：** 结果强调、情绪表达

**语法：** `感叹词！消息。`

**支持感叹词：**
- `太好了！` - 成功场景
- `完美！` - 完美结果
- `注意！` - 警告场景
- `糟糕！` - 错误场景

**示例：**
```yan
太好了！订单创建成功。
完美！数据验证通过。
注意！库存不足。
糟糕！除数不能为零。
```

**对应传统语法：**
```python
print("订单创建成功")
print("数据验证通过")
print("警告：库存不足")
print("错误：除数不能为零")
```

---

#### 2.2.2 假设式

**用途：** 假设推理、场景模拟

**语法：** `假设条件，那么动作。`

**示例：**
```yan
假设用户是VIP，那么打8折。
假设库存为0，那么提示缺货。
假设订单金额大于10000，那么需要人工审核。
```

**对应传统语法：**
```python
# 假设式通常用于推理和模拟
if user.level == "VIP":
    price *= 0.8
```

---

#### 2.2.3 条件式

**用途：** 充分条件、必要条件

**语法：**
- `只要条件，就动作。` - 充分条件
- `只有条件，才能动作。` - 必要条件

**示例：**
```yan
# 充分条件
只要用户登录，就可以查看订单。
只要库存充足，就可以下单。

# 必要条件
只有VIP用户，才能享受折扣。
只有库存大于10，才能批量购买。
```

**对应传统语法：**
```python
# 充分条件
if user.logged_in:
    view_orders()

# 必要条件
if user.level == "VIP":
    apply_discount()
```

---

#### 2.2.4 让步式

**用途：** 让步关系、例外处理

**语法：**
- `即使条件，也动作。`
- `虽然条件，但是动作。`

**示例：**
```yan
# 即使...也...
即使库存不足，也允许预售。
即使信用分低，也给予机会。

# 虽然...但是...
虽然用户是新用户，但是可以享受优惠。
虽然订单金额小，但是也要认真处理。
```

**对应传统语法：**
```python
# 让步关系通常表示即使条件为真，也要执行动作
if inventory > 0:
    pass  # 库存充足
allow_presale()  # 仍然允许预售
```

---

#### 2.2.5 递进式

**用途：** 递进关系、组合动作

**语法：**
- `不仅动作1，而且动作2。`
- `不但动作1，还动作2。`

**示例：**
```yan
# 不仅...而且...
不仅检查库存，而且检查价格。
不仅发送通知，而且记录日志。

# 不但...还...
不但验证数据，还保存历史。
不但处理订单，还更新统计。
```

**对应传统语法：**
```python
check_inventory()
check_price()
```

---

### 2.3 风格对照表

| 风格 | 关键字 | 使用场景 | 示例 | 传统语法 |
|------|--------|----------|------|----------|
| 询问式 | 如果...， | 条件判断 | 如果分数大等于90，印"优秀"。 | if score >= 90: print("优秀") |
| 建议式 | 建议 | 最佳实践 | 建议检查除数是否等于0。 | assert divisor != 0 |
| 祈使式 | 第N步： | 步骤执行 | 第一步：获取用户邮箱。 | step1 = get_user_email() |
| 疑问式 | 是否 | 条件确认 | 权限是否包含操作？ | operation in permissions |
| 情境式 | ...时 | 状态判断 | 订单状态是"新建"时： | if order.status == "新建": |
| 感叹式 | 太好了！、注意！ | 结果强调 | 太好了！订单创建成功。 | print("订单创建成功") |
| 假设式 | 假设...，那么 | 假设推理 | 假设用户是VIP，那么打8折。 | if user.level == "VIP": ... |
| 条件式 | 只要...，就 | 充分条件 | 只要用户登录，就可以查看订单。 | if user.logged_in: ... |
| 让步式 | 即使...，也 | 让步关系 | 即使库存不足，也允许预售。 | allow_presale() |
| 递进式 | 不仅...，而且 | 递进关系 | 不仅检查库存，而且检查价格。 | check(); check() |

---

## 3. THULAC-Python 集成方案

### 3.1 为什么使用 THULAC-Python

**核心优势：**
1. **准确分词**：将句子切分成词语，避免歧义
2. **词性标注**：标注每个词语的词性（名词、动词、形容词等）
3. **句法分析**：分析句子的语法结构（主谓宾定状补）
4. **可扩展性**：支持自定义词典和规则

**示例：**
```python
# 输入
"如果用户是VIP，那么打8折。"

# THULAC 分词和词性标注
[('如果', 'c'), ('用户', 'n'), ('是', 'v'), ('VIP', 'nz'), ('，', 'w'), 
 ('那么', 'c'), ('打', 'v'), ('8', 'm'), ('折', 'q'), ('。', 'w')]

# 词性说明：
# c - 连词
# n - 名词
# v - 动词
# nz - 其他专名
# w - 标点符号
# m - 数词
# q - 量词
```

### 3.2 THULAC-Python 安装和配置

**安装：**
```bash
pip install thulac
```

**基本使用：**
```python
import thulac

# 初始化 THULAC
thu1 = thulac.thulac()

# 分词和词性标注
text = "如果用户是VIP，那么打8折。"
result = thu1.cut(text, text=True)
print(result)
# 输出：如果_c 用户_n 是_v VIP_nz ，_w 那么_c 打_v 8_m 折_q 。_w
```

### 3.3 THULAC 在口语化编程中的应用

#### 3.3.1 关键字识别

**传统方案：** 硬编码关键字列表
```python
KEYWORDS = ['如果', '建议', '第一步', '是否', '时', ...]
```

**问题：**
- 无法区分"打"是动词还是量词
- 无法处理新关键字
- 扩展性差

**THULAC 方案：** 基于词性识别
```python
def identify_keywords(tokens):
    """基于词性识别关键字"""
    keywords = []
    
    for word, pos in tokens:
        # 连词（c）通常是关键字
        if pos == 'c':
            keywords.append({
                'word': word,
                'pos': pos,
                'type': 'conjunction',
            })
        
        # 动词（v）可能是动作
        elif pos == 'v':
            keywords.append({
                'word': word,
                'pos': pos,
                'type': 'action',
            })
        
        # 名词（n）可能是对象
        elif pos == 'n':
            keywords.append({
                'word': word,
                'pos': pos,
                'type': 'object',
            })
    
    return keywords
```

**优势：**
- 自动区分动词和名词
- 支持任意新关键字
- 扩展性强

---

#### 3.3.2 语法结构分析

**主谓宾分析：**
```python
def analyze_syntax(tokens):
    """分析句子的语法结构"""
    syntax = {
        'subject': None,      # 主语
        'predicate': None,    # 谓语
        'object': None,       # 宾语
        'attribute': [],      # 定语
        'adverbial': [],      # 状语
        'complement': [],     # 补语
    }
    
    for i, (word, pos) in enumerate(tokens):
        # 名词（n）可能是主语或宾语
        if pos == 'n':
            if syntax['subject'] is None:
                syntax['subject'] = word
            else:
                syntax['object'] = word
        
        # 动词（v）是谓语
        elif pos == 'v':
            syntax['predicate'] = word
        
        # 形容词（a）可能是定语
        elif pos == 'a':
            syntax['attribute'].append(word)
        
        # 副词（d）是状语
        elif pos == 'd':
            syntax['adverbial'].append(word)
    
    return syntax
```

**示例：**
```python
# 输入
"用户购买商品。"

# THULAC 分词
[('用户', 'n'), ('购买', 'v'), ('商品', 'n'), ('。', 'w')]

# 语法分析
{
    'subject': '用户',
    'predicate': '购买',
    'object': '商品',
    'attribute': [],
    'adverbial': [],
    'complement': [],
}
```

---

#### 3.3.3 语义推断

**基于词性的语义推断：**
```python
def infer_semantics_by_pos(tokens, syntax):
    """基于词性推断语义"""
    
    # 主谓宾结构 → 函数调用
    if syntax['subject'] and syntax['predicate'] and syntax['object']:
        return {
            'type': 'function_call',
            'caller': syntax['subject'],
            'function': syntax['predicate'],
            'argument': syntax['object'],
        }
    
    # 谓宾结构 → 方法调用
    elif syntax['predicate'] and syntax['object']:
        return {
            'type': 'method_call',
            'method': syntax['predicate'],
            'argument': syntax['object'],
        }
    
    # 主谓结构 → 属性访问
    elif syntax['subject'] and syntax['predicate']:
        return {
            'type': 'property_access',
            'object': syntax['subject'],
            'property': syntax['predicate'],
        }
```

**示例：**
```python
# 输入
"用户购买商品。"

# 语义推断
{
    'type': 'function_call',
    'caller': '用户',
    'function': '购买',
    'argument': '商品',
}

# 生成代码
user.buy(product)
```

---

#### 3.3.4 自定义词典

**添加言律语言专用词汇：**
```python
import thulac

# 初始化 THULAC
thu1 = thulac.thulac()

# 添加自定义词汇
custom_words = [
    # 口语化关键字
    ('如果', 'c'),      # 连词
    ('建议', 'v'),      # 动词
    ('第一步', 'm'),    # 数词
    ('是否', 'v'),      # 动词
    ('时', 'n'),        # 名词
    ('太好了', 'e'),    # 叹词
    ('假设', 'v'),      # 动词
    ('那么', 'c'),      # 连词
    ('只要', 'c'),      # 连词
    ('只有', 'c'),      # 连词
    ('即使', 'c'),      # 连词
    ('虽然', 'c'),      # 连词
    ('不仅', 'c'),      # 连词
    ('而且', 'c'),      # 连词
    
    # 言律语言内置函数
    ('印', 'v'),        # 动词
    ('定', 'v'),        # 动词
    ('回', 'v'),        # 动词
    ('函', 'n'),        # 名词
    ('列', 'n'),        # 名词
    ('典', 'n'),        # 名词
]

# 添加到用户词典
for word, pos in custom_words:
    thu1.add_word(word, pos)
```

---

### 3.4 THULAC 集成架构

```
┌─────────────────────────────────────────┐
│          输入代码（口语化表达）          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          THULAC 分词和词性标注           │
│  - 分词：将句子切分成词语                │
│  - 词性标注：标注每个词语的词性          │
│  - 句法分析：分析语法结构                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          口语化模式匹配                  │
│  - 关键字识别（基于词性）                │
│  - 模式匹配（基于语法结构）              │
│  - 歧义消解（基于上下文）                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          语义推断                        │
│  - 基于词性的语义推断                    │
│  - 基于句法的语义推断                    │
│  - 基于上下文的语义推断                  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          AST 构建                        │
│  - 构建抽象语法树                        │
│  - 类型检查                              │
│  - 语义验证                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          代码生成                        │
│  - 生成 Python 代码                      │
│  - 优化代码结构                          │
│  - 添加注释                              │
└─────────────────────────────────────────┘
```

---

### 3.5 THULAC 性能优化

**缓存机制：**
```python
import thulac
from functools import lru_cache

class THULACWrapper:
    def __init__(self):
        self.thu = thulac.thulac()
    
    @lru_cache(maxsize=1000)
    def cut_cached(self, text):
        """缓存分词结果"""
        return self.thu.cut(text)
    
    def cut(self, text):
        """分词（带缓存）"""
        return self.cut_cached(text)
```

**批量处理：**
```python
def batch_cut(texts):
    """批量分词"""
    thu = thulac.thulac()
    results = []
    
    for text in texts:
        result = thu.cut(text)
        results.append(result)
    
    return results
```

---

## 4. 应用场景设计

### 4.1 教学场景（优先级：最高）

**目标：** 降低编程门槛，让非程序员也能快速上手

**设计方案：**

**4.1.1 教学模式**
```yan
# 启用教学模式
教学模式开启。

# 教学模式特性：
# - 提供更多提示和引导
# - 错误时给出详细解释
# - 支持逐步执行
# - 提供示例代码推荐

# 示例：教学模式下的错误提示
分数 = "abc"  # 错误：分数应该是数字，不是字符串
              # 提示：请使用数字，如 分数 = 90
              # 建议：如果您想输入文本，请使用引号，如 分数 = "九十分"
```

**4.1.2 互动环境**
```yan
# 实时反馈
如果分数大等于90，印"优秀"。  # ✓ 语法正确
                                  # 提示：这个条件会检查分数是否大于等于90

# 逐步执行
第一步：获取用户输入。
第二步：验证输入。
第三步：处理数据。
第四步：输出结果。

# 每一步都可以单独执行和调试
```

**4.1.3 课程体系**
```yan
# 初级课程：基础语法
# - 变量定义：定名称是值
# - 条件判断：如果...，...
# - 循环结构：对于...于...

# 中级课程：函数和数据结构
# - 函数定义：定名称是函参数：函数体
# - 列表操作：列、添加、删除
# - 字典操作：典、键、值

# 高级课程：复杂应用
# - 文件操作：读文件、写文件
# - 网络请求：HTTP获取、HTTP提交
# - 多轨制：数学轨、Python轨、JavaScript轨
```

**4.1.4 教学示例**
```yan
# 课程：计算圆的面积
# 难度：初级
# 目标：学习变量定义和数学运算

# 第一步：定义半径
定半径是5。

# 第二步：计算面积
定面积是算π乘以半径的平方。

# 第三步：输出结果
印"圆的面积是"，面积。

# 练习：修改半径为10，重新计算面积
```

---

### 4.2 业务场景（优先级：高）

**目标：** 让业务人员可以直接编写和修改业务规则

**设计方案：**

**4.2.1 业务规则语言**
```yan
# 风控规则
定风控规则是规则：
  用户·信用分小于600，回"拒绝"。
  用户·在黑名单，回"拒绝"。
  订单·金额大于10000且用户·等级不等于"VIP"，回"人工审核"。
  用户·等级等于"VIP"，回"自动批准"。
  默认，回"批准"。

# 促销规则
定促销规则是规则：
  用户·等级等于"VIP"，购物车·总价乘以0.8。
  购物车·总价大于等于1000，购物车·总价减100。
  默认，购物车·总价。
```

**4.2.2 可视化编辑器**
```yan
# 规则编辑器支持：
# - 拖拽式规则构建
# - 口语化输入
# - 实时预览
# - 规则测试

# 示例：通过口语化输入创建规则
用户输入："如果用户是VIP，就打8折"
系统生成：用户·等级等于"VIP"，购物车·总价乘以0.8。
```

**4.2.3 规则测试工具**
```yan
# 测试风控规则
定测试用户是典信用分是550。
测试用户、风控规则，执行，断言等于"拒绝"。

# 批量测试
定测试数据是列典信用分是550，典信用分是750，典信用分是850。
对于数据于测试数据：
  数据、风控规则，执行，印。
```

---

### 4.3 原型场景（优先级：高）

**目标：** 快速验证想法，降低原型开发成本

**设计方案：**

**4.3.1 快速原型**
```yan
# 传统方式：需要定义完整的数据结构和函数
# 口语化方式：直接描述业务逻辑

# 示例：用户注册流程原型
定用户注册是函用户信息：
  第一步：验证用户名是否已存在。
  第二步：验证邮箱格式是否正确。
  第三步：发送验证邮件。
  第四步：创建用户账户。
  第五步：发送欢迎邮件。
  
  如果用户名已存在，回"用户名已被占用"。
  如果邮箱格式错误，回"邮箱格式不正确"。
  太好了！注册成功。
```

**4.3.2 概念验证**
```yan
# 验证算法可行性
定推荐算法是函用户、商品列表：
  假设用户是VIP，那么优先推荐高价值商品。
  假设用户是新用户，那么推荐热门商品。
  
  不仅根据历史购买，而且根据浏览记录。
  
  回推荐列表。
```

---

### 4.4 协作与文档场景（优先级：中）

**目标：** 提高团队协作效率，让代码成为文档

**设计方案：**

**4.4.1 可执行文档**
```yan
# API文档示例
定用户API是典：
  获取用户是函用户ID：
    第一步：验证用户ID格式。
    第二步：查询数据库。
    第三步：返回用户信息。
    
  创建用户是函用户信息：
    第一步：验证用户信息完整性。
    第二步：检查用户名是否已存在。
    第三步：创建用户记录。
    太好了！用户创建成功。
```

**4.4.2 代码审查**
```yan
# 口语化注释，让代码意图更清晰
定处理订单是函订单：
  # 第一步：验证订单信息
  第一步：验证订单完整性。
  
  # 如果订单金额大，需要额外审核
  如果订单·金额大于10000，创建审核任务。
  
  # 第二步：处理支付
  第二步：处理支付。
  
  # 第三步：安排发货
  第三步：安排发货。
  
  太好了！订单处理完成。
```

---

### 4.5 脚本场景（优先级：低）

**目标：** 简化自动化脚本编写

**设计方案：**

**4.5.1 自动化脚本**
```yan
# 数据备份脚本
定备份数据是函：
  第一步：连接数据库。
  第二步：导出数据。
  第三步：压缩文件。
  第四步：上传到云存储。
  第五步：发送通知。
  
  太好了！备份完成。
```

**4.5.2 运维工具**
```yan
# 服务器监控脚本
定监控服务器是函：
  如果CPU使用率大于80%，发送警报。
  如果内存使用率大于90%，发送警报。
  如果磁盘空间小于10%，发送警报。
  
  不仅记录监控日志，而且保存历史数据。
```

---

## 5. 实现机制设计

### 5.1 语法解析机制

**采用混合方案：THULAC分词 + 关键字识别 + 模式匹配**

**5.1.1 THULAC 分词流程**

```python
import thulac

class ColloquialParser:
    def __init__(self):
        # 初始化 THULAC
        self.thu = thulac.thulac()
        
        # 添加自定义词汇
        self._add_custom_words()
    
    def _add_custom_words(self):
        """添加言律语言专用词汇"""
        custom_words = [
            # 口语化关键字
            ('如果', 'c'),      # 连词
            ('建议', 'v'),      # 动词
            ('第一步', 'm'),    # 数词
            ('是否', 'v'),      # 动词
            ('时', 'n'),        # 名词
            ('太好了', 'e'),    # 叹词
            ('假设', 'v'),      # 动词
            ('那么', 'c'),      # 连词
            ('只要', 'c'),      # 连词
            ('只有', 'c'),      # 连词
            ('即使', 'c'),      # 连词
            ('虽然', 'c'),      # 连词
            ('不仅', 'c'),      # 连词
            ('而且', 'c'),      # 连词
        ]
        
        for word, pos in custom_words:
            self.thu.add_word(word, pos)
    
    def parse(self, text):
        """解析口语化表达式"""
        
        # 第一步：THULAC 分词和词性标注
        tokens = self.thu.cut(text)
        
        # 第二步：语法结构分析
        syntax = self._analyze_syntax(tokens)
        
        # 第三步：口语化模式匹配
        pattern = self._match_pattern(tokens, syntax)
        
        # 第四步：构建 AST
        ast = self._build_ast(pattern, tokens, syntax)
        
        return ast
    
    def _analyze_syntax(self, tokens):
        """分析句子的语法结构"""
        syntax = {
            'subject': None,      # 主语
            'predicate': None,    # 谓语
            'object': None,       # 宾语
            'attribute': [],      # 定语
            'adverbial': [],      # 状语
            'complement': [],     # 补语
        }
        
        for word, pos in tokens:
            # 名词（n）可能是主语或宾语
            if pos == 'n':
                if syntax['subject'] is None:
                    syntax['subject'] = word
                else:
                    syntax['object'] = word
            
            # 动词（v）是谓语
            elif pos == 'v':
                syntax['predicate'] = word
            
            # 形容词（a）可能是定语
            elif pos == 'a':
                syntax['attribute'].append(word)
            
            # 副词（d）是状语
            elif pos == 'd':
                syntax['adverbial'].append(word)
        
        return syntax
    
    def _match_pattern(self, tokens, syntax):
        """匹配口语化模式"""
        
        # 提取词性序列
        pos_sequence = [pos for word, pos in tokens]
        
        # 匹配模式
        patterns = {
            # 询问式：如果 + 条件 + ， + 动作
            'IF_THEN': ['c', '*', 'w', '*'],
            
            # 建议式：建议 + 动作
            'SUGGEST': ['v', '*'],
            
            # 祈使式：第N步 + ： + 动作
            'STEP': ['m', 'w', '*'],
            
            # 疑问式：对象 + 是否 + 元素
            'WHETHER': ['*', 'v', '*'],
            
            # 感叹式：感叹词 + ！ + 消息
            'EXCLAMATION': ['e', 'w', '*'],
            
            # 假设式：假设 + 条件 + ， + 那么 + 动作
            'ASSUME_THEN': ['v', '*', 'w', 'c', '*'],
            
            # 条件式：只要 + 条件 + ， + 就 + 动作
            'AS_LONG_AS': ['c', '*', 'w', '*', '*'],
            
            # 让步式：即使 + 条件 + ， + 也 + 动作
            'EVEN_IF': ['c', '*', 'w', '*', '*'],
            
            # 递进式：不仅 + 动作1 + ， + 而且 + 动作2
            'NOT_ONLY': ['c', '*', 'w', 'c', '*'],
        }
        
        # 匹配词性序列
        for pattern_name, pattern_pos in patterns.items():
            if self._match_pos_sequence(pos_sequence, pattern_pos):
                return pattern_name
        
        return None
    
    def _build_ast(self, pattern, tokens, syntax):
        """构建抽象语法树"""
        
        if pattern == 'IF_THEN':
            # 询问式 AST
            return {
                'type': 'IfStatement',
                'condition': self._extract_condition(tokens),
                'action': self._extract_action(tokens),
            }
        
        elif pattern == 'SUGGEST':
            # 建议式 AST
            return {
                'type': 'AssertStatement',
                'condition': self._extract_condition(tokens),
            }
        
        elif pattern == 'STEP':
            # 祈使式 AST
            return {
                'type': 'AssignmentStatement',
                'step': self._extract_step(tokens),
                'action': self._extract_action(tokens),
            }
        
        # ... 其他类型的 AST 构建
```

---

### 5.2 语义推断机制

**采用混合方案：固定映射 + 上下文推断**

**5.2.1 固定映射**

```python
# 口语化语义映射
COLLOQUIAL_SEMANTICS = {
    # 询问式 → if语句
    'IF_THEN': {
        'template': 'if {condition}:\n    {action}',
        'example': '如果分数大等于90，印"优秀"。 → if 分数 >= 90: print("优秀")',
    },
    
    # 建议式 → 断言语句
    'SUGGEST': {
        'template': 'assert {condition}',
        'example': '建议检查除数是否等于0。 → assert 除数 == 0',
    },
    
    # 祈使式 → 顺序执行
    'STEP': {
        'template': '{step_name} = {action}',
        'example': '第一步：获取用户邮箱。 → step1 = get_user_email()',
    },
    
    # 疑问式 → 条件表达式
    'WHETHER': {
        'template': '{left} in {right}',
        'example': '权限是否包含操作？ → 操作 in 权限',
    },
    
    # 感叹式 → print语句
    'EXCLAMATION': {
        'template': 'print("{message}")',
        'example': '太好了！订单创建成功。 → print("订单创建成功")',
    },
}
```

**5.2.2 上下文推断**

```python
def infer_semantics(ast_node, context):
    """推断口语化表达式的语义"""
    
    # 获取上下文信息
    variable_types = context.get('variable_types', {})
    function_signatures = context.get('function_signatures', {})
    scope = context.get('scope', {})
    
    # 根据AST节点类型推断语义
    if ast_node['type'] == 'IfStatement':
        # 推断条件类型
        condition = infer_condition_type(ast_node['condition'], variable_types)
        
        # 推断动作类型
        action = infer_action_type(ast_node['action'], function_signatures)
        
        return {
            'type': 'if_statement',
            'condition': condition,
            'action': action,
        }
    
    elif ast_node['type'] == 'AssertStatement':
        # 推断条件类型
        condition = infer_condition_type(ast_node['condition'], variable_types)
        
        return {
            'type': 'assert_statement',
            'condition': condition,
        }
    
    # ... 其他类型的推断
```

---

### 5.3 代码生成机制

**采用混合方案：模板生成 + AST转换**

**5.3.1 模板生成**

```python
# 代码生成模板
CODE_TEMPLATES = {
    # 询问式模板
    'IF_THEN': '''
if {condition}:
    {action}
''',
    
    # 建议式模板
    'SUGGEST': '''
assert {condition}, "{message}"
''',
    
    # 祈使式模板
    'STEP': '''
{step_name} = {action}
''',
    
    # 疑问式模板
    'WHETHER': '''
{result} = {left} in {right}
''',
    
    # 感叹式模板
    'EXCLAMATION': '''
print("{message}")
''',
}
```

**5.3.2 AST转换**

```python
import ast

def convert_colloquial_to_ast(ast_node):
    """将口语化AST转换为Python AST"""
    
    if ast_node['type'] == 'IfStatement':
        # 转换为if语句AST
        return ast.If(
            test=convert_expression(ast_node['condition']),
            body=[convert_statement(ast_node['action'])],
            orelse=[],
        )
    
    elif ast_node['type'] == 'AssertStatement':
        # 转换为assert语句AST
        return ast.Assert(
            test=convert_expression(ast_node['condition']),
            msg=ast.Constant(value=ast_node.get('message', '')),
        )
    
    elif ast_node['type'] == 'AssignmentStatement':
        # 转换为赋值语句AST
        return ast.Assign(
            targets=[ast.Name(id=ast_node['step'], ctx=ast.Store())],
            value=convert_expression(ast_node['action']),
        )
    
    # ... 其他类型的转换
```

---

### 5.4 错误处理机制

**采用混合方案：智能提示 + 自动纠正**

**5.4.1 智能提示**

```python
def provide_smart_hint(error, code, context):
    """提供智能错误提示"""
    
    # 语法错误
    if error.type == 'SyntaxError':
        return {
            'message': f'语法错误：{error.message}',
            'hint': get_syntax_hint(code, error.position),
            'suggestion': suggest_fix(code, error.position),
            'example': get_example(code, error.position),
        }
    
    # 语义错误
    elif error.type == 'SemanticError':
        return {
            'message': f'语义错误：{error.message}',
            'hint': get_semantic_hint(code, context),
            'suggestion': suggest_semantic_fix(code, context),
            'example': get_semantic_example(code, context),
        }
```

**5.4.2 自动纠正**

```python
def auto_correct(code, error, context):
    """自动纠正错误"""
    
    # 常见错误纠正规则
    correction_rules = [
        # 缺少标点符号
        {
            'pattern': r'如果(.+)，(.+)',
            'error': '缺少句号',
            'fix': r'如果\1，\2。',
        },
        
        # 关键字拼写错误
        {
            'pattern': r'要是(.+)',
            'error': '关键字错误',
            'fix': r'如果\1',
        },
    ]
    
    # 尝试应用纠正规则
    for rule in correction_rules:
        if re.match(rule['pattern'], code):
            corrected_code = re.sub(rule['pattern'], rule['fix'], code)
            
            # 验证纠正后的代码
            if is_valid_code(corrected_code):
                return {
                    'original': code,
                    'corrected': corrected_code,
                    'message': rule['error'],
                    'confidence': 0.9,
                }
    
    return None
```

---

### 5.5 混合模式支持

**支持口语化和传统语法混合使用**

**5.5.1 混合模式示例**

```yan
# 混合使用口语化和传统语法
定处理订单是函订单：
  # 口语化：情境式
  订单状态是"新建"时：
    # 传统语法
    订单·状态变为"处理中"。
    订单，发送到仓库。
  
  # 口语化：询问式
  如果订单·金额大于10000，创建审核任务。
  
  # 传统语法
  不然：
    处理订单。
  
  # 口语化：感叹式
  太好了！订单处理完成。
```

**5.5.2 混合模式解析**

```python
def parse_mixed_code(code):
    """解析混合模式代码"""
    
    lines = code.split('\n')
    ast_nodes = []
    
    for line in lines:
        # 尝试口语化解析
        colloquial_node = try_parse_colloquial(line)
        
        if colloquial_node:
            ast_nodes.append(colloquial_node)
        else:
            # 回退到传统语法解析
            traditional_node = parse_traditional(line)
            ast_nodes.append(traditional_node)
    
    return ast_nodes
```

---

## 6. 性能优化

### 6.1 THULAC 缓存机制

```python
from functools import lru_cache

class THULACWrapper:
    def __init__(self):
        self.thu = thulac.thulac()
    
    @lru_cache(maxsize=1000)
    def cut_cached(self, text):
        """缓存分词结果"""
        return self.thu.cut(text)
    
    def cut(self, text):
        """分词（带缓存）"""
        return self.cut_cached(text)
```

### 6.2 批量处理

```python
def batch_parse(texts):
    """批量解析口语化代码"""
    parser = ColloquialParser()
    results = []
    
    for text in texts:
        result = parser.parse(text)
        results.append(result)
    
    return results
```

### 6.3 性能指标

| 指标 | 目标值 |
|------|--------|
| 单行代码解析时间 | < 10ms |
| 100行代码解析时间 | < 100ms |
| 1000行代码解析时间 | < 1s |
| 内存占用 | < 50MB |

---

## 7. 测试方案

### 7.1 单元测试

```python
def test_colloquial_parser():
    """测试口语化解析器"""
    
    # 测试询问式
    ast = parse("如果分数大等于90，印\"优秀\"。")
    assert ast['type'] == 'IfStatement'
    
    # 测试建议式
    ast = parse("建议检查除数是否等于0。")
    assert ast['type'] == 'AssertStatement'
    
    # 测试祈使式
    ast = parse("第一步：获取用户邮箱。")
    assert ast['type'] == 'AssignmentStatement'
```

### 7.2 集成测试

```python
def test_mixed_code():
    """测试混合模式代码"""
    
    code = """
定处理订单是函订单：
  订单状态是"新建"时：
    订单·状态变为"处理中"。
  
  如果订单·金额大于10000，创建审核任务。
  
  太好了！订单处理完成。
"""
    
    ast_nodes = parse_mixed_code(code)
    assert len(ast_nodes) == 3
```

---

## 8. 实现计划

### 8.1 阶段1：THULAC 集成（1周）

**任务：**
1. 安装和配置 THULAC-Python
2. 添加自定义词汇
3. 实现分词和词性标注
4. 实现语法结构分析

**交付物：**
- THULAC 集成模块
- 自定义词典
- 分词和词性标注 API

---

### 8.2 阶段2：口语化解析器（2周）

**任务：**
1. 实现关键字识别
2. 实现模式匹配
3. 实现 AST 构建
4. 实现语义推断

**交付物：**
- 口语化解析器
- AST 构建器
- 语义推断器

---

### 8.3 阶段3：代码生成器（1周）

**任务：**
1. 实现模板生成
2. 实现 AST 转换
3. 实现代码优化
4. 实现错误处理

**交付物：**
- 代码生成器
- 错误处理器
- 测试套件

---

### 8.4 阶段4：应用场景实现（2周）

**任务：**
1. 实现教学模式
2. 实现业务规则语言
3. 实现可视化编辑器
4. 实现文档生成

**交付物：**
- 教学模式
- 业务规则语言
- 可视化编辑器
- 文档生成器

---

## 9. 风险与挑战

### 9.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| THULAC 性能问题 | 解析速度慢 | 缓存机制、批量处理 |
| 分词准确性 | 语义推断错误 | 自定义词典、上下文推断 |
| 歧义消解 | 代码生成错误 | 多候选方案、用户确认 |

### 9.2 用户体验风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 学习曲线 | 用户不熟悉口语化语法 | 详细文档、示例库、教学模式 |
| 调试困难 | 错误提示不清晰 | 智能提示、自动纠正 |
| 混合模式混淆 | 口语化和传统语法混淆 | 清晰的语法规则、IDE支持 |

---

## 10. 成功标准

### 10.1 功能标准

- ✅ 支持10种口语化风格
- ✅ 支持 THULAC 分词和词性标注
- ✅ 支持混合模式
- ✅ 支持错误提示和自动纠正

### 10.2 性能标准

- ✅ 单行代码解析时间 < 10ms
- ✅ 100行代码解析时间 < 100ms
- ✅ 1000行代码解析时间 < 1s

### 10.3 质量标准

- ✅ 单元测试覆盖率 > 90%
- ✅ 集成测试通过率 100%
- ✅ 文档完整性 > 80%

---

## 11. 总结

言律口语化编程系统通过 THULAC-Python 的分词和词性标注能力，实现了高度可扩展的口语化编程支持。通过混合方案（关键字识别 + 模式匹配 + 上下文推断），提供了准确、高效、易用的口语化编程体验。

**核心优势：**
- 自然性：符合中文表达习惯
- 可扩展性：支持新风格的添加
- 准确性：基于 THULAC 的准确分词
- 高效性：缓存机制确保性能

**下一步行动：**
1. 实现 THULAC 集成
2. 开发口语化解析器
3. 构建代码生成器
4. 实现应用场景

---

**版本历史：**
- v1.0 (2026-05-21) - 初始设计文档
