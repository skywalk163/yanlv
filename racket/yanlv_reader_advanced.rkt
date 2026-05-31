#lang racket

;; ========================================
;; 言律语言高级语法读取器
;; 支持循环、语境省略、数组操作
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
    "当" "时" "返回" "印" "长度"))

;; 分词一行
(define (tokenize-line line line-num)
  (define trimmed (string-trim line))
  (cond
    [(or (string=? trimmed "")
         (string-prefix? trimmed "#"))
     '()]
    [else
     (define parts (string-split trimmed))
     (for/list ([part parts]
                [i (in-naturals)])
       (cond
         [(and (string-prefix? part "\"")
               (string-suffix? part "\""))
          (token part 'string line-num i)]
         [(regexp-match? #rx"^-?[0-9]+\\.?[0-9]*$" part)
          (token part 'number line-num i)]
         [(member part keywords)
          (token part 'keyword line-num i)]
         [(or (string=? part "，") (string=? part "。")
              (string=? part "：") (string=? part "、"))
          (token part 'punctuation line-num i)]
         [else
          (token part 'identifier line-num i)]))]))

;; 查找token位置
(define (find-token-index tokens value)
  (for/first ([t tokens]
              [i (in-naturals)]
              #:when (string=? (token-value t) value))
    i))

;; ========================================
;; 表达式解析
;; ========================================

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
    ;; 长度
    [(find-token-index tokens "长度")
     => (λ (pos)
          (define var-tokens (drop tokens (+ pos 1)))
          (define var (parse-expression var-tokens))
          `(length ,var))]
    ;; 函数式数组访问：列表算j
    [(find-token-index tokens "算")
     => (λ (pos)
          (define arr-tokens (take tokens pos))
          (define idx-tokens (drop tokens (+ pos 1)))
          (define arr (parse-expression arr-tokens))
          (define idx (parse-expression idx-tokens))
          `(list-ref ,arr ,idx))]
    [else
     (string->symbol (token-value (car tokens)))]))

;; ========================================
;; 条件解析
;; ========================================

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

;; ========================================
;; 动作解析
;; ========================================

(define (parse-action tokens)
  (cond
    [(null? tokens) #f]
    [(string=? (token-value (car tokens)) "输出")
     (define content (parse-expression (cdr tokens)))
     `(displayln ,content)]
    [(string=? (token-value (car tokens)) "印")
     (define content (parse-expression (cdr tokens)))
     `(displayln ,content)]
    [else (parse-expression tokens)]))

;; ========================================
;; 因果链解析
;; ========================================

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

;; ========================================
;; 主读取函数
;; ========================================

(define (read in)
  (syntax->datum (read-syntax #f in)))

(define (read-syntax src in)
  (define source (port->string in))
  (define lines (string-split source "\n"))
  
  ;; 分词所有行
  (define all-tokens
    (for/list ([line lines]
               [line-num (in-naturals 1)])
      (tokenize-line line line-num)))
  
  ;; 解析语法（支持多行结构）
  (define-values (racket-code _)
    (parse-lines all-tokens '() 0))
  
  ;; 过滤掉#f
  (define filtered-code (filter identity racket-code))
  
  ;; 包装成begin块
  (define final-code
    (if (null? filtered-code)
        '(begin)
        (if (= (length filtered-code) 1)
            (car filtered-code)
            `(begin ,@filtered-code))))
  
  (datum->syntax #f final-code))

;; ========================================
;; 多行语法解析
;; ========================================

(define (parse-lines all-tokens result indent)
  (cond
    [(null? all-tokens) (values (reverse result) indent)]
    [else
     (define line-tokens (car all-tokens))
     (define rest-lines (cdr all-tokens))
     
     (cond
       ;; 空行
       [(null? line-tokens)
        (parse-lines rest-lines result indent)]
       
       ;; 循环语法：对于i从1到10：
       [(find-token-index line-tokens "对于")
        (define-values (loop-code new-indent)
          (parse-for-loop line-tokens rest-lines))
        (parse-lines (drop rest-lines (- (length rest-lines) 
                                         (length (cdr rest-lines))))
                     (cons loop-code result)
                     new-indent)]
       
       ;; 语境省略：以X为主题：
       [(find-token-index line-tokens "以")
        (define-values (context-code new-indent)
          (parse-context-omission line-tokens rest-lines))
        (parse-lines (drop rest-lines (- (length rest-lines) 
                                         (length (cdr rest-lines))))
                     (cons context-code result)
                     new-indent)]
       
       ;; 因果链
       [(and (find-token-index line-tokens "，")
             (find-token-index line-tokens "。"))
        (define chain-code (parse-causal-chain line-tokens))
        (parse-lines rest-lines (cons chain-code result) indent)]
       
       ;; 输出语句
       [(and (not (null? line-tokens))
             (string=? (token-value (car line-tokens)) "输出"))
        (define content (parse-expression (cdr line-tokens)))
        (parse-lines rest-lines 
                     (cons `(displayln ,content) result) 
                     indent)]
       
       ;; 变量定义
       [(find-token-index line-tokens "定")
        (define name-pos (find-token-index line-tokens "定"))
        (define value-pos (find-token-index line-tokens "是"))
        (define var-name (token-value (list-ref line-tokens (+ name-pos 1))))
        (define var-value-tokens (drop line-tokens (+ value-pos 1)))
        (define var-value-tokens-clean
          (if (and (not (null? var-value-tokens))
                   (string=? (token-value (last var-value-tokens)) "。"))
              (drop-right var-value-tokens 1)
              var-value-tokens))
        (define var-value (parse-expression var-value-tokens-clean))
        (parse-lines rest-lines 
                     (cons `(define ,(string->symbol var-name) ,var-value) result)
                     indent)]
       
       [else
        (parse-lines rest-lines result indent)])]))

;; ========================================
;; 循环语法解析
;; ========================================

(define (parse-for-loop line-tokens rest-lines)
  ;; 对于 i 从 1 到 10 ：
  (define for-pos (find-token-index line-tokens "对于"))
  (define from-pos (find-token-index line-tokens "从"))
  (define to-pos (find-token-index line-tokens "到"))
  
  (define var-name (token-value (list-ref line-tokens (+ for-pos 1))))
  (define start-value (parse-expression 
                       (list (list-ref line-tokens (+ from-pos 1)))))
  (define end-value (parse-expression 
                     (list (list-ref line-tokens (+ to-pos 1)))))
  
  ;; 收集循环体（缩进的行）
  (define body-lines
    (for/list ([line rest-lines]
               #:when (and (not (null? line))
                          (> (get-indent line) 0)))
      line))
  
  ;; 解析循环体
  (define body-code
    (for/list ([line body-lines]
               #:when (not (null? line)))
      (cond
        ;; 输出
        [(string=? (token-value (car line)) "输出")
         `(displayln ,(parse-expression (cdr line)))]
        ;; 变量定义
        [(find-token-index line "定")
         (define name-pos (find-token-index line "定"))
         (define value-pos (find-token-index line "是"))
         (define var (token-value (list-ref line (+ name-pos 1))))
         (define val-tokens (drop line (+ value-pos 1)))
         (define val-tokens-clean
           (if (and (not (null? val-tokens))
                    (string=? (token-value (last val-tokens)) "。"))
               (drop-right val-tokens 1)
               val-tokens))
         (define val (parse-expression val-tokens-clean))
         `(set! ,(string->symbol var) ,val)]
        [else #f])))
  
  (define filtered-body (filter identity body-code))
  
  (values
   `(for ([,(string->symbol var-name) 
           (in-range ,start-value (+ ,end-value 1))])
      ,@filtered-body)
   1))

;; ========================================
;; 语境省略解析
;; ========================================

(define (parse-context-omission line-tokens rest-lines)
  ;; 以 订单 为 主题 ：
  (define theme-pos (find-token-index line-tokens "为主题"))
  (define theme-name (token-value (list-ref line-tokens (- theme-pos 1))))
  
  ;; 收集主题体
  (define body-lines
    (for/list ([line rest-lines]
               #:when (and (not (null? line))
                          (> (get-indent line) 0)))
      line))
  
  ;; 解析主题体
  (define body-code
    (for/list ([line body-lines]
               #:when (not (null? line)))
      (cond
        ;; 输出
        [(string=? (token-value (car line)) "输出")
         `(displayln ,(parse-expression (cdr line)))]
        ;; 印
        [(string=? (token-value (car line)) "印")
         `(displayln ,(parse-expression (cdr line)))]
        [else #f])))
  
  (define filtered-body (filter identity body-code))
  
  (values
   `(let ([当前主题 ,(string->symbol theme-name)])
      ,@filtered-body)
   1))

;; ========================================
;; 辅助函数
;; ========================================

(define (get-indent tokens)
  ;; 简单的缩进检测
  (if (null? tokens) 0 1))
