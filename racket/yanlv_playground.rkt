#lang racket

;; ========================================
;; 言律语言 Playground (简化版)
;; 在浏览器中运行言律代码
;; ========================================

(require "yanlv_reader_surname.rkt"
         net/url
         web-server/http
         web-server/servlet
         web-server/servlet-env
         xml)

(define-namespace-anchor anchor)

;; 执行言律代码
(define (execute-yanlv code)
  (with-handlers ([exn:fail?
                   (λ (e)
                     (format "错误: ~a" (exn-message e)))])
    (define ns (make-base-namespace))
    (define in (open-input-string code))
    (define stx (read-syntax 'playground in))
    (define racket-code (syntax->datum stx))
    
    ;; 捕获输出
    (define output-port (open-output-string))
    (parameterize ([current-output-port output-port])
      (when (and racket-code (not (equal? racket-code '(begin))))
        (eval racket-code ns)))
    
    (get-output-string output-port)))

;; HTML模板
(define (render-page [result ""] [code ""])
  (string-append
   "<!DOCTYPE html>"
   "<html lang='zh-CN'>"
   "<head>"
   "  <meta charset='UTF-8'>"
   "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
   "  <title>言律语言 Playground</title>"
   "  <style>"
   "    * { margin: 0; padding: 0; box-sizing: border-box; }"
   "    body { "
   "      font-family: 'Microsoft YaHei', 'SimHei', sans-serif; "
   "      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
   "      min-height: 100vh; "
   "      padding: 20px; "
   "    }"
   "    .container { "
   "      max-width: 1200px; "
   "      margin: 0 auto; "
   "      background: white; "
   "      border-radius: 20px; "
   "      box-shadow: 0 20px 60px rgba(0,0,0,0.3); "
   "      overflow: hidden; "
   "    }"
   "    .header { "
   "      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
   "      color: white; "
   "      padding: 30px; "
   "      text-align: center; "
   "    }"
   "    .header h1 { font-size: 2.5em; margin-bottom: 10px; }"
   "    .header p { font-size: 1.2em; opacity: 0.9; }"
   "    .main { padding: 30px; }"
   "    .editor { "
   "      display: grid; "
   "      grid-template-columns: 1fr 1fr; "
   "      gap: 20px; "
   "      margin-bottom: 20px; "
   "    }"
   "    .panel { "
   "      border: 2px solid #e0e0e0; "
   "      border-radius: 10px; "
   "      overflow: hidden; "
   "    }"
   "    .panel-header { "
   "      background: #f5f5f5; "
   "      padding: 15px; "
   "      font-weight: bold; "
   "      border-bottom: 2px solid #e0e0e0; "
   "    }"
   "    .panel-content { padding: 15px; }"
   "    textarea { "
   "      width: 100%; "
   "      height: 300px; "
   "      border: none; "
   "      font-family: 'Consolas', 'Monaco', monospace; "
   "      font-size: 16px; "
   "      resize: vertical; "
   "      outline: none; "
   "    }"
   "    .output { "
   "      width: 100%; "
   "      height: 300px; "
   "      background: #f8f8f8; "
   "      font-family: 'Consolas', 'Monaco', monospace; "
   "      font-size: 16px; "
   "      white-space: pre-wrap; "
   "      overflow-y: auto; "
   "      padding: 15px; "
   "    }"
   "    .buttons { text-align: center; margin: 20px 0; }"
   "    button { "
   "      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
   "      color: white; "
   "      border: none; "
   "      padding: 15px 40px; "
   "      font-size: 18px; "
   "      border-radius: 50px; "
   "      cursor: pointer; "
   "      margin: 0 10px; "
   "      transition: transform 0.3s, box-shadow 0.3s; "
   "    }"
   "    button:hover { "
   "      transform: translateY(-3px); "
   "      box-shadow: 0 10px 20px rgba(0,0,0,0.2); "
   "    }"
   "    .examples { "
   "      background: #f9f9f9; "
   "      padding: 20px; "
   "      border-radius: 10px; "
   "      margin-top: 20px; "
   "    }"
   "    .examples h3 { margin-bottom: 15px; color: #667eea; }"
   "    .example-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }"
   "    .example { "
   "      background: white; "
   "      padding: 15px; "
   "      border-radius: 8px; "
   "      cursor: pointer; "
   "      transition: all 0.3s; "
   "      border: 2px solid transparent; "
   "    }"
   "    .example:hover { "
   "      border-color: #667eea; "
   "      transform: translateY(-2px); "
   "    }"
   "    .example h4 { color: #667eea; margin-bottom: 8px; }"
   "    .example pre { "
   "      font-size: 12px; "
   "      color: #666; "
   "      white-space: pre-wrap; "
   "    }"
   "  </style>"
   "</head>"
   "<body>"
   "  <div class='container'>"
   "    <div class='header'>"
   "      <h1>🎯 言律语言 Playground</h1>"
   "      <p>在浏览器中体验中文编程的魅力</p>"
   "    </div>"
   "    <div class='main'>"
   "      <form method='post' action='/run'>"
   "        <div class='editor'>"
   "          <div class='panel'>"
   "            <div class='panel-header'>📝 代码编辑器</div>"
   "            <div class='panel-content'>"
   "              <textarea name='code' placeholder='在这里输入言律代码...'>" code "</textarea>"
   "            </div>"
   "          </div>"
   "          <div class='panel'>"
   "            <div class='panel-header'>⚡ 执行结果</div>"
   "            <div class='panel-content'>"
   "              <div class='output'>" result "</div>"
   "            </div>"
   "          </div>"
   "        </div>"
   "        <div class='buttons'>"
   "          <button type='submit'>🚀 运行代码</button>"
   "          <button type='button' onclick='clearCode()'>🗑️ 清空</button>"
   "        </div>"
   "      </form>"
   "      <div class='examples'>"
   "        <h3>📚 示例代码</h3>"
   "        <div class='example-grid'>"
   "          <div class='example' onclick='loadExample(1)'>"
   "            <h4>Hello World</h4>"
   "            <pre>输出 \"你好世界\"</pre>"
   "          </div>"
   "          <div class='example' onclick='loadExample(2)'>"
   "            <h4>变量计算</h4>"
   "            <pre>定义变量赵为10\\n定义变量钱为20\\n输出 赵加钱</pre>"
   "          </div>"
   "          <div class='example' onclick='loadExample(3)'>"
   "            <h4>条件判断</h4>"
   "            <pre>定义变量赵为90\\n赵 大于 80，输出 \"优秀\"。</pre>"
   "          </div>"
   "        </div>"
   "      </div>"
   "    </div>"
   "  </div>"
   "  <script>"
   "    function clearCode() {"
   "      document.querySelector('textarea[name=code]').value = '';"
   "    }"
   "    function loadExample(num) {"
   "      const examples = {"
   "        1: '输出 \"你好世界\"',"
   "        2: '定义变量赵为10\\n定义变量钱为20\\n输出 赵加钱',"
   "        3: '定义变量赵为90\\n赵 大于 80，输出 \"优秀\"。'"
   "      };"
   "      document.querySelector('textarea[name=code]').value = examples[num];"
   "    }"
   "  </script>"
   "</body>"
   "</html>"))

;; Servlet处理函数
(define (start req)
  (response/xexpr
   (string->xexpr (render-page))))

(define (run-handler req)
  (define bindings (request-bindings req))
  (define code (extract-binding/single 'code bindings))
  (define result (execute-yanlv code))
  (response/xexpr
   (string->xexpr (render-page result code))))

;; 定义URL路由
(define-values (dispatch generate-url)
  (dispatch-rules
   [("") start]
   [("run") run-handler]))

;; 启动服务器
(define (start-playground [port 8080])
  (displayln "╔════════════════════════════════════════════════╗")
  (displayln "║     言律语言 Playground v6.0                  ║")
  (displayln "╚════════════════════════════════════════════════╝")
  (displayln "")
  (displayln "🌐 服务器启动中...")
  (displayln (format "📍 访问地址: http://localhost:~a" port))
  (displayln "")
  (displayln "✨ 特性：")
  (displayln "  • 在浏览器中运行言律代码")
  (displayln "  • 实时执行和反馈")
  (displayln "  • 精美的界面设计")
  (displayln "  • 内置示例代码")
  (displayln "")
  (displayln "💡 按 Ctrl+C 停止服务器")
  (displayln "")
  
  (serve/servlet dispatch
                 #:port port
                 #:servlet-path "/"
                 #:launch-browser? #f
                 #:quit? #f
                 #:listen-ip #f))

;; 主函数
(define (main)
  (define args (current-command-line-arguments))
  
  (cond
    [(= (vector-length args) 0)
     (start-playground 8080)]
    
    [(string=? (vector-ref args 0) "--help")
     (displayln "言律语言 Playground")
     (displayln "")
     (displayln "用法: racket yanlv_playground.rkt [端口]")
     (displayln "")
     (displayln "示例:")
     (displayln "  racket yanlv_playground.rkt        # 默认端口8080")
     (displayln "  racket yanlv_playground.rkt 3000   # 使用端口3000")]
    
    [else
     (define port (string->number (vector-ref args 0)))
     (if port
         (start-playground port)
         (start-playground 8080))]))

(main)
