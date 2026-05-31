#lang racket

;; ========================================
;; 言律语言完美兼容版运行器
;; 完全支持Python版本和Racket版本语法
;; ========================================

(require "yanlv_reader_perfect.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言完美兼容版 v5.1          ║")
  (displayln "╚══════════════════════════════════════╝")
  (displayln "")
  (displayln (format "📄 文件: ~a" filename))
  (displayln "")
  
  (unless (file-exists? filename)
    (displayln "❌ 错误: 文件不存在")
    (exit 1))
  
  (define source (file->string filename))
  (define in (open-input-string source))
  (define stx (read-syntax filename in))
  
  (displayln "🔍 解析结果:")
  (displayln "─────────────────────────────────────")
  (pretty-print (syntax->datum stx))
  (displayln "")
  
  (displayln "⚡ 执行结果:")
  (displayln "─────────────────────────────────────")
  (with-handlers ([exn:fail?
                   (λ (e)
                     (displayln "❌ 执行错误:")
                     (displayln (exn-message e)))])
    (eval (syntax->datum stx) ns))
  
  (displayln "")
  (displayln "✅ 执行完成"))

(define (main)
  (define args (current-command-line-arguments))
  
  (cond
    [(= (vector-length args) 0)
     (displayln "╔══════════════════════════════════════╗")
     (displayln "║   言律语言完美兼容版 v5.1          ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_perfect.rkt <文件名.yan>")
     (displayln "")
     (displayln "✨ 完美支持两种语法！")
     (displayln "")
     (displayln "Python版本语法：")
     (displayln "  定义变量x为10      ✅ 完全支持")
     (displayln "  输出x              ✅ 完全支持")
     (displayln "  定义变量z为x加y    ✅ 完全支持")
     (displayln "")
     (displayln "Racket版本语法：")
     (displayln "  定 x 是 10         ✅ 完全支持")
     (displayln "  输出 x             ✅ 完全支持")
     (displayln "  定 z 是 x 加 y     ✅ 完全支持")
     (displayln "")
     (displayln "混合使用：")
     (displayln "  定义变量a为10")
     (displayln "  定 b 是 20")
     (displayln "  输出 a 加 b        ✅ 完全支持")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
