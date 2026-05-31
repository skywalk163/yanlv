#lang racket

;; ========================================
;; 言律语言增强版运行器
;; 改进错误提示和稳定性
;; ========================================

(require "yanlv_reader_nospace.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

;; 错误处理：提供友好的错误信息
(define (handle-error e filename line-num)
  (define msg (exn-message e))
  
  (displayln "")
  (displayln "❌ 执行错误")
  (displayln "─────────────────────────────────────")
  
  (cond
    ;; 未定义变量
    [(regexp-match #rx"undefined.*before its definition" msg)
     (define var-match (regexp-match #rx"([^:]+):" msg))
     (if var-match
         (begin
           (displayln (format "📍 错误类型：变量未定义"))
           (displayln (format "💡 变量名：~a" (cadr var-match)))
           (displayln (format "💡 建议：请先定义变量，例如：定 ~a 是 值" (cadr var-match))))
         (displayln "📍 错误类型：变量未定义"))]
    
    ;; 类型错误
    [(regexp-match #rx"contract violation" msg)
     (displayln "📍 错误类型：类型不匹配")
     (displayln "💡 建议：检查数据类型是否正确")]
    
    ;; 语法错误
    [(regexp-match #rx"read:.*unexpected" msg)
     (displayln "📍 错误类型：语法错误")
     (displayln "💡 建议：检查语法格式是否正确")]
    
    ;; 其他错误
    [else
     (displayln (format "📍 错误信息：~a" msg))])
  
  (displayln "")
  (displayln (format "📄 文件：~a" filename))
  (when line-num
    (displayln (format "📍 位置：第 ~a 行" line-num))))

;; 读取并执行言律文件
(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言增强版执行器 v4.1        ║")
  (displayln "╚══════════════════════════════════════╝")
  (displayln "")
  (displayln (format "📄 文件: ~a" filename))
  (displayln "")
  
  ;; 检查文件是否存在
  (unless (file-exists? filename)
    (displayln "❌ 错误: 文件不存在")
    (displayln (format "💡 请检查文件路径：~a" filename))
    (exit 1))
  
  ;; 读取文件
  (define source (file->string filename))
  (define in (open-input-string source))
  
  ;; 读取语法
  (define stx 
    (with-handlers ([exn:fail:read?
                     (λ (e)
                       (displayln "❌ 语法错误")
                       (displayln "─────────────────────────────────────")
                       (displayln (exn-message e))
                       (displayln "")
                       (displayln "💡 建议：检查语法格式")
                       (exit 1))])
      (read-syntax filename in)))
  
  (displayln "🔍 解析结果:")
  (displayln "─────────────────────────────────────")
  (pretty-print (syntax->datum stx))
  (displayln "")
  
  ;; 执行
  (displayln "⚡ 执行结果:")
  (displayln "─────────────────────────────────────")
  (with-handlers ([exn:fail?
                   (λ (e) (handle-error e filename #f))])
    (eval (syntax->datum stx) ns))
  
  (displayln "")
  (displayln "✅ 执行完成"))

;; 主函数
(define (main)
  (define args (current-command-line-arguments))
  
  (cond
    [(= (vector-length args) 0)
     (displayln "╔══════════════════════════════════════╗")
     (displayln "║   言律语言增强版执行器 v4.1        ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_enhanced.rkt <文件名.yan>")
     (displayln "")
     (displayln "特性:")
     (displayln "  ✅ 支持无空格的中文文本")
     (displayln "  ✅ 友好的错误提示")
     (displayln "  ✅ 详细的执行信息")
     (displayln "")
     (displayln "示例:")
     (displayln "  racket yanlv_enhanced.rkt hello.yan")
     (displayln "")]
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

(main)
