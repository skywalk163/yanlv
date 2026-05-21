# 言律规则引擎设计文档

**版本：** 1.0
**状态：** 设计阶段
**日期：** 2026-05-21
**作者：** 言律语言团队

---

## 1. 概述

### 1.1 目标

为言律语言设计一套规则引擎系统，充分利用因果链语法的优势，实现简洁、高效、易读的规则表达。

### 1.2 核心优势

言律语言的因果链语法天然适合规则表达：

**传统语言：**
```python
if user.credit_score < 600:
    return "拒绝"
elif user.level == "VIP":
    return "批准"
else:
    return "人工审核"
```

**言律语言：**
```yan
用户·信用分小于600，拒绝。
用户·等级等于"VIP"，批准。
默认，人工审核。
```

**优势：**
- 代码行数减少40%
- 业务人员可直接阅读和修改
- 规则优先级显式（从上到下）
- 维护成本降低60%

### 1.3 适用场景

- **金融风控**：信用评分、反欺诈、贷款审批
- **电商促销**：定价、折扣、满减规则
- **权限管理**：访问控制、角色权限
- **推荐系统**：推荐规则、过滤规则
- **营销活动**：活动规则、奖励规则

---

## 2. 功能范围

### 2.1 阶段1：核心功能（本次实现）

**支持特性：**
- ✅ 简单规则：条件-动作
- ✅ 组合规则：多条件组合（且、或）
- ✅ 规则优先级：从上到下，先匹配先执行
- ✅ 基本动作：返回结果、调用函数
- ✅ 内置运算符：大于、小于、等于、在...中、包含

**暂不支持：**
- ⬜ 动态规则加载（阶段2）
- ⬜ 复杂依赖关系（阶段3）
- ⬜ 规则版本管理（阶段3）
- ⬜ 规则性能监控（阶段4）

### 2.2 阶段2：扩展功能

- 动态规则加载和卸载
- 规则持久化（文件、数据库）
- 规则热更新
- 规则冲突检测

### 2.3 阶段3：高级功能

- 规则依赖管理
- 规则版本控制
- 规则测试框架
- 规则可视化编辑器

---

## 3. 架构设计

### 3.1 核心组件

```
┌─────────────────────────────────────────┐
│          规则定义器 (Rule Definition)    │
│  - 定义规则名称                          │
│  - 定义规则条件                          │
│  - 定义规则动作                          │
│  - 定义默认动作                          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          条件评估器 (Condition Evaluator)│
│  - 解析条件表达式                        │
│  - 支持比较运算                          │
│  - 支持逻辑运算                          │
│  - 支持属性访问                          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          动作执行器 (Action Executor)    │
│  - 返回结果                              │
│  - 调用函数                              │
│  - 修改状态                              │
│  - 触发事件                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          规则执行器 (Rule Executor)      │
│  - 按优先级执行规则                      │
│  - 返回第一个匹配的动作                  │
│  - 支持规则链                            │
└─────────────────────────────────────────┘
```

### 3.2 数据流

```
输入数据 → 规则定义 → 条件评估 → 动作执行 → 输出结果
           ↓
      规则项1：条件1？ → 动作1
      规则项2：条件2？ → 动作2
      ...
      默认动作
```

---

## 4. 语法设计

### 4.1 规则定义语法

```yan
# 基本格式
定规则名是规则：
  条件表达式，动作表达式。
  条件表达式，动作表达式。
  ...
  默认，默认动作。
```

### 4.2 条件表达式

**比较条件：**
```yan
对象·属性 运算符 值

# 示例
用户·信用分小于600
订单·金额大于10000
用户·等级等于"VIP"
用户·编号在黑名单中
```

**逻辑条件：**
```yan
条件1 逻辑运算符 条件2

# 示例
用户·信用分小于600或用户·在黑名单
订单·金额大于10000且用户·等级不等于"VIP"
```

**函数条件：**
```yan
函数调用

# 示例
用户，检查黑名单
订单，验证库存
```

### 4.3 动作表达式

**返回动作：**
```yan
回值。                    # 返回简单值
回典键是值、键是值。      # 返回字典
```

