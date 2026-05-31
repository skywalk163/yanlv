#lang racket

;; ========================================
;; 言律语言宏系统版读取器
;; 支持宏定义、宏展开、宏调用
;; ========================================

(provide read read-syntax tokenize-line macro-table)

;; Token结构
(struct token (value type line col) #:transparent)

;; 宏表：存储定义的宏
(define macro-table (make-hash))

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
    "当" "时" "返回" "印" "长度" "为"))

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
             (char=? char #\,))  ;; 添加英文逗号
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

;; 解析条件
(define (parse-condition tokens)
  (cond
    [(null? tokens) #f]
    
    [(find-token-index tokens "大于等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(>= ,left ,right))
              #f))]
    
    [(find-token-index tokens "小于等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(<= ,left ,right))
              #f))]
    
    [(find-token-index tokens "大于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(> ,left ,right))
              #f))]
    
    [(find-token-index tokens "小于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(< ,left ,right))
              #f))]
    
    [(find-token-index tokens "等于")
     => (λ (pos)
          (if (and (> pos 0) (< (+ pos 1) (length tokens)))
              (let ([left (parse-expression (take tokens pos))]
                    [right (parse-expression (drop tokens (+ pos 1)))])
                `(= ,left ,right))
              #f))]
    
    [else (parse-expression tokens)]))

;; 解析动作
(define (parse-action tokens)
  (cond
    [(null? tokens) #f]
    [(string=? (token-value (car tokens)) "输出")
     (let ([content (parse-expression (cdr tokens))])
       `(displayln ,content))]
    [else (parse-expression tokens)]))

;; 解析因果链
(define (parse-causal-chain tokens)
  (define comma-pos (find-token-index tokens "，"))
  (define period-pos (find-token-index tokens "。"))
  (if (and comma-pos period-pos (> comma-pos 0))
      (let ([condition-tokens (take tokens comma-pos)]
            [action-tokens (take (drop tokens (+ comma-pos 1)) 
                                (- period-pos comma-pos 1))])
        (let ([condition (parse-condition condition-tokens)]
              [action (parse-action action-tokens)])
          (if (and condition action)
              `(when ,condition ,action)
              #f)))
      #f))

;; 解析宏定义
;; 语法: 定义宏 宏名(参数) 为 表达式
(define (parse-macro-definition line-tokens)
  (define macro-pos (find-token-index line-tokens "定义宏"))
  (define as-pos (find-token-index line-tokens "为"))
  
  (if (and macro-pos as-pos
           (< (+ macro-pos 1) (length line-tokens)))
      (let* ([name-token (list-ref line-tokens (+ macro-pos 1))]
             [macro-name (token-value name-token)]
             
             ;; 查找参数列表 ( )
             [lparen-pos (find-token-index line-tokens "(")]
             [rparen-pos (find-token-index line-tokens ")")]
             
             ;; 提取参数
             [params (if (and lparen-pos rparen-pos (> rparen-pos lparen-pos))
                        (map (λ (t) (token-value t))
                             (filter (λ (t) (eq? (token-type t) 'identifier))
                                     (take (drop line-tokens (+ lparen-pos 1))
                                           (- rparen-pos lparen-pos 1))))
                        '())]
             
             ;; 提取宏体
             [body-tokens (drop line-tokens (+ as-pos 1))]
             [body-tokens-clean
              (if (and (not (null? body-tokens))
                       (string=? (token-value (last body-tokens)) "。"))
                  (drop-right body-tokens 1)
                  body-tokens)])
        
        ;; 存储宏定义
        (hash-set! macro-table macro-name
                   (list params body-tokens-clean))
        
        ;; 返回宏定义信息
        `(macro-defined ,macro-name ,params))
      #f))

;; 宏展开
(define (expand-macro macro-name arg-tokens-list)
  (define macro-def (hash-ref macro-table macro-name #f))
  (if macro-def
      (let ([params (car macro-def)]
            [body-tokens (cadr macro-def)])
        ;; 参数替换 - 将参数token替换为实参token
        (define body-with-args
          (for/list ([t body-tokens])
            (define token-val (token-value t))
            (define param-index (index-of params token-val))
            (if param-index
                ;; 参数被替换为实参token列表
                (list-ref arg-tokens-list param-index)
                ;; 非参数token保持不变，包装为列表
                (list t))))
        
        ;; 展平token列表
        (define flattened-tokens
          (apply append body-with-args))
        
        ;; 解析展开后的表达式
        (parse-expression flattened-tokens))
      #f))

;; 检查是否是宏调用
(define (try-macro-call tokens)
  (if (null? tokens)
      #f
      (let ([first-token (car tokens)])
        (if (and (eq? (token-type first-token) 'identifier)
                 (hash-has-key? macro-table (token-value first-token)))
            ;; 可能是宏调用
            (let* ([macro-name (token-value first-token)]
                   [lparen-pos (find-token-index tokens "(")]
                   [rparen-pos (find-token-index tokens ")")])
              (if (and lparen-pos rparen-pos)
                  ;; 提取参数token（不解析）
                  (let ([arg-tokens
                         (take (drop tokens (+ lparen-pos 1))
                               (- rparen-pos lparen-pos 1))])
                    ;; 分割参数（按逗号）- 返回token列表的列表
                    (define arg-tokens-list
                      (let loop ([tokens arg-tokens] [result '()] [current '()])
                        (if (null? tokens)
                            (if (null? current)
                                (reverse result)
                                (reverse (cons current result)))
                            (let ([t (car tokens)])
                              ;; 检查是否是逗号（中文或英文）
                              (if (or (and (eq? (token-type t) 'punctuation)
                                          (or (string=? (token-value t) "，")
                                              (string=? (token-value t) ",")))
                                      (string=? (token-value t) "，")
                                      (string=? (token-value t) ","))
                                  (if (null? current)
                                      (loop (cdr tokens) result '())
                                      (loop (cdr tokens)
                                            (cons current result)
                                            '()))
                                  (loop (cdr tokens) result (cons t current)))))))
                    
                    (expand-macro macro-name arg-tokens-list))
                  #f))
            #f))))

;; 主读取函数
(define (read in)
  (syntax->datum (read-syntax #f in)))

(define (read-syntax src in)
  (define source (port->string in))
  (define lines (string-split source "\n"))
  
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
        ;; 宏定义
        [(find-token-index line-tokens "定义宏")
         (parse-macro-definition line-tokens)
         '(begin)]  ;; 宏定义不生成执行代码
        
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
        
        ;; 因果链
        [(and (find-token-index line-tokens "，")
              (find-token-index line-tokens "。"))
         (parse-causal-chain line-tokens)]
        
        ;; 输出语句（可能包含宏调用）
        [(and (not (null? line-tokens))
              (string=? (token-value (car line-tokens)) "输出"))
         (let ([content-tokens (cdr line-tokens)])
           ;; 检查是否是宏调用
           (define macro-expanded (try-macro-call content-tokens))
           (if macro-expanded
               `(displayln ,macro-expanded)
               (let ([content (parse-expression content-tokens)])
                 `(displayln ,content))))]
        
        ;; 尝试宏调用
        [(try-macro-call line-tokens)
         => (λ (expanded) expanded)]
        
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
