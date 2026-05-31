#lang racket

;; ========================================
;; 言律语言导入导出版读取器
;; 支持导入库、导出函数和变量
;; ========================================

(provide read read-syntax tokenize-line macro-table export-table import-table)

;; Token结构
(struct token (value type line col) #:transparent)

;; 宏表：存储定义的宏
(define macro-table (make-hash))

;; 导出表：存储导出的函数和变量
(define export-table (make-hash))

;; 导入表：存储导入的库
(define import-table (make-hash))

;; 百家姓
(define surnames
  '("赵" "钱" "孙" "李" "周" "吴" "郑" "王" "冯" "陈"
    "褚" "卫" "蒋" "沈" "韩" "杨" "朱" "秦" "尤" "许"
    "何" "吕" "施" "张" "孔" "曹" "严" "华" "金" "魏"
    "陶" "姜" "戚" "谢" "邹" "喻" "柏" "水" "窦" "章"
    "云" "苏" "潘" "葛" "奚" "范" "彭" "郎" "鲁" "韦"
    "昌" "马" "苗" "凤" "花" "方" "俞" "任" "袁" "柳"
    "酆" "鲍" "史" "唐" "费" "廉" "岑" "薛" "雷" "贺"
    "倪" "汤" "滕" "殷" "罗" "毕" "郝" "邬" "安" "常"
    "乐" "于" "时" "傅" "皮" "卞" "齐" "康" "伍" "余"
    "元" "卜" "顾" "孟" "平" "黄" "和" "穆" "萧" "尹"
    "姚" "邵" "湛" "汪" "祁" "毛" "禹" "狄" "米" "贝"
    "明" "臧" "计" "伏" "成" "戴" "谈" "宋" "茅" "庞"
    "熊" "纪" "舒" "屈" "项" "祝" "梁" "杜" "阮" "蓝"
    "闵" "席" "季" "麻" "强" "贾" "路" "娄" "危" "江"
    "童" "颜" "郭" "梅" "盛" "林" "刁" "钟" "徐" "邱"
    "骆" "高" "夏" "蔡" "田" "樊" "胡" "凌" "霍" "虞"
    "万" "支" "柯" "昝" "管" "卢" "莫" "经" "房" "裘"
    "缪" "干" "解" "应" "宗" "丁" "宣" "邓" "郁" "单"
    "杭" "洪" "包" "诸" "左" "石" "崔" "吉" "龚" "程"
    "嵇" "邢" "滑" "裴" "陆" "荣" "翁" "荀" "羊" "甄"
    "家" "封" "芮" "羿" "储" "靳" "汲" "邴" "糜" "松"
    "井" "段" "富" "巫" "乌" "焦" "巴" "弓" "牧" "隗"
    "山" "谷" "车" "侯" "宓" "蓬" "全" "郗" "班" "仰"
    "秋" "仲" "伊" "宫" "宁" "仇" "栾" "暴" "甘" "钭"
    "厉" "戎" "祖" "武" "符" "刘" "景" "詹" "束" "龙"
    "叶" "幸" "司" "韶" "郜" "黎" "蓟" "薄" "印" "宿"
    "白" "怀" "蒲" "台" "从" "鄂" "索" "咸" "籍" "赖"
    "卓" "蔺" "屠" "蒙" "池" "乔" "阴" "郁" "胥" "能"
    "苍" "双" "闻" "莘" "党" "翟" "谭" "贡" "劳" "逄"
    "姬" "申" "扶" "堵" "冉" "宰" "郦" "雍" "却" "璩"
    "桑" "桂" "濮" "牛" "寿" "通" "边" "扈" "燕" "冀"
    "郏" "浦" "尚" "农" "温" "别" "庄" "晏" "符" "舒"
    "展" "杜" "艾" "蓝" "宋" "道" "郑" "吴"))

;; 关键词列表（按长度降序）
(define keywords-sorted
  '("大于等于" "小于等于" "不等于" "为主题" "定义宏" "定义变量"
    "输出" "定义" "变量" "如果" "则" "否则"
    "对于" "从" "到" "若" "就" "以"
    "大于" "小于" "等于" "加" "减" "乘" "除"
    "定" "是" "列" "算" "且" "或" "在" "之间"
    "当" "时" "返回" "印" "长度" "为"
    "导入" "导出" "从" "作为"))  ;; 新增导入导出关键词

;; 检查是否是姓氏
(define (is-surname? char)
  (define char-str (string char))
  (member char-str surnames))

;; 检查是否是关键词的开始
(define (is-keyword-start? text pos len)
  (for/or ([keyword keywords-sorted])
    (let ([kw-len (string-length keyword)])
      (and (<= (+ pos kw-len) len)
           (string=? (substring text pos (+ pos kw-len)) keyword)))))

