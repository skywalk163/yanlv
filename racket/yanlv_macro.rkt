#lang racket

;; ========================================
;; 言律语言宏系统版运行器
;; 支持宏定义和宏展开
;; ========================================

(require "yanlv_reader_macro.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言宏系统版 v7.0            ║")
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
  
  (displayln "📊 宏定义:")
  (displayln "─────────────────────────────────────")
  (if (hash-empty? macro-table)
      (displayln "  (无宏定义)")
      (for ([(name def) macro-table])
        (displayln (format "  ~a: 参数=~a" name (car def)))))
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
     (displayln "║   言律语言宏系统版 v7.0            ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_macro.rkt <文件名.yan>")
     (displayln "")
     (displayln "✨ 支持宏系统！")
     (displayln "")
     (displayln "宏定义语法：")
     (displayln "  定义宏 宏名(参数) 为 表达式")
     (displayln "")
     (displayln "示例：")
     (displayln "  定义宏 双倍(赵) 为 赵加赵")
     (displayln "  定义变量钱为10")
     (displayln "  输出 双倍(钱)    # 输出 20")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
