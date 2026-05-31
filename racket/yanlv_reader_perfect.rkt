#lang racket

;; ========================================
;; 言律语言完美兼容版读取器
;; 完全支持Python版本和Racket版本语法
;; ========================================

(provide read read-syntax)

;; Token结构
(struct token (value type line col) #:transparent)

;; 关键词列表（按长度降序）
(define keywords-sorted
  '("大于等于" "小于等于" "不等于" "为主题" "定义变量"
    "输出" "定义" "变量" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以"
    "大于" "小于" "等于" "加" "减" "乘" "除"
    "定" "是" "列" "算" "且" "或" "在" "之间"
    "当" "时" "返回" "印" "长度" "为"))

;; 智能分词
(define (smart-tokenize text line-num)
  (define tokens '())
  (define pos 0)
  (define len (string-length text))
  
  (let loop ()
    (when (< pos len)
      (define char (string-ref text pos))
      
      (cond
        ;; 跳过空白
        [(char-whitespace? char)
         (set! pos (+ pos 1))
         (loop)]
        
        ;; 匹配字符串
        [(or (char=? char #\") (char=? char #\'))
         (let* ([quote-char char]
                [start pos])
           (set! pos (+ pos 1))
           (let find-end ()
             (when (and (< pos len)
                        (not (char=? (string-ref text pos) quote-char)))
               (set! pos (+ pos 1))
               (find-end)))
           (set! pos (+ pos 1))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'string line-num start))))
           (loop))]
        
        ;; 匹配数字
        [(or (char-numeric? char)
             (and (char=? char #\-)
                  (< (+ pos 1) len)
                  (char-numeric? (string-ref text (+ pos 1)))))
         (let ([start pos])
           (when (char=? char #\-)
             (set! pos (+ pos 1)))
           (let find-end ()
             (when (and (< pos len)
                        (or (char-numeric? (string-ref text pos))
                            (char=? (string-ref text pos) #\.)))
               (set! pos (+ pos 1))
               (find-end)))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'number line-num start))))
           (loop))]
        
        ;; 匹配中文关键词或标识符
        [(char>=? char #\一)
         (let ([matched-kw #f]
               [matched-len 0])
           ;; 尝试匹配最长关键词
           (for ([keyword keywords-sorted])
             (let ([kw-len (string-length keyword)])
               (when (and (<= (+ pos kw-len) len)
                          (string=? (substring text pos (+ pos kw-len)) keyword)
                          (> kw-len matched-len))
                 (set! matched-kw keyword)
                 (set! matched-len kw-len))))
           
           (if matched-kw
               (begin
                 (set! tokens (append tokens 
                                     (list (token matched-kw 'keyword line-num pos))))
                 (set! pos (+ pos matched-len))
                 (loop))
               ;; 作为标识符
               (let ([start pos])
                 (let find-end ()
                   (when (and (< pos len)
                              (char>=? (string-ref text pos) #\一)
                              (not (is-keyword-start? text pos len)))
                     (set! pos (+ pos 1))
                     (find-end)))
                 (when (= pos start)
                   (set! pos (+ pos 1)))
                 (set! tokens (append tokens 
                                     (list (token (substring text start pos) 
                                                 'identifier line-num start))))
                 (loop))))]
        
        ;; 匹配英文标识符
        [(or (char-alphabetic? char) (char=? char #\_))
         (let ([start pos])
           (let find-end ()
             (when (and (< pos len)
                        (let ([c (string-ref text pos)])
                          (or (char-alphabetic? c)
                              (char-numeric? c)
                              (char=? c #\_))))
               (set! pos (+ pos 1))
               (find-end)))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'identifier line-num start))))
           (loop))]
        
        ;; 匹配标点
        [(or (char=? char #\，) (char=? char #\。)
             (char=? char #\：) (char=? char #\、))
         (set! tokens (append tokens 
                             (list (token (string char) 
                                         'punctuation line-num pos))))
         (set! pos (+ pos 1))
         (loop)]
        
        ;; 其他字符
        [else
         (set! pos (+ pos 1))
         (loop)])))
  
  tokens)

;; 检查是否是关键词的开始
(define (is-keyword-start? text pos len)
  (for/or ([keyword keywords-sorted])
    (let ([kw-len (string-length keyword)])
      (and (<= (+ pos kw-len) len)
           (string=? (substring text pos (+ pos kw-len)) keyword)))))

;; 分词一行
(define (tokenize-line line line-num)
  (define trimmed (string-trim line))
  (cond
    [(or (string=? trimmed "")
         (string-prefix? trimmed "#"))
     '()]
    [else
     (smart-tokenize trimmed line-num)]))

;; 查找token位置
(define (find-token-index tokens value)
  (for/first ([t tokens]
              [i (in-naturals)]
              #:when (string=? (token-value t) value))
    i))

;; 解析表达式（改进版）
(define (parse-expression tokens)
  (cond
    [(null? tokens) 
     0]  ;; 返回0而不是#f
    
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
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(+ ,left ,right))
              (string->symbol (token-value (car tokens)))))]
    
    ;; 减法
    [(find-token-index tokens "减")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(- ,left ,right))
              (string->symbol (token-value (car tokens)))))]
    
    [else
     (string->symbol (token-value (car tokens)))]))

;; 解析条件
(define (parse-condition tokens)
  (cond
    [(null? tokens) #f]
    
    ;; 大于等于
    [(find-token-index tokens "大于等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(>= ,left ,right))
              #f))]
    
    ;; 小于等于
    [(find-token-index tokens "小于等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(<= ,left ,right))
              #f))]
    
    ;; 大于
    [(find-token-index tokens "大于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(> ,left ,right))
              #f))]
    
    ;; 小于
    [(find-token-index tokens "小于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(< ,left ,right))
              #f))]
    
    ;; 等于
    [(find-token-index tokens "等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(= ,left ,right))
              #f))]
    
    [else (parse-expression tokens)]))

;; 解析动作
(define (parse-action tokens)
  (cond
    [(null? tokens) #f]
    [(string=? (token-value (car tokens)) "输出")
     (let ([content (parse-expression (cdr tokens))])
       `(displayln ,content))]
    [else (parse-expression tokens)]))

;; 解析因果链
(define (parse-causal-chain tokens)
  (define comma-pos (find-token-index tokens "，"))
  (define period-pos (find-token-index tokens "。"))
  (if (and comma-pos period-pos (> comma-pos 0))
      (let ([condition-tokens (take tokens comma-pos)]
            [action-tokens (take (drop tokens (+ comma-pos 1)) 
                                (- period-pos comma-pos 1))])
        (let ([condition (parse-condition condition-tokens)]
              [action (parse-action action-tokens)])
          (if (and condition action)
              `(when ,condition ,action)
              #f)))
      #f))

;; 主读取函数
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
  
  ;; 解析语法
  (define racket-code
    (for/list ([line-tokens all-tokens]
               #:when (not (null? line-tokens)))
      (cond
        ;; Python版本：定义变量x为10
        [(find-token-index line-tokens "定义变量")
         (let* ([var-pos (find-token-index line-tokens "定义变量")]
                [value-pos (find-token-index line-tokens "为")])
           (if (and var-pos value-pos 
                    (> (+ var-pos 1) 0)
                    (< (+ var-pos 1) (length line-tokens))
                    (< (+ value-pos 1) (length line-tokens)))
               (let* ([var-name (token-value (list-ref line-tokens (+ var-pos 1)))]
                      [var-value-tokens (drop line-tokens (+ value-pos 1))]
                      [var-value-tokens-clean
                       (if (and (not (null? var-value-tokens))
                                (string=? (token-value (last var-value-tokens)) "。"))
                           (drop-right var-value-tokens 1)
                           var-value-tokens)]
                      [var-value (parse-expression var-value-tokens-clean)])
                 `(define ,(string->symbol var-name) ,var-value))
               #f))]
        
        ;; Racket版本：定x是10
        [(find-token-index line-tokens "定")
         (let* ([name-pos (find-token-index line-tokens "定")]
                [value-pos (find-token-index line-tokens "是")])
           (if (and name-pos value-pos
                    (> (+ name-pos 1) 0)
                    (< (+ name-pos 1) (length line-tokens))
                    (< (+ value-pos 1) (length line-tokens)))
               (let* ([var-name (token-value (list-ref line-tokens (+ name-pos 1)))]
                      [var-value-tokens (drop line-tokens (+ value-pos 1))]
                      [var-value-tokens-clean
                       (if (and (not (null? var-value-tokens))
                                (string=? (token-value (last var-value-tokens)) "。"))
                           (drop-right var-value-tokens 1)
                           var-value-tokens)]
                      [var-value (parse-expression var-value-tokens-clean)])
                 `(define ,(string->symbol var-name) ,var-value))
               #f))]
        
        ;; 因果链
        [(and (find-token-index line-tokens "，")
              (find-token-index line-tokens "。"))
         (parse-causal-chain line-tokens)]
        
        ;; 输出语句
        [(and (not (null? line-tokens))
              (string=? (token-value (car line-tokens)) "输出"))
         (let ([content (parse-expression (cdr line-tokens))])
           `(displayln ,content))]
        
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
  
  (datum->syntax #f final-code))