;; 智能分词
(define (smart-tokenize text line-num)
  (define tokens '())
  (define pos 0)
  (define len (string-length text))
  
  (let loop ()
    (when (< pos len)
      (define char (string-ref text pos))
      
      (cond
        ;; 跳过空白
        [(char-whitespace? char)
         (set! pos (+ pos 1))
         (loop)]
        
        ;; 匹配字符串
        [(or (char=? char #\") (char=? char #\'))
         (let* ([quote-char char]
                [start pos])
           (set! pos (+ pos 1))
           (let find-end ()
             (when (and (< pos len)
                        (not (char=? (string-ref text pos) quote-char)))
               (set! pos (+ pos 1))
               (find-end)))
           (set! pos (+ pos 1))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'string line-num start))))
           (loop))]
        
        ;; 匹配数字
        [(or (char-numeric? char)
             (and (char=? char #\-)
                  (< (+ pos 1) len)
                  (char-numeric? (string-ref text (+ pos 1)))))
         (let ([start pos])
           (when (char=? char #\-)
             (set! pos (+ pos 1)))
           (let find-end ()
             (when (and (< pos len)
                        (or (char-numeric? (string-ref text pos))
                            (char=? (string-ref text pos) #\.)))
               (set! pos (+ pos 1))
               (find-end)))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'number line-num start))))
           (loop))]
        
        ;; 匹配中文关键词或标识符
        [(char>=? char #\一)
         (let ([matched-kw #f]
               [matched-len 0])
           (for ([keyword keywords-sorted])
             (let ([kw-len (string-length keyword)])
               (when (and (<= (+ pos kw-len) len)
                          (string=? (substring text pos (+ pos kw-len)) keyword)
                          (> kw-len matched-len))
                 (set! matched-kw keyword)
                 (set! matched-len kw-len))))
           
           (if matched-kw
               (begin
                 (set! tokens (append tokens 
                                     (list (token matched-kw 'keyword line-num pos))))
                 (set! pos (+ pos matched-len))
                 (loop))
               (if (is-surname? char)
                   (let ([start pos])
                     (let find-end ()
                       (when (and (< pos len)
                                  (char>=? (string-ref text pos) #\一)
                                  (not (is-keyword-start? text pos len)))
                         (set! pos (+ pos 1))
                         (find-end)))
                     (set! tokens (append tokens 
                                         (list (token (substring text start pos) 
                                                     'identifier line-num start))))
                     (loop))
                   (let ([start pos])
                     (set! pos (+ pos 1))
                     (set! tokens (append tokens 
                                         (list (token (substring text start pos) 
                                                     'identifier line-num start))))
                     (loop)))))]
        
        ;; 匹配英文标识符
        [(or (char-alphabetic? char) (char=? char #\_))
         (let ([start pos])
           (let find-end ()
             (when (and (< pos len)
                        (let ([c (string-ref text pos)])
                          (or (char-alphabetic? c)
                              (char-numeric? c)
                              (char=? c #\_))))
               (set! pos (+ pos 1))
               (find-end)))
           (set! tokens (append tokens 
                               (list (token (substring text start pos) 
                                           'identifier line-num start))))
           (loop))]
        
        ;; 匹配标点和括号
        [(or (char=? char #\，) (char=? char #\。)
             (char=? char #\：) (char=? char #\、)
             (char=? char #\() (char=? char #\))
             (char=? char #\[) (char=? char #\])
             (char=? char #\,))
         (set! tokens (append tokens 
                             (list (token (string char) 
                                         'punctuation line-num pos))))
         (set! pos (+ pos 1))
         (loop)]
        
        ;; 其他字符
        [else
         (set! pos (+ pos 1))
         (loop)])))
  
  tokens)

;; 分词一行
(define (tokenize-line line line-num)
  (define trimmed (string-trim line))
  (cond
    [(or (string=? trimmed "")
         (string-prefix? trimmed "#"))
     '()]
    [else
     (smart-tokenize trimmed line-num)]))

;; 查找token位置
(define (find-token-index tokens value)
  (for/first ([t tokens]
              [i (in-naturals)]
              #:when (string=? (token-value t) value))
    i))

;; 解析表达式
(define (parse-expression tokens)
  (cond
    [(null? tokens) 0]
    
    [(= (length tokens) 1)
     (define t (car tokens))
     (cond
       [(eq? (token-type t) 'number)
        (string->number (token-value t))]
       [(eq? (token-type t) 'string)
        (define str (token-value t))
        (substring str 1 (- (string-length str) 1))]
       [else
        (string->symbol (token-value t))])]
    
    ;; 检查是否是函数调用: 函数名(参数)
    [(and (>= (length tokens) 3)
          (eq? (token-type (car tokens)) 'identifier)
          (string=? (token-value (cadr tokens)) "("))
     (let* ([func-name (string->symbol (token-value (car tokens)))]
            ;; 找到匹配的右括号
            [rparen-pos (find-token-index tokens ")")])
       (if rparen-pos
           (let ([arg-tokens (take (drop tokens 2) (- rparen-pos 2))])
             ;; 解析参数（可能多个，用逗号分隔）
             (let ([args
                    (if (null? arg-tokens)
                        '()
                        (let loop ([tokens arg-tokens] [result '()] [current '()])
                          (if (null? tokens)
                              (if (null? current)
                                  (reverse result)
                                  (reverse (cons (parse-expression (reverse current)) result)))
                              (let ([t (car tokens)])
                                (if (or (string=? (token-value t) "，")
                                        (string=? (token-value t) ","))
                                    (if (null? current)
                                        (loop (cdr tokens) result '())
                                        (loop (cdr tokens)
                                              (cons (parse-expression (reverse current)) result)
                                              '()))
                                    (loop (cdr tokens) result (cons t current)))))))])
               ;; 生成函数调用
               `(,func-name ,@args)))
           ;; 没找到右括号，当作普通表达式
           (string->symbol (token-value (car tokens)))))]
    
    ;; 加法
    [(find-token-index tokens "加")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(+ ,left ,right))
              (string->symbol (token-value (car tokens)))))]
    
    ;; 减法
    [(find-token-index tokens "减")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(- ,left ,right))
              (string->symbol (token-value (car tokens)))))]
    
    [else
     (string->symbol (token-value (car tokens)))]))

;; 解析导入语句
;; 语法: 导入 "文件名.yan"
(define (parse-import-statement line-tokens base-path)
  (define import-pos (find-token-index line-tokens "导入"))
  (if (and import-pos (< (+ import-pos 1) (length line-tokens)))
      (let* ([file-token (list-ref line-tokens (+ import-pos 1))]
             [file-path (token-value file-token)])
        ;; 去掉引号
        (define clean-path
          (if (and (string-prefix? file-path "\"")
                   (string-suffix? file-path "\""))
              (substring file-path 1 (- (string-length file-path) 1))
              file-path))
        
        ;; 构建完整路径
        (define full-path
          (if (absolute-path? clean-path)
              clean-path
              (build-path base-path clean-path)))
        
        ;; 加载库文件
        (if (file-exists? full-path)
            (let ([lib-source (file->string full-path)])
              ;; 存储库源码
              (hash-set! import-table clean-path lib-source)
              
              ;; 解析并执行库代码，提取导出项
              (define lib-lines (string-split lib-source "\n"))
              (define lib-tokens
                (for/list ([line lib-lines]
                           [line-num (in-naturals 1)])
                  (tokenize-line line line-num)))
              
              ;; 处理库中的导出语句
              (define export-codes
                (for/list ([line-tokens lib-tokens]
                           #:when (not (null? line-tokens)))
                  (if (find-token-index line-tokens "导出")
                      (parse-export-statement line-tokens)
                      #f)))
              
              ;; 过滤并返回导出代码
              (define filtered-exports (filter identity export-codes))
              
              ;; 返回导入成功和导出项
              `(begin ,@filtered-exports))
            `(begin)))  ;; 文件不存在时返回空begin
      #f))

;; 解析导出语句
;; 语法: 导出 宏名(参数) 为 表达式
;; 语法: 导出 变量名 为 值
(define (parse-export-statement line-tokens)
  (define export-pos (find-token-index line-tokens "导出"))
  (define as-pos (find-token-index line-tokens "为"))
  
  (if (and export-pos as-pos (< (+ export-pos 1) (length line-tokens)))
      (let* ([name-token (list-ref line-tokens (+ export-pos 1))]
             [name (token-value name-token)]
             
             ;; 检查是否是宏导出（有括号）
             [lparen-pos (find-token-index line-tokens "(")]
             [rparen-pos (find-token-index line-tokens ")")])
        
        (if (and lparen-pos rparen-pos)
            ;; 导出宏
            (let* ([params (map (λ (t) (token-value t))
                               (filter (λ (t) (eq? (token-type t) 'identifier))
                                       (take (drop line-tokens (+ lparen-pos 1))
                                             (- rparen-pos lparen-pos 1))))]
                   [body-tokens (drop line-tokens (+ as-pos 1))]
                   [body-tokens-clean
                    (if (and (not (null? body-tokens))
                             (string=? (token-value (last body-tokens)) "。"))
                        (drop-right body-tokens 1)
                        body-tokens)])
              
              ;; 存储到导出表
              (hash-set! export-table name
                         (list 'macro params body-tokens-clean))
              
              ;; 同时存储到宏表
              (hash-set! macro-table name
                         (list params body-tokens-clean))
              
              ;; 返回宏定义代码（使其可执行）
              `(define ,(string->symbol name)
                 (λ ,(map string->symbol params)
                   ,(parse-expression body-tokens-clean))))
            
            ;; 导出变量
            (let* ([value-tokens (drop line-tokens (+ as-pos 1))]
                   [value-tokens-clean
                    (if (and (not (null? value-tokens))
                             (string=? (token-value (last value-tokens)) "。"))
                        (drop-right value-tokens 1)
                        value-tokens)]
                   [value (parse-expression value-tokens-clean)])
              
              ;; 存储到导出表
              (hash-set! export-table name
                         (list 'variable value))
              
              ;; 返回变量定义代码（使其可执行）
              `(define ,(string->symbol name) ,value))))
      #f))

;; 主读取函数
(define (read in)
  (syntax->datum (read-syntax #f in)))

(define (read-syntax src in)
  (define source (port->string in))
  (define lines (string-split source "\n"))
  
  ;; 获取基础路径
  (define base-path
    (if (and src (path? src))
        (path-only src)
        (string->path ".")))
  
  ;; 分词所有行
  (define all-tokens
    (for/list ([line lines]
               [line-num (in-naturals 1)])
      (tokenize-line line line-num)))
  
  ;; 解析语法
  (define racket-code
    (for/list ([line-tokens all-tokens]
               #:when (not (null? line-tokens)))
      (cond
        ;; 导入语句
        [(find-token-index line-tokens "导入")
         (parse-import-statement line-tokens base-path)]
        
        ;; 导出语句
        [(find-token-index line-tokens "导出")
         (parse-export-statement line-tokens)]
        
        ;; 宏定义
        [(find-token-index line-tokens "定义宏")
         '(begin)]
        
        ;; Python版本：定义变量x为10
        [(find-token-index line-tokens "定义变量")
         (let* ([var-pos (find-token-index line-tokens "定义变量")]
                [value-pos (find-token-index line-tokens "为")])
           (if (and var-pos value-pos 
                    (> (+ var-pos 1) 0)
                    (< (+ var-pos 1) (length line-tokens))
                    (< (+ value-pos 1) (length line-tokens)))
               (let* ([var-name (token-value (list-ref line-tokens (+ var-pos 1)))]
                      [var-value-tokens (drop line-tokens (+ value-pos 1))]
                      [var-value-tokens-clean
                       (if (and (not (null? var-value-tokens))
                                (string=? (token-value (last var-value-tokens)) "。"))
                           (drop-right var-value-tokens 1)
                           var-value-tokens)]
                      [var-value (parse-expression var-value-tokens-clean)])
                 `(define ,(string->symbol var-name) ,var-value))
               #f))]
        
        ;; Racket版本：定x是10
        [(find-token-index line-tokens "定")
         (let* ([name-pos (find-token-index line-tokens "定")]
                [value-pos (find-token-index line-tokens "是")])
           (if (and name-pos value-pos
                    (> (+ name-pos 1) 0)
                    (< (+ name-pos 1) (length line-tokens))
                    (< (+ value-pos 1) (length line-tokens)))
               (let* ([var-name (token-value (list-ref line-tokens (+ name-pos 1)))]
                      [var-value-tokens (drop line-tokens (+ value-pos 1))]
                      [var-value-tokens-clean
                       (if (and (not (null? var-value-tokens))
                                (string=? (token-value (last var-value-tokens)) "。"))
                           (drop-right var-value-tokens 1)
                           var-value-tokens)]
                      [var-value (parse-expression var-value-tokens-clean)])
                 `(define ,(string->symbol var-name) ,var-value))
               #f))]
        
        ;; 输出语句
        [(and (not (null? line-tokens))
              (string=? (token-value (car line-tokens)) "输出"))
         (let ([content (parse-expression (cdr line-tokens))])
           `(displayln ,content))]
        
        [else #f])))
  
  ;; 过滤掉#f
  (define filtered-code (filter identity racket-code))
  
  ;; 包装成begin块
  (define final-code
    (if (null? filtered-code)
        '(begin)
        (if (= (length filtered-code) 1)
            (car filtered-code)
            `(begin ,@filtered-code))))
  
  (datum->syntax #f final-code))
