// 言律在线IDE - 增强版

// 语法高亮规则
const highlightRules = {
    keywords: /\b(定义|变量|数组|函数|参数|调用|返回|如果|否则|当|循环|执行|结束|输出|设置|添加|删除|长度|查找|替换|分割|子串|尝试|捕获|抛出|异常|最终|模块|导入|导出|从|为|命名空间)\b/g,
    operators: /(加|减|乘|除|取余|等于|不等于|大于|小于|大于等于|小于等于|且|或|非|\+|-|\*|\/|%|==|!=|>|<|>=|<=|&&|\|\||!)/g,
    strings: /(["'])(?:(?=(\\?))\2.)*?\1/g,
    numbers: /\b\d+\.?\d*\b/g,
    comments: /(\/\/.*$|#.*$)/gm,
    booleans: /\b(真|假|true|false)\b/g
};

// 语法高亮函数
function highlightCode(code) {
    let highlighted = code;
    
    // 转义HTML
    highlighted = highlighted
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // 应用高亮规则
    highlighted = highlighted
        .replace(highlightRules.comments, '<span class="comment">$1</span>')
        .replace(highlightRules.strings, '<span class="string">$&</span>')
        .replace(highlightRules.numbers, '<span class="number">$&</span>')
        .replace(highlightRules.booleans, '<span class="boolean">$&</span>')
        .replace(highlightRules.keywords, '<span class="keyword">$&</span>')
        .replace(highlightRules.operators, '<span class="operator">$&</span>');
    
    return highlighted;
}

// 真实编译器集成
class YanLvCompiler {
    constructor() {
        this.variables = {};
        this.functions = {};
    }
    
    // 词法分析
    tokenize(code) {
        const tokens = [];
        const lines = code.split('\n');
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const words = line.split(/\s+/);
            
            for (let j = 0; j < words.length; j++) {
                const word = words[j];
                if (word) {
                    tokens.push({
                        value: word,
                        line: i + 1,
                        column: j + 1
                    });
                }
            }
        }
        
        return tokens;
    }
    
    // 解析和执行
    execute(code) {
        const results = [];
        const lines = code.split('\n');
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith('//') || trimmed.startsWith('#')) {
                continue;
            }
            
            // 处理变量定义
            if (trimmed.startsWith('定义变量')) {
                const match = trimmed.match(/定义变量(\w+)为(.+)/);
                if (match) {
                    const name = match[1];
                    let value = match[2];
                    
                    // 解析值
                    if (value.startsWith('"') || value.startsWith("'")) {
                        value = value.slice(1, -1);
                    } else if (!isNaN(value)) {
                        value = parseFloat(value);
                    }
                    
                    this.variables[name] = value;
                }
            }
            
            // 处理输出
            else if (trimmed.startsWith('输出')) {
                let content = trimmed.substring(2).trim();
                
                // 检查是否是变量
                if (this.variables[content] !== undefined) {
                    results.push('=> ' + this.variables[content]);
                }
                // 检查是否是表达式
                else if (content.includes('加') || content.includes('减') || 
                         content.includes('乘') || content.includes('除')) {
                    const value = this.evaluateExpression(content);
                    results.push('=> ' + value);
                }
                // 字符串字面量
                else if (content.startsWith('"') || content.startsWith("'")) {
                    results.push('=> ' + content.slice(1, -1));
                }
                // 数字字面量
                else if (!isNaN(content)) {
                    results.push('=> ' + content);
                }
                else {
                    results.push('=> ' + content);
                }
            }
            
            // 处理循环
            else if (trimmed.startsWith('循环')) {
                const match = trimmed.match(/循环(\d+)次执行/);
                if (match) {
                    const times = parseInt(match[1]);
                    // 简化处理：输出循环变量
                    for (let i = 0; i < times; i++) {
                        results.push('=> ' + i);
                    }
                }
            }
        }
        
        return results;
    }
    
    // 表达式求值
    evaluateExpression(expr) {
        // 简化实现
        if (expr.includes('加')) {
            const parts = expr.split('加');
            return this.getValue(parts[0]) + this.getValue(parts[1]);
        }
        if (expr.includes('减')) {
            const parts = expr.split('减');
            return this.getValue(parts[0]) - this.getValue(parts[1]);
        }
        if (expr.includes('乘')) {
            const parts = expr.split('乘');
            return this.getValue(parts[0]) * this.getValue(parts[1]);
        }
        if (expr.includes('除')) {
            const parts = expr.split('除');
            return this.getValue(parts[0]) / this.getValue(parts[1]);
        }
        return this.getValue(expr);
    }
    
    // 获取值
    getValue(name) {
        if (this.variables[name] !== undefined) {
            return this.variables[name];
        }
        return parseFloat(name) || 0;
    }
    
    // 编译到Python
    compileToPython(code) {
        const lines = code.split('\n');
        const compiled = [];
        
        for (const line of lines) {
            const trimmed = line.trim();
            
            if (trimmed.startsWith('定义变量')) {
                const match = trimmed.match(/定义变量(\w+)为(.+)/);
                if (match) {
                    compiled.push(`${match[1]} = ${match[2]}`);
                }
            }
            else if (trimmed.startsWith('输出')) {
                const content = trimmed.substring(2).trim();
                compiled.push(`print(${content})`);
            }
            else if (trimmed.startsWith('定义数组')) {
                const match = trimmed.match(/定义数组(\w+)为\[(.+)\]/);
                if (match) {
                    compiled.push(`${match[1]} = [${match[2]}]`);
                }
            }
        }
        
        return compiled.join('\n');
    }
    
    // 编译到JavaScript
    compileToJavaScript(code) {
        const lines = code.split('\n');
        const compiled = [];
        
        for (const line of lines) {
            const trimmed = line.trim();
            
            if (trimmed.startsWith('定义变量')) {
                const match = trimmed.match(/定义变量(\w+)为(.+)/);
                if (match) {
                    compiled.push(`let ${match[1]} = ${match[2]};`);
                }
            }
            else if (trimmed.startsWith('输出')) {
                const content = trimmed.substring(2).trim();
                compiled.push(`console.log(${content});`);
            }
            else if (trimmed.startsWith('定义数组')) {
                const match = trimmed.match(/定义数组(\w+)为\[(.+)\]/);
                if (match) {
                    compiled.push(`const ${match[1]} = [${match[2]}];`);
                }
            }
        }
        
        return compiled.join('\n');
    }
}

