#lang racket

;; ========================================
;; 言律语言兼容版运行器
;; 同时支持Python版本和Racket版本语法
;; ========================================

(require "yanlv_reader_compatible.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言兼容版执行器 v5.0        ║")
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
     (displayln "║   言律语言兼容版执行器 v5.0        ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_compatible.rkt <文件名.yan>")
     (displayln "")
     (displayln "特性: 同时支持两种语法！")
     (displayln "")
     (displayln "Python版本语法：")
     (displayln "  定义变量x为10      ✅ 支持")
     (displayln "  输出x              ✅ 支持")
     (displayln "")
     (displayln "Racket版本语法：")
     (displayln "  定 x 是 10         ✅ 支持")
     (displayln "  输出 x             ✅ 支持")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
