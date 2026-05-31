#lang racket

;; ========================================
;; 言律语言导入导出版运行器
;; 支持导入库和导出函数
;; ========================================

(require "yanlv_reader_import.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言导入导出版 v8.0          ║")
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
  
  (displayln "📊 导入库:")
  (displayln "─────────────────────────────────────")
  (if (hash-empty? import-table)
      (displayln "  (无导入)")
      (for ([(path code) import-table])
        (displayln (format "  ✅ ~a" path))))
  (displayln "")
  
  (displayln "📤 导出项:")
  (displayln "─────────────────────────────────────")
  (if (hash-empty? export-table)
      (displayln "  (无导出)")
      (for ([(name def) export-table])
        (define type (car def))
        (if (eq? type 'macro)
            (displayln (format "  宏: ~a" name))
            (displayln (format "  变量: ~a" name)))))
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
     (displayln "║   言律语言导入导出版 v8.0          ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_import.rkt <文件名.yan>")
     (displayln "")
     (displayln "✨ 支持导入导出功能！")
     (displayln "")
     (displayln "导入语法：")
     (displayln "  导入 \"库文件.yan\"")
     (displayln "")
     (displayln "导出语法：")
     (displayln "  导出 宏名(参数) 为 表达式")
     (displayln "  导出 变量名 为 值")
     (displayln "")
     (displayln "示例：")
     (displayln "  # 导入库")
     (displayln "  导入 \"数学库.yan\"")
     (displayln "")
     (displayln "  # 导出函数")
     (displayln "  导出 平方根(赵) 为 赵乘赵")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