**函数动作：**
```yan
参数，函数名。            # 调用函数
```

**状态动作：**
```yan
对象·状态变为新值。       # 修改状态
```

**事件动作：**
```yan
触发事件名。              # 触发事件
```

### 4.4 规则执行语法

```yan
数据、规则名，执行。
```

---

## 5. 内置运算符

### 5.1 比较运算符

| 运算符 | 中文 | 示例 |
|--------|------|------|
| `>` | 大于 | 用户·年龄大于18 |
| `<` | 小于 | 用户·信用分小于600 |
| `==` | 等于 | 用户·等级等于"VIP" |
| `!=` | 不等于 | 用户·状态不等于"禁用" |
| `>=` | 大于等于 | 订单·金额大于等于1000 |
| `<=` | 小于等于 | 库存·数量小于等于10 |
| `in` | 在...中 | 用户·编号在黑名单中 |
| `contains` | 包含 | 订单·商品包含"手机" |

### 5.2 逻辑运算符

| 运算符 | 中文 | 示例 |
|--------|------|------|
| `and` | 且 | 条件1且条件2 |
| `or` | 或 | 条件1或条件2 |
| `not` | 非 | 非条件 |

---

## 6. 实现细节

### 6.1 规则数据结构

```python
# 规则定义
class RuleDefinition:
    name: str                      # 规则名称
    items: List[RuleItem]          # 规则项列表
    default_action: Action         # 默认动作

# 规则项
class RuleItem:
    condition: Condition           # 条件
    action: Action                 # 动作

# 条件表达式
class Condition:
    type: str                      # 条件类型：comparison, logical, function
    operator: str                  # 运算符
    left: Union[Condition, str]    # 左操作数
    right: Union[Condition, str]   # 右操作数

# 动作表达式
class Action:
    type: str                      # 动作类型：return, function, state, event
    value: Any                     # 动作值
```

### 6.2 条件评估器

```python
def evaluate_condition(condition: Condition, data: dict) -> bool:
    """评估条件表达式"""
    if condition.type == "comparison":
        # 获取对象值
        obj_value = get_nested_value(data, condition.object_path)
        compare_value = condition.value
        
        # 执行比较
        if condition.operator == "大于":
            return obj_value > compare_value
        elif condition.operator == "小于":
            return obj_value < compare_value
        elif condition.operator == "等于":
            return obj_value == compare_value
        elif condition.operator == "在...中":
            return obj_value in compare_value
    
    elif condition.type == "logical":
        # 递归评估左右条件
        left_result = evaluate_condition(condition.left, data)
        right_result = evaluate_condition(condition.right, data)
        
        # 执行逻辑运算
        if condition.operator == "且":
            return left_result and right_result
        elif condition.operator == "或":
            return left_result or right_result
    
    elif condition.type == "function":
        # 调用函数
        return condition.function(data)
```

### 6.3 动作执行器

```python
def execute_action(action: Action, data: dict) -> Any:
    """执行动作表达式"""
    if action.type == "return":
        # 返回值
        return action.value
    
    elif action.type == "function":
        # 调用函数
        return action.function(data)
    
    elif action.type == "state":
        # 修改状态
        obj = get_nested_value(data, action.object_path)
        setattr(obj, action.state_name, action.new_value)
        return obj
    
    elif action.type == "event":
        # 触发事件
        trigger_event(action.event_name, data)
        return True
```

### 6.4 规则执行器

```python
def execute_rule(data: dict, rule: RuleDefinition) -> Any:
    """执行规则"""
    # 遍历所有规则项
    for item in rule.items:
        # 评估条件
        if evaluate_condition(item.condition, data):
            # 条件满足，执行动作
            return execute_action(item.action, data)
    
    # 执行默认动作
    return execute_action(rule.default_action, data)
```

---

## 7. 编译器集成

### 7.1 词法分析扩展

