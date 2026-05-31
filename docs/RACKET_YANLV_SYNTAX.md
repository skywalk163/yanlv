# 言律语言 Racket 实现方案 - 真正的中文语法

## 🎯 核心思路

**不使用Lisp括号语法，实现真正的言律中文语法！**

关键：使用Racket的**读取器扩展（Reader Extension）**机制，自定义源代码解析。

---

## 1. 架构设计

### 1.1 三层架构

```
言律源代码 (.yan)
    ↓
[读取器层] - 中文分词 + 语法解析
    ↓
[转换层] - 言律语法 → Racket语法
    ↓
[执行层] - Racket运行时
    ↓
执行结果
```

### 1.2 文件结构

```
yanlv-racket/
├── yanlv-lang/
│   ├── main.rkt          # 语言入口
│   ├── reader.rkt        # 读取器（核心）
│   ├── parser.rkt        # 语法解析器
│   ├── tokenizer.rkt     # 中文分词
│   └── expander.rkt      # 语法扩展
├── examples/
│   ├── hello.yan         # 示例程序
│   ├── causal.yan        # 因果链示例
│   └── loop.yan          # 循环示例
└── tests/
    └── test-all.rkt      # 测试套件
```

---

## 2. 读取器实现

### 2.1 核心读取器 (reader.rkt)

```racket
#lang racket

(provide read read-syntax)

;; 读取言律源代码
(define (read in)
  (syntax->datum (read-syntax #f in)))

;; 读取语法对象
(define (read-syntax src in)
  ;; 1. 读取全部源代码
  (define source-code (port->string in))
  
  ;; 2. 中文分词
  (define tokens (tokenize-chinese source-code))
  
  ;; 3. 解析言律语法
  (define ast (parse-yanlv tokens))
  
  ;; 4. 转换为Racket语法
  (define racket-code (yanlv->racket ast))
  
  ;; 5. 返回语法对象
  (datum->syntax #f racket-code))

;; 中文分词
(define (tokenize-chinese code)
  ;; 这里需要集成中文分词库
  ;; 可以使用Racket FFI调用Python的jieba
  ;; 或者实现简单的规则分词
  (define lines (string-split code "\n"))
  (for/list ([line lines])
    (tokenize-line line)))

;; 解析言律语法
(define (parse-yanlv tokens)
  ;; 解析各种言律语法结构
  (for/list ([token-group tokens])
    (cond
      ;; 因果链：条件，动作。
      [(causal-chain? token-group)
       (parse-causal-chain token-group)]
      
      ;; 语境省略：以X为主题：
      [(context-omission? token-group)
       (parse-context-omission token-group)]
      
      ;; 循环：对于i从1到10：
      [(for-loop? token-group)
       (parse-for-loop token-group)]
      
      ;; 条件：若...就：
      [(if-simple? token-group)
       (parse-if-simple token-group)]
      
      ;; 其他语法
      [else (parse-expression token-group)])))
```

### 2.2 中文分词器 (tokenizer.rkt)

```racket
#lang racket

(provide tokenize-line)

;; 分词规则
(define keywords
  '("输出" "定义" "变量" "为" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以" "为主题"
    "大于" "小于" "等于" "加" "减" "乘" "除"
    "定" "是" "列" "算"))

;; 分词一行
(define (tokenize-line line)
  ;; 移除注释
  (define clean-line (remove-comments line))
  
  ;; 简单分词（实际应使用jieba）
  (define tokens '())
  (define current-pos 0)
  
  (while (< current-pos (string-length clean-line))
    ;; 尝试匹配关键词
    (define matched #f)
    (for ([keyword keywords])
      (when (and (not matched)
                 (string-prefix? (substring clean-line current-pos)
                                keyword))
        (set! tokens (append tokens (list (make-token keyword 'keyword))))
        (set! current-pos (+ current-pos (string-length keyword)))
        (set! matched #t)))
    
    ;; 匹配数字
    (when (not matched)
      (define num-match (regexp-match #rx"[0-9]+" 
                                      (substring clean-line current-pos)))
      (when num-match
        (set! tokens (append tokens (list (make-token (car num-match) 'number))))
        (set! current-pos (+ current-pos (string-length (car num-match))))
        (set! matched #t)))
    
    ;; 匹配字符串
    (when (not matched)
      (define str-match (regexp-match #rx"\"[^\"]*\"" 
                                      (substring clean-line current-pos)))
      (when str-match
        (set! tokens (append tokens (list (make-token (car str-match) 'string))))
        (set! current-pos (+ current-pos (string-length (car str-match))))
        (set! matched #t)))
    
    ;; 跳过空白
    (when (not matched)
      (set! current-pos (+ current-pos 1))))
  
  tokens)

;; Token结构
(struct token (value type) #:transparent)
(define (make-token value type)
  (token value type))
```

### 2.3 语法解析器 (parser.rkt)

