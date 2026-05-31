#lang racket

;; ========================================
;; 言律语言百家姓版运行器
;; 使用百家姓识别变量名
;; ========================================

(require "yanlv_reader_surname.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言百家姓版 v6.0            ║")
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
     (displayln "║   言律语言百家姓版 v6.0            ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_surname.rkt <文件名.yan>")
     (displayln "")
     (displayln "✨ 使用百家姓识别变量名！")
     (displayln "")
     (displayln "百家姓变量名示例：")
     (displayln "  赵钱孙李周吴郑王  - 常用姓氏")
     (displayln "  定义变量赵为10    - 赵是变量名")
     (displayln "  输出赵            - 输出变量赵")
     (displayln "")
     (displayln "Python版本语法：")
     (displayln "  定义变量赵为10    ✅ 支持")
     (displayln "  定义变量钱为20    ✅ 支持")
     (displayln "  输出赵加钱        ✅ 支持")
     (displayln "")
     (displayln "Racket版本语法：")
     (displayln "  定 孙 是 30       ✅ 支持")
     (displayln "  定 李 是 40       ✅ 支持")
     (displayln "  输出 孙 加 李     ✅ 支持")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