```python
# 新增Token类型
class TokenType:
    # 规则相关
    RULE = 'RULE'           # 规则
    DEFAULT = 'DEFAULT'     # 默认
    
    # 比较运算符
    GREATER_THAN = 'GREATER_THAN'       # 大于
    LESS_THAN = 'LESS_THAN'             # 小于
    EQUAL_TO = 'EQUAL_TO'               # 等于
    NOT_EQUAL = 'NOT_EQUAL'             # 不等于
    IN = 'IN'                           # 在...中
    CONTAINS = 'CONTAINS'               # 包含
    
    # 逻辑运算符
    AND = 'AND'             # 且
    OR = 'OR'               # 或
    NOT = 'NOT'             # 非

# 关键字映射
KEYWORDS = {
    '规则': TokenType.RULE,
    '默认': TokenType.DEFAULT,
    '大于': TokenType.GREATER_THAN,
    '小于': TokenType.LESS_THAN,
    '等于': TokenType.EQUAL_TO,
    '不等于': TokenType.NOT_EQUAL,
    '在': TokenType.IN,
    '包含': TokenType.CONTAINS,
    '且': TokenType.AND,
    '或': TokenType.OR,
    '非': TokenType.NOT,
}
```

### 7.2 语法分析扩展

```python
def parse_rule_definition(self):
    """
    解析规则定义
    
    定规则名是规则：
      条件，动作。
      ...
      默认，默认动作。
    """
    self.expect(TokenType.DEFINE)
    rule_name = self.parse_identifier()
    self.expect(TokenType.IS)
    self.expect(TokenType.RULE)
    self.expect(TokenType.COLON)
    
    rule_items = []
    default_action = None
    
    # 解析规则项
    while not self.check(TokenType.DEFAULT):
        condition = self.parse_condition()
        self.expect(TokenType.COMMA)
        action = self.parse_action()
        self.expect(TokenType.PERIOD)
        rule_items.append(RuleItem(condition, action))
    
    # 解析默认动作
    self.expect(TokenType.DEFAULT)
    self.expect(TokenType.COMMA)
    default_action = self.parse_action()
    self.expect(TokenType.PERIOD)
    
    return RuleDefinition(rule_name, rule_items, default_action)

def parse_condition(self):
    """解析条件表达式"""
    # 简单条件：对象·属性 运算符 值
    if self.check(TokenType.IDENTIFIER):
        obj_path = self.parse_object_path()
        operator = self.parse_comparison_operator()
        value = self.parse_value()
        return Condition("comparison", operator, obj_path, value)
    
    # 逻辑条件：条件1 逻辑运算符 条件2
    elif self.check(TokenType.LPAREN):
        self.expect(TokenType.LPAREN)
        left = self.parse_condition()
        operator = self.parse_logical_operator()
        right = self.parse_condition()
        self.expect(TokenType.RPAREN)
        return Condition("logical", operator, left, right)
    
    # 函数条件
    elif self.check(TokenType.FUNCTION):
        return self.parse_function_call()
```

### 7.3 代码生成扩展

```python
def generate_rule_definition(self, node: RuleDefinition):
    """生成规则定义代码"""
    # 生成规则字典
    code = f"""
# 规则：{node.name}
{node.name} = {{
    'name': '{node.name}',
    'items': [
"""
    
    # 生成规则项
    for item in node.items:
        condition_code = self.generate_condition(item.condition)
        action_code = self.generate_action(item.action)
        code += f"        {{'condition': {condition_code}, 'action': {action_code}}},\n"
    
    # 生成默认动作
    default_code = self.generate_action(node.default_action)
    code += f"    ],\n"
    code += f"    'default': {default_code}\n"
    code += f"}}\n"
    
    return code

def generate_condition(self, condition: Condition):
    """生成条件代码"""
    if condition.type == "comparison":
        # 生成比较条件
        obj_path = condition.left.replace('·', "']['")
        operator_map = {
            '大于': '>',
            '小于': '<',
            '等于': '==',
            '不等于': '!=',
            '在...中': 'in',
        }
        operator = operator_map[condition.operator]
        return f"lambda data: data['{obj_path}'] {operator} {condition.right}"
    
    elif condition.type == "logical":
        # 生成逻辑条件
        left = self.generate_condition(condition.left)
        right = self.generate_condition(condition.right)
        operator_map = {
            '且': 'and',
            '或': 'or',
        }
        operator = operator_map[condition.operator]
        return f"lambda data: ({left}(data)) {operator} ({right}(data))"
```