```racket
#lang racket

(provide parse-causal-chain
         parse-context-omission
         parse-for-loop
         parse-if-simple)

;; 解析因果链：条件，动作。
(define (parse-causal-chain tokens)
  ;; 格式：条件 ， 动作 。
  (define comma-pos (find-token tokens "，"))
  (define period-pos (find-token tokens "。"))
  
  (define condition (take tokens comma-pos))
  (define action (take (drop tokens (+ comma-pos 1)) 
                       (- period-pos comma-pos 1)))
  
  `(causal-chain ,condition ,action))

;; 解析语境省略：以X为主题：
(define (parse-context-omission tokens)
  ;; 格式：以 主题 为 主题名 ：
  (define theme-pos (find-token tokens "为主题"))
  (define colon-pos (find-token tokens "："))
  
  (define theme-name (list-ref tokens (- theme-pos 1)))
  (define body (drop tokens (+ colon-pos 1)))
  
  `(context-omission ,theme-name ,body))

;; 解析循环：对于i从1到10：
(define (parse-for-loop tokens)
  ;; 格式：对于 变量 从 起点 到 终点 ：
  (define var-pos (find-token tokens "对于"))
  (define from-pos (find-token tokens "从"))
  (define to-pos (find-token tokens "到"))
  (define colon-pos (find-token tokens "："))
  
  (define var (list-ref tokens (+ var-pos 1)))
  (define start (list-ref tokens (+ from-pos 1)))
  (define end (list-ref tokens (+ to-pos 1)))
  (define body (drop tokens (+ colon-pos 1)))
  
  `(for-loop ,var ,start ,end ,body))

