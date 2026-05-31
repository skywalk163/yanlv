#lang racket

;; ========================================
;; 言律语言交互模式 (REPL)
;; 实时输入执行，即时反馈
;; ========================================

(require "yanlv_reader_surname.rkt")

(define-namespace-anchor anchor)
(define ns (make-base-namespace))

;; 执行单行代码
(define (execute-line line)
  (with-handlers ([exn:fail?
                   (λ (e)
                     (displayln (format "❌ 错误: ~a" (exn-message e)))
                     #f)])
    (define tokens (tokenize-line line 1))
    (if (null? tokens)
        #t
        (let ([in (open-input-string line)])
          (define stx (read-syntax 'repl in))
          (define code (syntax->datum stx))
          (when (and code (not (equal? code '(begin))))
            (eval code ns))
          #t))))

;; 显示欢迎信息
(define (show-welcome)
  (displayln "")
  (displayln "╔════════════════════════════════════════════════╗")
  (displayln "║     言律语言交互模式 v6.0 (REPL)              ║")
  (displayln "╚════════════════════════════════════════════════╝")
  (displayln "")
  (displayln "✨ 特性：")
  (displayln "  • 实时输入执行")
  (displayln "  • 即时反馈结果")
  (displayln "  • 支持Python和Racket两种语法")
  (displayln "  • 使用百家姓作为变量名")
  (displayln "")
  (displayln "📝 示例：")
  (displayln "  言律> 定义变量赵为10")
  (displayln "  言律> 输出赵")
  (displayln "  10")
  (displayln "  言律> 定 钱是20")
  (displayln "  言律> 输出 赵加钱")
  (displayln "  30")
  (displayln "")
  (displayln "💡 命令：")
  (displayln "  :help    - 显示帮助")
  (displayln "  :clear   - 清空环境")
  (displayln "  :quit    - 退出")
  (displayln "")
  (displayln "🎯 开始输入言律代码吧！")
  (displayln ""))

;; 显示帮助
(define (show-help)
  (displayln "")
  (displayln "╔════════════════════════════════════════════════╗")
  (displayln "║              言律语言帮助文档                  ║")
  (displayln "╚════════════════════════════════════════════════╝")
  (displayln "")
  (displayln "📖 语法说明：")
  (displayln "")
  (displayln "1. 变量定义：")
  (displayln "   Python版本：定义变量赵为10")
  (displayln "   Racket版本：定 钱是20")
  (displayln "")
  (displayln "2. 输出：")
  (displayln "   输出 赵")
  (displayln "   输出 \"你好世界\"")
  (displayln "")
  (displayln "3. 运算：")
  (displayln "   输出 赵加钱")
  (displayln "   输出 赵减钱")
  (displayln "")
  (displayln "4. 条件：")
  (displayln "   赵大于10，输出 \"大于10\"。")
  (displayln "")
  (displayln "💡 命令：")
  (displayln "   :help  - 显示帮助")
  (displayln "   :clear - 清空环境")
  (displayln "   :quit  - 退出")
  (displayln ""))

;; 清空环境
(define (clear-env)
  (set! ns (make-base-namespace))
  (displayln "✅ 环境已清空")
  (displayln ""))

;; 主循环
(define (repl-loop)
  (display "言律> ")
  (flush-output)
  
  (define line (read-line))
  
  (cond
    [(eof-object? line) 
     (displayln "")
     (displayln "再见！👋")
     (exit 0)]
    
    [(string=? (string-trim line) "")
     (repl-loop)]
    
    ;; 命令处理
    [(string=? (string-trim line) ":help")
     (show-help)
     (repl-loop)]
    
    [(string=? (string-trim line) ":clear")
     (clear-env)
     (repl-loop)]
    
    [(string=? (string-trim line) ":quit")
     (displayln "")
     (displayln "再见！👋")
     (exit 0)]
    
    ;; 执行代码
    [else
     (execute-line (string-trim line))
     (repl-loop)]))

;; 启动REPL
(define (start-repl)
  (show-welcome)
  (repl-loop))

;; 主函数
(define (main)
  (define args (current-command-line-arguments))
  
  (cond
    [(= (vector-length args) 0)
     (start-repl)]
    
    [(string=? (vector-ref args 0) "--help")
     (displayln "言律语言交互模式")
     (displayln "")
     (displayln "用法: racket yanlv_repl.rkt")
     (displayln "")
     (displayln "启动交互式编程环境")]
    
    [else
     (start-repl)]))

(main)
