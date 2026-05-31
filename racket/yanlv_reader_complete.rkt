#lang racket

;; ========================================
;; 言律语言完整读取器 - 简化版
;; ========================================

(provide read read-syntax)

;; Token结构
(struct token (value type line col) #:transparent)

;; 关键词列表
(define keywords
  '("输出" "定义" "变量" "为" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以" "为主题"
    "大于" "小于" "等于" "大于等于" "小于等于"
    "加" "减" "乘" "除" "不等于"
    "定" "是" "列" "算" "且" "或" "在" "之间"
    "当" "时" "返回" "印"))

;; 分词一行
(define (tokenize-line line line-num)
  (define trimmed (string-trim line))
  (cond
    ;; 跳过空行和注释
    [(or (string=? trimmed "")
         (string-prefix? trimmed "#"))
     '()]
    [else
     ;; 简单分词：按空格分割
     (define parts (string-split trimmed))
     (for/list ([part parts]
                [i (in-naturals)])
       (cond
         ;; 字符串
         [(and (string-prefix? part "\"")
               (string-suffix? part "\""))
          (token part 'string line-num i)]
         ;; 数字
         [(regexp-match? #rx"^-?[0-9]+\\.?[0-9]*$" part)
          (token part 'number line-num i)]
         ;; 关键词
         [(member part keywords)
          (token part 'keyword line-num i)]
         ;; 标点
         [(or (string=? part "，") (string=? part "。")
              (string=? part "：") (string=? part "、"))
          (token part 'punctuation line-num i)]
         ;; 标识符
         [else
          (token part 'identifier line-num i)]))]))

;; 查找token位置
(define (find-token-index tokens value)
  (for/first ([t tokens]
              [i (in-naturals)]
              #:when (string=? (token-value t) value))
    i))

;; 解析表达式
(define (parse-expression tokens)
  (cond
    [(null? tokens) #f]
    [(= (length tokens) 1)
     (define t (car tokens))
     (cond
       [(eq? (token-type t) 'number)
        (string->number (token-value t))]
       [(eq? (token-type t) 'string)
        (define str (token-value t))
        (substring str 1 (- (string-length str) 1))]
       [else
        (string->symbol (token-value t))])]
    ;; 加法
    [(find-token-index tokens "加")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(+ ,left ,right))]
    ;; 减法
    [(find-token-index tokens "减")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(- ,left ,right))]
    ;; 乘法
    [(find-token-index tokens "乘")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(* ,left ,right))]
    ;; 除法
    [(find-token-index tokens "除")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(/ ,left ,right))]
    [else
     (string->symbol (token-value (car tokens)))]))

;; 解析条件
(define (parse-condition tokens)
  (cond
    [(null? tokens) #f]
    ;; 且
    [(find-token-index tokens "且")
     => (λ (pos)
          (define left (parse-condition (take tokens pos)))
          (define right (parse-condition (drop tokens (+ pos 1))))
          `(and ,left ,right))]
    ;; 或
    [(find-token-index tokens "或")
     => (λ (pos)
          (define left (parse-condition (take tokens pos)))
          (define right (parse-condition (drop tokens (+ pos 1))))
          `(or ,left ,right))]
    ;; 在...之间
    [(find-token-index tokens "在")
     => (λ (pos)
          (define var-tokens (take tokens pos))
          (define rest-tokens (drop tokens (+ pos 1)))
          (define between-pos (find-token-index rest-tokens "之间"))
          (define var (parse-expression var-tokens))
          (define range-tokens (take rest-tokens between-pos))
          (define min (parse-expression (take range-tokens 1)))
          (define max (parse-expression (drop range-tokens 1)))
          `(and (>= ,var ,min) (<= ,var ,max)))]
    ;; 大于等于
    [(find-token-index tokens "大于等于")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(>= ,left ,right))]
    ;; 小于等于
    [(find-token-index tokens "小于等于")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(<= ,left ,right))]
    ;; 大于
    [(find-token-index tokens "大于")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(> ,left ,right))]
    ;; 小于
    [(find-token-index tokens "小于")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(< ,left ,right))]
    ;; 等于
    [(find-token-index tokens "等于")
     => (λ (pos)
          (define left (parse-expression (take tokens pos)))
          (define right (parse-expression (drop tokens (+ pos 1))))
          `(= ,left ,right))]
    [else (parse-expression tokens)]))

;; 解析动作
(define (parse-action tokens)
  (cond
    [(null? tokens) #f]
    ;; 输出
    [(string=? (token-value (car tokens)) "输出")
     (define content (parse-expression (cdr tokens)))
     `(displayln ,content)]
    ;; 印
    [(string=? (token-value (car tokens)) "印")
     (define content (parse-expression (cdr tokens)))
     `(displayln ,content)]
    [else (parse-expression tokens)]))

;; 解析因果链
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

;; 主读取函数
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
         (define content (parse-expression (cdr line-tokens)))
         `(displayln ,content)]
        ;; 变量定义
        [(find-token-index line-tokens "定")
         (define name-pos (find-token-index line-tokens "定"))
         (define value-pos (find-token-index line-tokens "是"))
         (define var-name (token-value (list-ref line-tokens (+ name-pos 1))))
         (define var-value-tokens (drop line-tokens (+ value-pos 1)))
         ;; 移除句号
         (define var-value-tokens-clean
           (if (and (not (null? var-value-tokens))
                    (string=? (token-value (last var-value-tokens)) "。"))
               (drop-right var-value-tokens 1)
               var-value-tokens))
         (define var-value (parse-expression var-value-tokens-clean))
         `(define ,(string->symbol var-name) ,var-value)]
        [else #f])))
  
  ;; 过滤掉#f
  (define filtered-code (filter identity racket-code))
  
  ;; 包装成begin块
  (define final-code
    (if (null? filtered-code)
        '(begin)
        (if (= (length filtered-code) 1)
            (car filtered-code)
            `(begin ,@filtered-code))))
  
  ;; 返回语法对象
  (datum->syntax #f final-code))