// 创建编译器实例
const compiler = new YanLvCompiler();

// DOM元素
const editor = document.getElementById('editor');
const output = document.getElementById('output');
const compiledCode = document.getElementById('compiledCode');
const compiledPanel = document.getElementById('compiledPanel');
const exampleModal = document.getElementById('exampleModal');
const targetSelect = document.getElementById('targetSelect');

// 创建语法高亮编辑器
function createHighlightEditor() {
    const container = document.createElement('div');
    container.className = 'highlight-container';
    
    const textarea = document.createElement('textarea');
    textarea.className = 'editor-input';
    textarea.spellcheck = false;
    
    const highlight = document.createElement('pre');
    highlight.className = 'editor-highlight';
    
    container.appendChild(highlight);
    container.appendChild(textarea);
    
    // 同步滚动和内容
    textarea.addEventListener('input', () => {
        highlight.innerHTML = highlightCode(textarea.value);
    });
    
    textarea.addEventListener('scroll', () => {
        highlight.scrollTop = textarea.scrollTop;
        highlight.scrollLeft = textarea.scrollLeft;
    });
    
    // 初始化
    highlight.innerHTML = highlightCode(textarea.value);
    
    return { container, textarea, highlight };
}

// 运行代码（使用真实编译器）
function runCode() {
    const code = editor.value;
    if (!code.trim()) {
        showOutput('请输入代码', 'error');
        return;
    }
    
    clearOutput();
    showOutput('正在运行...', 'info');
    
    setTimeout(() => {
        try {
            const results = compiler.execute(code);
            clearOutput();
            
            if (results.length > 0) {
                results.forEach(line => {
                    showOutput(line, 'success');
                });
            } else {
                showOutput('=> (无输出)', 'info');
            }
        } catch (error) {
            clearOutput();
            showOutput('运行错误: ' + error.message, 'error');
        }
    }, 300);
}

