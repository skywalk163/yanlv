#lang racket

;; ========================================
;; 言律语言命令行运行器
;; 支持命令行参数指定文件
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
     (displayln "║   言律语言高级语法执行器 v3.0      ║")
     (displayln "╚══════════════════════════════════════╝")
     (displayln "")
     (displayln "用法: racket yanlv.rkt <文件名.yan>")
     (displayln "")
     (displayln "示例:")
     (displayln "  racket yanlv.rkt quick_start.yan")
     (displayln "  racket yanlv.rkt test_advanced.yan")
     (displayln "")
     (displayln "可用文件:")
     (displayln "  - quick_start.yan      快速开始示例")
     (displayln "  - test_advanced.yan    高级语法测试")
     (displayln "  - test_complete.yan    完整测试套件")
     (displayln "")]
    
    ;; 有参数，运行文件
    [else
     (define filename (vector-ref args 0))
     (run-yanlv-file filename)]))

;; 运行
(main)
