#lang racket

;; 测试参数分割逻辑

(define test-tokens
  (list (token "孙" 'identifier 0 0)
        (token "，" 'punctuation 0 1)
        (token "李" 'identifier 0 2)))

(struct token (value type line col) #:transparent)

;; 当前的分割逻辑
(define (split-args tokens)
  (let loop ([tokens tokens] [result '()] [current '()])
    (if (null? tokens)
        (if (null? current)
            (reverse result)
            (reverse (cons current result)))
        (let ([t (car tokens)])
          (if (or (string=? (token-value t) "，")
                  (string=? (token-value t) ","))
              (if (null? current)
                  (loop (cdr tokens) result '())
                  (loop (cdr tokens)
                        (cons current result)
                        '()))
              (loop (cdr tokens) result (cons t current)))))))

(displayln "测试参数分割:")
(displayln "输入tokens:")
(for ([t test-tokens])
  (displayln (format "  ~a" (token-value t))))

(displayln "")
(displayln "分割结果:")
(define result (split-args test-tokens))
(for ([arg result]
      [i (in-naturals)])
  (displayln (format "  参数~a: ~a" i (map token-value arg))))