;; 解析条件：若...就：
(define (parse-if-simple tokens)
  ;; 格式：若 条件 就 ：
  (define if-pos (find-token tokens "若"))
  (define then-pos (find-token tokens "就"))
  (define colon-pos (find-token tokens "："))
  
  (define condition (take (drop tokens (+ if-pos 1)) 
                          (- then-pos if-pos 1)))
  (define body (drop tokens (+ colon-pos 1)))
  
  `(if-simple ,condition ,body))
```

### 2.4 语法转换器 (expander.rkt)

```racket
#lang racket

(provide yanlv->racket)

;; 言律语法 → Racket语法
(define (yanlv->racket ast)
  (match ast
    ;; 因果链转换
    [`(causal-chain ,condition ,action)
     `(when ,(condition->racket condition)
        ,(action->racket action))]
    
    ;; 语境省略转换
    [`(context-omission ,theme-name ,body)
     `(let ([当前主题 ,theme-name])
        ,@(map yanlv->racket body))]
    
    ;; 循环转换
    [`(for-loop ,var ,start ,end ,body)
     `(for ([,var (in-range ,start (+ ,end 1))])
        ,@(map yanlv->racket body))]
    
    ;; 条件转换
    [`(if-simple ,condition ,body)
     `(when ,(condition->racket condition)
        ,@(map yanlv->racket body))]
    
    ;; 输出语句
    [`(output ,content)
     `(displayln ,content)]
    
    ;; 变量定义
    [`(define-var ,name ,value)
     `(define ,name ,value)]
    
    ;; 其他表达式
    [else ast]))

;; 条件转换
(define (condition->racket condition)
  (match condition
    [`(大于 ,x ,y) `(> ,x ,y)]
    [`(小于 ,x ,y) `(< ,x ,y)]
    [`(等于 ,x ,y) `(= ,x ,y)]
    [else condition]))

;; 动作转换
(define (action->racket action)
  (yanlv->racket action))
```

---

## 3. 语言入口 (main.rkt)

```racket
#lang racket

;; 言律语言主模块
(module reader syntax/module-reader
  yanlv-lang)

;; 提供所有语法形式
(provide (all-from-out racket)
         (rename-out [displayln 输出]
                     [define 定义]))

;; 因果链宏
(define-syntax-rule (条件 ， 动作 。)
  (when 条件 动作))

;; 循环宏
(define-syntax 对于
  (syntax-rules (从 到)
    [(_ 变量 从 起点 到 终点 ： 主体 ...)
     (for ([变量 (in-range 起点 (+ 终点 1))])
       主体 ...)]))

;; 条件宏
(define-syntax 若
  (syntax-rules (就)
    [(_ 条件 就 ： 主体 ...)
     (when 条件 主体 ...)]))
```

---

## 4. 完整示例

### 4.1 因果链示例 (causal.yan)

```言律
# 智能家居控制
温度大于28，开启空调制冷。
温度小于20，开启空调制热。
温度在20到28之间，关闭空调。

湿度大于70，开启除湿机。
湿度小于40，开启加湿器。

光线为"昏暗"且有人，开启灯光。
光线为"明亮"，关闭灯光。
```

**转换后的Racket代码：**

```racket
#lang racket

(when (> 温度 28) (开启空调制冷))
(when (< 温度 20) (开启空调制热))
(when (and (>= 温度 20) (<= 温度 28)) (关闭空调))

(when (> 湿度 70) (开启除湿机))
(when (< 湿度 40) (开启加湿器))

(when (and (string=? 光线 "昏暗") 有人) (开启灯光))
(when (string=? 光线 "明亮") (关闭灯光))
```

### 4.2 循环示例 (loop.yan)

```言律
# 计算1到100的和
定总和是0。
对于i从1到100：
  定总和是总和加i。

输出 "1到100的和："
输出 总和
```

**转换后的Racket代码：**

```racket
#lang racket

(define 总和 0)
(for ([i (in-range 1 101)])
  (set! 总和 (+ 总和 i)))

(displayln "1到100的和：")
(displayln 总和)
```

### 4.3 语境省略示例 (context.yan)

```言律
# 订单处理
以订单为主题：
  验证。
  处理。
  发货。

# 用户信息
以张三为主题：
  姓名，印。
  年龄，印。
  城市，印。
```

**转换后的Racket代码：**

```racket
#lang racket

(let ([当前主题 订单])
  (验证)
  (处理)
  (发货))

(let ([当前主题 张三])
  (displayln 姓名)
  (displayln 年龄)
  (displayln 城市))
```

---

## 5. 实现步骤

### 步骤1：基础读取器

```racket
;; 创建 yanlv-lang/reader.rkt
;; 实现基本的中文分词和语法识别
```

### 步骤2：语法解析

```racket
;; 创建 yanlv-lang/parser.rkt
;; 实现因果链、循环、条件等语法解析
```

### 步骤3：语法转换

```racket
;; 创建 yanlv-lang/expander.rkt
;; 将言律语法转换为Racket代码
```

### 步骤4：测试验证

```racket
;; 创建测试用例
;; 验证各种言律语法正确转换
```

---

## 6. 关键技术点

### 6.1 中文分词

**方案1：集成jieba**
```racket
;; 使用Racket FFI调用Python jieba
(define (tokenize-with-jieba text)
  (define python-code 
    (format "import jieba; print(list(jieba.cut('~a')))" text))
  (define result (system python-code))
  (parse-jieba-result result))
```

**方案2：规则分词**
```racket
;; 基于关键词的简单分词
(define (tokenize-by-rules text)
  ;; 优先匹配长关键词
  ;; 然后匹配短关键词
  ;; 最后匹配标识符和数字
  )
```

### 6.2 缩进处理

```racket
;; 处理Python风格的缩进
(define (parse-indentation lines)
  (define indent-stack '())
  (for/list ([line lines])
    (define indent (count-leading-spaces line))
    (cond
      [(> indent (car indent-stack))
       ;; 进入新块
       (set! indent-stack (cons indent indent-stack))
       'enter-block]
      [(< indent (car indent-stack))
       ;; 退出块
       (set! indent-stack (cdr indent-stack))
       'exit-block]
      [else 'same-block])))
```

### 6.3 错误处理

```racket
;; 提供友好的错误信息
(define (yanlv-error msg tokens pos)
  (error '言律语言
         (format "~a\n位置：第~a行\n代码：~a"
                 msg
                 (token-line (list-ref tokens pos))
                 (token-value (list-ref tokens pos)))))
```

---

## 7. 优势分析

### 7.1 相比Lisp括号语法

| 特性 | Lisp括号语法 | 言律中文语法 |
|------|-------------|-------------|
| 可读性 | 中等 | **优秀** |
| 学习曲线 | 陡峭 | **平缓** |
| 语法自然度 | 低 | **高** |
| 实现复杂度 | 简单 | 中等 |
| 性能 | 快 | **快** |

### 7.2 技术优势

1. **真正的中文语法** - 不是Lisp的变体
2. **自然表达** - 像说话一样编程
3. **Racket性能** - 继承Racket的优秀性能
4. **宏系统** - 保留Racket的强大宏
5. **工具链** - 复用Racket的工具

---

## 8. 实施计划

### 阶段1：原型验证（1周）

- ✅ 设计架构
- 🔄 实现基础读取器
- 🔄 实现简单分词
- 🔄 实现因果链语法

### 阶段2：核心功能（2-3周）

- 📅 实现循环语法
- 📅 实现条件语法
- 📅 实现语境省略
- 📅 实现数组操作

### 阶段3：完善优化（2-4周）

- 📅 集成jieba分词
- 📅 错误处理
- 📅 性能优化
- 📅 文档完善

---

## 9. 示例对比

### Python实现

```python
# 需要完整的解释器
温度 = 30
if 温度 > 28:
    print("开启空调")
```

### Racket Lisp语法

```racket
# 不够自然
(定义 变量 温度 为 30)
(如果 (大于 温度 28) 则
      (输出 "开启空调"))
```

### Racket 言律语法 ✅

```言律
# 真正的言律语法！
定温度是30。
温度大于28，输出"开启空调"。
```

**这才是我们想要的！**

---

## 10. 结论

**完全可行！而且更好！**

通过Racket的读取器扩展机制，我们可以：
- ✅ 实现真正的言律中文语法
- ✅ 不使用Lisp括号
- ✅ 保持自然语言风格
- ✅ 继承Racket的优秀性能
- ✅ 利用Racket的强大工具链

**这是实现言律语言的最佳方案！**

🎯
