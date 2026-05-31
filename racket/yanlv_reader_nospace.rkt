#lang racket

;; ========================================
;; 言律语言无空格分词读取器
;; 支持无空格的中文文本
;; ========================================

(provide read read-syntax)

;; Token结构
(struct token (value type line col) #:transparent)

;; 关键词列表（按长度降序排列，优先匹配长关键词）
(define keywords-sorted
  '("大于等于" "小于等于" "不等于" "为主题"
    "输出" "定义" "变量" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以"
    "大于" "小于" "等于" "加" "减" "乘" "除"
    "定" "是" "列" "算" "且" "或" "在" "之间"
    "当" "时" "返回" "印" "长度"))

;; 智能分词：支持无空格的中文文本
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
         (define quote-char char)
         (define start pos)
         (set! pos (+ pos 1))
         (while (and (< pos len)
                     (not (char=? (string-ref text pos) quote-char)))
           (set! pos (+ pos 1)))
         (set! pos (+ pos 1))
         (set! tokens (append tokens 
                             (list (token (substring text start pos) 
                                         'string line-num start))))
         (loop)]
        
        ;; 匹配数字
        [(or (char-numeric? char)
             (and (char=? char #\-)
                  (< (+ pos 1) len)
                  (char-numeric? (string-ref text (+ pos 1)))))
         (define start pos)
         (when (char=? char #\-)
           (set! pos (+ pos 1)))
         (while (and (< pos len)
                     (or (char-numeric? (string-ref text pos))
                         (char=? (string-ref text pos) #\.)))
           (set! pos (+ pos 1)))
         (set! tokens (append tokens 
                             (list (token (substring text start pos) 
                                         'number line-num start))))
         (loop)]
        
        ;; 匹配中文关键词或标识符
        [(char>=? char #\一)
         ;; 尝试匹配最长关键词
         (define matched-kw #f)
         (define matched-len 0)
         
         (for ([keyword keywords-sorted])
           (define kw-len (string-length keyword))
           (when (and (<= (+ pos kw-len) len)
                      (string=? (substring text pos (+ pos kw-len)) keyword)
                      (> kw-len matched-len))
             (set! matched-kw keyword)
             (set! matched-len kw-len)))
         
         (if matched-kw
             ;; 匹配到关键词
             (begin
               (set! tokens (append tokens 
                                   (list (token matched-kw 'keyword line-num pos))))
               (set! pos (+ pos matched-len))
               (loop))
             ;; 没匹配到关键词，作为标识符
             (let ([start pos])
               (while (and (< pos len)
                           (char>=? (string-ref text pos) #\一)
                           ;; 确保不是关键词的开始
                           (not (is-keyword-start? text pos len)))
                 (set! pos (+ pos 1)))
               ;; 至少前进一个字符
               (when (= pos start)
                 (set! pos (+ pos 1)))
               (set! tokens (append tokens 
                                   (list (token (substring text start pos) 
                                               'identifier line-num start))))
               (loop)))]
        
        ;; 匹配英文标识符
        [(or (char-alphabetic? char) (char=? char #\_))
         (define start pos)
         (while (and (< pos len)
                     (let ([c (string-ref text pos)])
                       (or (char-alphabetic? c)
                           (char-numeric? c)
                           (char=? c #\_))))
           (set! pos (+ pos 1)))
         (set! tokens (append tokens 
                             (list (token (substring text start pos) 
                                         'identifier line-num start))))
         (loop)]
        
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
    (define kw-len (string-length keyword))
    (and (<= (+ pos kw-len) len)
         (string=? (substring text pos (+ pos kw-len)) keyword))))

;; while 宏
(define-syntax while
  (syntax-rules ()
    [(_ condition body ...)
     (let loop ()
       (when condition
         body ...
         (loop)))]))

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
    [else
     (string->symbol (token-value (car tokens)))]))

;; 解析条件
(define (parse-condition tokens)
  (cond
    [(null? tokens) #f]
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
    [(string=? (token-value (car tokens)) "输出")
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
         (and name-pos value-pos)
         (define var-name (token-value (list-ref line-tokens (+ name-pos 1))))
         (define var-value-tokens (drop line-tokens (+ value-pos 1)))
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
  
  (datum->syntax #f final-code))