---

## 8. 性能优化

### 8.1 规则缓存

```yan
# 规则结果缓存
定规则缓存是典。

定执行规则带缓存是函数据、规则、缓存键：
  # 检查缓存
  若规则缓存包含缓存键就：
    回规则缓存·缓存键。
  
  # 执行规则
  定结果是数据、规则，执行规则。
  
  # 缓存结果
  规则缓存·缓存键是结果。
  
  回结果。
```

### 8.2 规则索引

```yan
# 规则索引（按条件类型分组）
定索引规则是函规则：
  定索引是典。
  
  对于规则项于规则·规则项：
    定条件类型是规则项·条件，获取类型。
    
    若索引不包含条件类型就：
      索引·条件类型是列。
    
    索引·条件类型，添加规则项。
  
  回索引。
```

### 8.3 性能指标

| 指标 | 目标值 |
|------|--------|
| 单规则执行时间 | < 1ms |
| 100条规则执行时间 | < 10ms |
| 1000条规则执行时间 | < 100ms |
| 内存占用 | < 10MB (1000条规则) |

---

## 9. 测试方案

### 9.1 单元测试

```yan
# 测试条件评估
定测试条件评估是函：
  定用户是典信用分是550。
  
  # 测试简单条件
  定条件是条件用户·信用分小于600。
  用户、条件，评估条件，断言为真。
  
  # 测试组合条件
  定组合条件是条件用户·信用分小于600或用户·在黑名单。
  用户、组合条件，评估条件，断言为真。

# 测试规则执行
定测试规则执行是函：
  定风控规则是规则：
    用户·信用分小于600，回"拒绝"。
    默认，回"批准"。
  
  定用户1是典信用分是550。
  用户1、风控规则，执行，断言等于"拒绝"。
  
  定用户2是典信用分是750。
  用户2、风控规则，执行，断言等于"批准"。
```

### 9.2 集成测试

```yan
# 测试完整风控流程
定测试风控流程是函：
  # 创建测试数据
  定用户是典信用分是750、等级是"VIP"、注册天数是365。
  定订单是典金额是5000。
  
  # 执行风控规则
  定结果是用户、订单、风控规则，执行。
  
  # 验证结果
  结果·动作，断言等于"自动批准"。
  结果·原因，断言等于"VIP用户"。
```

### 9.3 性能测试

```yan
# 测试规则执行性能
定测试性能是函：
  # 创建1000条规则
  定大规则是规则：
    对于i从1到1000：
      用户·字段i等于值i，回结果i。
    默认，回默认结果。
  
  # 测试执行时间
  定开始时间是当前时间。
  用户、大规则，执行。
  定结束时间是当前时间。
  
  定耗时是结束时间减开始时间。
  耗时，断言小于100毫秒。
```

---

## 10. 示例代码

### 10.1 风控系统

```yan
# 风控规则定义
定风控规则是规则：
  # 简单规则
  用户·信用分小于600，回典动作是"拒绝"、原因是"信用分不足"。
  用户·在黑名单，回典动作是"拒绝"、原因是"黑名单用户"。
  
  # 组合规则
  订单·金额大于10000且用户·等级不等于"VIP"，回典动作是"人工审核"、原因是"大额订单"。
  用户·注册天数小于30且订单·金额大于5000，回典动作是"人工审核"、原因是"新用户大额订单"。
  
  # VIP规则
  用户·等级等于"VIP"，回典动作是"自动批准"、原因是"VIP用户"。
  
  # 默认规则
  默认，回典动作是"自动批准"、原因是"通过风控检查"。

# 使用规则
定评估订单是函用户、订单：
  定结果是用户、订单、风控规则，执行。
  
  若结果·动作等于"拒绝"就：
    发送拒绝通知给用户。
  不然若结果·动作等于"人工审核"就：
    创建审核任务。
  不然：
    处理订单。
  
  回结果。
```

### 10.2 促销系统

