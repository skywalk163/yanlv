#lang racket

;; ========================================
;; 言律语言高级语法运行器
;; ========================================

(require "yanlv_reader_advanced.rkt")

;; 定义执行环境
(define-namespace-anchor anchor)
(define ns (make-base-namespace))

;; 读取并执行言律文件
(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言高级语法执行器 v3.0      ║")
  (displayln "╚══════════════════════════════════════╝")
  (displayln "")
  (displayln (format "📄 文件: ~a" filename))
  (displayln "")
  
  ;; 读取文件
  (define source (file->string filename))
  
  ;; 创建输入端口
  (define in (open-input-string source))
  
  ;; 读取语法
  (define stx (read-syntax filename in))
  
  (displayln "🔍 解析结果:")
  (displayln "─────────────────────────────────────")
  (pretty-print (syntax->datum stx))
  (displayln "")
  
  ;; 执行
  (displayln "⚡ 执行结果:")
  (displayln "─────────────────────────────────────")
  (with-handlers ([exn:fail?
                   (λ (e)
                     (displayln "❌ 执行错误:")
                     (displayln (exn-message e)))])
    (eval (syntax->datum stx) ns))
  
  (displayln "")
  (displayln "✅ 执行完成"))

;; 运行测试
(run-yanlv-file "test_advanced.yan")
