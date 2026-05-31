#lang racket

;; ========================================
;; 言律语言读取器原型 - 简化版
;; 实现真正的中文语法
;; ========================================

(provide read read-syntax)

;; ========================================
;; 1. Token结构
;; ========================================

(struct token (value type line col) #:transparent)

;; ========================================
;; 2. 中文分词器
;; ========================================

(define keywords
  '("输出" "定义" "变量" "为" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以" "为主题"
    "大于" "小于" "等于" "大于等于" "小于等于"
    "加" "减" "乘" "除"
    "定" "是" "列" "算" "且" "或"
    "当" "时" "返回"))

;; 分词一行
(define (tokenize-line line line-num)
  (define tokens '())
  (define col 0)
  (define len (string-length line))
  
  ;; 跳过注释
  (cond
    [(string-prefix? line "#") '()]
    [else
     ;; 简单分词：按空格和标点分割
     (define parts (string-split line " "))
     (for/list ([part parts])
       (cond
         ;; 字符串
         [(regexp-match? #rx"\".*\"" part)
          (token part 'string line-num col)]
         ;; 数字
         [(regexp-match? #rx"[0-9]+" part)
          (token part 'number line-num col)]
         ;; 关键词
         [(member part keywords)
          (token part 'keyword line-num col)]
         ;; 标点
         [(or (string=? part "，") (string=? part "。")
              (string=? part "：") (string=? part "、"))
          (token part 'punctuation line-num col)]
         ;; 标识符
         [else
          (token part 'identifier line-num col)]))]))

;; ========================================
;; 3. 语法解析器
;; ========================================

;; 解析因果链：条件，动作。
(define (parse-causal-chain tokens)
  (define comma-pos (find-token-index tokens "，"))
  (define period-pos (find-token-index tokens "。"))
  
  (if (and comma-pos period-pos)
      (let* ([condition-tokens (take tokens comma-pos)]
             [action-tokens (take (drop tokens (+ comma-pos 1)) 
                                 (- period-pos comma-pos 1))])
        `(when ,(parse-condition condition-tokens)
           ,(parse-action action-tokens)))
      #f))

;; 解析条件
(define (parse-condition tokens)
  (cond
    ;; 大于
    [(find-token-index tokens "大于")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(> ,left ,right)))]
    
    ;; 小于
    [(find-token-index tokens "小于")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(< ,left ,right)))]
    
    ;; 等于
    [(find-token-index tokens "等于")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(= ,left ,right)))]
    
    ;; 其他
    [else (parse-expression tokens)]))

;; 解析动作
(define (parse-action tokens)
  (cond
    ;; 输出
    [(and (not (null? tokens))
          (string=? (token-value (car tokens)) "输出"))
     (let ([content (parse-expression (cdr tokens))])
       `(displayln ,content))]
    
    ;; 其他
    [else (parse-expression tokens)]))

;; 解析表达式
(define (parse-expression tokens)
  (cond
    [(null? tokens) #f]
    
    ;; 单个token
    [(= (length tokens) 1)
     (let ([t (car tokens)])
       (cond
         [(eq? (token-type t) 'number)
          (string->number (token-value t))]
         [(eq? (token-type t) 'string)
          (token-value t)]
         [else
          (string->symbol (token-value t))]))]
    
    ;; 加法
    [(find-token-index tokens "加")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(+ ,left ,right)))]
    
    ;; 减法
    [(find-token-index tokens "减")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(- ,left ,right)))]
    
    ;; 乘法
    [(find-token-index tokens "乘")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(* ,left ,right)))]
    
    ;; 除法
    [(find-token-index tokens "除")
     => (λ (pos)
          (let ([left (parse-expression (take tokens pos))]
                [right (parse-expression (drop tokens (+ pos 1)))])
            `(/ ,left ,right)))]
    
    [else
     (string->symbol (token-value (car tokens)))]))

;; ========================================
;; 4. 辅助函数
;; ========================================

(define (find-token-index tokens value)
  (for/first ([t tokens]
              [i (in-naturals)]
              #:when (string=? (token-value t) value))
    i))

;; ========================================
;; 5. 主读取函数
;; ========================================

(define (read in)
  (syntax->datum (read-syntax #f in)))

(define (read-syntax src in)
  ;; 读取源代码
  (define source (port->string in))
  (define lines (string-split source "\n"))
  
  ;; 分词所有行
  (define all-tokens
    (for/list ([line lines]
               [line-num (in-naturals 1)])
      (tokenize-line line line-num)))
  
  ;; 解析语法
  (define racket-code
    (for/list ([line-tokens all-tokens]
               #:when (not (null? line-tokens)))
      (cond
        ;; 因果链
        [(and (find-token-index line-tokens "，")
              (find-token-index line-tokens "。"))
         (parse-causal-chain line-tokens)]
        
        ;; 输出语句
        [(and (not (null? line-tokens))
              (string=? (token-value (car line-tokens)) "输出"))
         (let ([content (parse-expression (cdr line-tokens))])
           `(displayln ,content))]
        
        ;; 变量定义
        [(and (find-token-index line-tokens "定")
              (find-token-index line-tokens "是"))
         (let* ([name-pos (find-token-index line-tokens "定")]
                [value-pos (find-token-index line-tokens "是")]
                [var-name (token-value (list-ref line-tokens (+ name-pos 1)))]
                [var-value (parse-expression (drop line-tokens (+ value-pos 1)))])
           `(define ,(string->symbol var-name) ,var-value))]
        
        ;; 其他
        [else #f])))
  
  ;; 过滤掉#f
  (define filtered-code (filter identity racket-code))
  
  ;; 包装成begin块
  (define final-code
    (if (= (length filtered-code) 1)
        (car filtered-code)
        `(begin ,@filtered-code)))
  
  ;; 返回语法对象
  (datum->syntax #f final-code))