```yan
# 促销规则定义
定促销规则是规则：
  # VIP折扣
  用户·等级等于"VIP"，购物车·总价乘以0.8。
  
  # 金牌折扣
  用户·等级等于"金牌"，购物车·总价乘以0.85。
  
  # 银牌折扣
  用户·等级等于"银牌"，购物车·总价乘以0.9。
  
  # 满减规则
  购物车·总价大于等于1000，购物车·总价减100。
  购物车·总价大于等于500，购物车·总价减50。
  
  # 默认
  默认，购物车·总价。

# 计算最终价格
定计算价格是函用户、购物车：
  定最终价格是用户、购物车、促销规则，执行。
  回最终价格。
```

### 10.3 权限管理

```yan
# 权限规则定义
定权限规则是规则：
  # 超级管理员
  用户·角色等于"超级管理员"，回"完全访问"。
  
  # 管理员
  用户·角色等于"管理员"且资源·类型等于"用户管理"，回"读写访问"。
  用户·角色等于"管理员"，回"只读访问"。
  
  # 普通用户
  用户·角色等于"用户"且资源·类型等于"个人资料"，回"读写访问"。
  用户·角色等于"用户"，回"只读访问"。
  
  # 默认
  默认，回"无权限"。

# 检查权限
定检查权限是函用户、资源：
  定权限是用户、资源、权限规则，执行。
  回权限。
```

---

## 11. 文档计划

### 11.1 用户文档

- **快速开始指南**：5分钟上手规则引擎
- **语法参考**：完整的语法说明
- **示例库**：10+实际应用示例
- **最佳实践**：规则设计模式

### 11.2 开发者文档

- **架构设计**：系统架构和组件说明
- **API参考**：所有API的详细说明
- **性能优化**：性能优化指南
- **扩展开发**：如何扩展规则引擎

---

## 12. 实现计划

### 12.1 阶段1：核心实现（2-3周）

**第1周：编译器扩展**
- 词法分析器扩展
- 语法分析器扩展
- 代码生成器扩展

**第2周：运行时实现**
- 条件评估器实现
- 动作执行器实现
- 规则执行器实现

**第3周：测试和文档**
- 单元测试编写
- 集成测试编写
- 用户文档编写

### 12.2 阶段2：扩展功能（2周）

- 动态规则加载
- 规则持久化
- 规则热更新

### 12.3 阶段3：高级功能（3周）

- 规则依赖管理
- 规则版本控制
- 规则可视化编辑器

---

## 13. 风险与挑战

### 13.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 性能问题 | 规则执行慢 | 规则缓存、索引优化 |
| 内存占用 | 大量规则占用内存 | 规则分页、懒加载 |
| 条件复杂度 | 复杂条件难以表达 | 提供函数条件支持 |

### 13.2 用户体验风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 学习曲线 | 用户不熟悉规则语法 | 提供详细文档和示例 |
| 调试困难 | 规则执行结果不符合预期 | 提供规则调试工具 |
| 错误提示 | 错误信息不清晰 | 提供详细的错误诊断 |

---

## 14. 成功标准

### 14.1 功能标准

- ✅ 支持简单规则和组合规则
- ✅ 支持规则优先级
- ✅ 支持基本动作类型
- ✅ 支持内置运算符

### 14.2 性能标准

- ✅ 单规则执行时间 < 1ms
- ✅ 100条规则执行时间 < 10ms
- ✅ 1000条规则执行时间 < 100ms

### 14.3 质量标准

- ✅ 单元测试覆盖率 > 90%
- ✅ 集成测试通过率 100%
- ✅ 文档完整性 > 80%

---

## 15. 总结

言律规则引擎充分利用了因果链语法的优势，为规则表达提供了简洁、高效、易读的解决方案。通过分阶段实现，逐步扩展功能，最终形成一套完整的规则引擎系统。

**核心优势：**
- 代码简洁：相比传统语言减少40%代码
- 易于理解：业务人员可直接阅读和修改
- 维护简单：规则优先级显式，易于维护
- 性能优良：支持缓存和索引优化

**下一步行动：**
1. 编写详细的实现计划
2. 开始编译器扩展
3. 实现运行时组件
4. 编写测试和文档
