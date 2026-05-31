#lang racket

;; 言律语言运行器
;; 读取言律源代码并执行

(require "yanlv_reader.rkt")

;; 读取并执行言律文件
(define (run-yanlv-file filename)
  (displayln "=== 言律语言执行器 ===")
  (displayln (format "文件: ~a" filename))
  (displayln "")
  
  ;; 读取文件
  (define source (file->string filename))
  
  ;; 创建输入端口
  (define in (open-input-string source))
  
  ;; 读取语法
  (define stx (read-syntax filename in))
  
  (displayln "=== 解析结果 ===")
  (displayln (syntax->datum stx))
  (displayln "")
  
  ;; 执行
  (displayln "=== 执行结果 ===")
  (eval (syntax->datum stx)))

;; 测试
(run-yanlv-file "test_yanlv_syntax.yan")