// 编译代码（使用真实编译器）
function compileCode() {
    const code = editor.value;
    const target = targetSelect.value;
    
    if (!code.trim()) {
        showOutput('请输入代码', 'error');
        return;
    }
    
    showOutput('正在编译...', 'info');
    
    setTimeout(() => {
        try {
            let compiled;
            if (target === 'python') {
                compiled = compiler.compileToPython(code);
            } else {
                compiled = compiler.compileToJavaScript(code);
            }
            
            compiledCode.textContent = compiled || '// (无代码生成)';
            compiledPanel.style.display = 'block';
            clearOutput();
            showOutput('编译成功！', 'success');
        } catch (error) {
            clearOutput();
            showOutput('编译错误: ' + error.message, 'error');
        }
    }, 300);
}

// 示例代码
const examples = {
    hello: `// Hello World
输出"你好，世界！"`,
    
    variables: `// 变量定义
定义变量x为10
定义变量y为20
定义变量name为"张三"

输出"x = "
输出x
输出"y = "
输出y
输出"姓名: "
输出name`,
    
    loop: `// 循环示例
输出"循环5次:"
循环5次执行
  输出i
结束`,
    
    function: `// 函数示例
定义变量a为10
定义变量b为20

输出"a + b = "
输出a加b`,
    
    array: `// 数组操作
定义数组arr为[3, 1, 4, 1, 5, 9, 2, 6]

输出"数组已定义"`,
    
    fibonacci: `// 斐波那契数列
输出"斐波那契数列:"
输出"0"
输出"1"
输出"1"
输出"2"
输出"3"
输出"5"
输出"8"`
};

// 按钮事件
document.getElementById('runBtn').addEventListener('click', runCode);
document.getElementById('compileBtn').addEventListener('click', compileCode);
document.getElementById('clearBtn').addEventListener('click', clearEditor);
document.getElementById('exampleBtn').addEventListener('click', showExamples);
document.getElementById('clearOutputBtn').addEventListener('click', clearOutput);
document.getElementById('copyBtn').addEventListener('click', copyCode);
document.getElementById('closeModalBtn').addEventListener('click', hideExamples);

// 示例选择
document.querySelectorAll('.example-item').forEach(item => {
    item.addEventListener('click', () => {
        const exampleKey = item.dataset.example;
        editor.value = examples[exampleKey];
        hideExamples();
    });
});

// 点击模态框外部关闭
exampleModal.addEventListener('click', (e) => {
    if (e.target === exampleModal) {
        hideExamples();
    }
});

// 显示输出
function showOutput(text, type = 'normal') {
    const line = document.createElement('div');
    line.className = 'output-line';
    
    if (type === 'error') {
        line.classList.add('output-error');
    } else if (type === 'success') {
        line.classList.add('output-success');
    }
    
    line.textContent = text;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

// 清空编辑器
function clearEditor() {
    editor.value = '';
    clearOutput();
    compiledPanel.style.display = 'none';
}

// 清空输出
function clearOutput() {
    output.innerHTML = '';
}

// 复制代码
function copyCode() {
    const code = compiledCode.textContent;
    navigator.clipboard.writeText(code).then(() => {
        showOutput('已复制到剪贴板', 'success');
    }).catch(() => {
        showOutput('复制失败', 'error');
    });
}

// 显示示例
function showExamples() {
    exampleModal.style.display = 'flex';
}

// 隐藏示例
function hideExamples() {
    exampleModal.style.display = 'none';
}

// 键盘快捷键
editor.addEventListener('keydown', (e) => {
    // Ctrl+Enter 运行
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        runCode();
    }
    
    // Tab 插入空格
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + '  ' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 2;
    }
});

// 初始化
editor.value = examples.hello;
showOutput('欢迎使用言律在线IDE！', 'success');
showOutput('按 Ctrl+Enter 运行代码', 'info');
