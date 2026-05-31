#lang racket

;; ========================================
;; 言律语言无空格分词运行器
;; ========================================

(require "yanlv_reader_nospace.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言无空格分词执行器 v4.0    ║")
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
     (displayln "║   言律语言无空格分词执行器 v4.0    ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_nospace.rkt <文件名.yan>")
     (displayln "")
     (displayln "特性: 支持无空格的中文文本！")
     (displayln "")
     (displayln "示例:")
     (displayln "  定年龄是25        ✅ 支持")
     (displayln "  定 年龄 是 25     ✅ 也支持")
     (displayln "  温度大于28，输出\"高温\"。  ✅ 支持")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
