#lang racket

;; ========================================
;; 言律语言智能分词运行器
;; 支持无空格的中文文本
;; ========================================

(require "yanlv_reader_smart.rkt")

;; 定义执行环境
(define-namespace-anchor anchor)
(define ns (make-base-namespace))

;; 读取并执行言律文件
(define (run-yanlv-file filename)
  (displayln "╔══════════════════════════════════════╗")
  (displayln "║   言律语言智能分词执行器 v3.1      ║")
  (displayln "╚══════════════════════════════════════╝")
  (displayln "")
  (displayln (format "📄 文件: ~a" filename))
  (displayln "")
  
  ;; 检查文件是否存在
  (unless (file-exists? filename)
    (displayln "❌ 错误: 文件不存在")
    (exit 1))
  
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

;; 主函数
(define (main)
  (define args (current-command-line-arguments))
  
  (cond
    ;; 没有参数，显示帮助
    [(= (vector-length args) 0)
     (displayln "╔══════════════════════════════════════╗")
     (displayln "║   言律语言智能分词执行器 v3.1      ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv_smart.rkt <文件名.yan>")
     (displayln "")
     (displayln "特性: 支持无空格的中文文本")
     (displayln "")
     (displayln "示例:")
     (displayln "  racket yanlv_smart.rkt test_no_space.yan")
     (displayln "")
     (displayln "对比:")
     (displayln "  ✅ 定年龄是25")
     (displayln "  ✅ 定 年龄 是 25")
     (displayln "  两种写法都支持！")
     (displayln "")]
    
    ;; 有参数，运行文件
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

;; 运行
(main)
