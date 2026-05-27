// 言律在线IDE - 主应用

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
结束

输出"遍历数组:"
定义数组arr为[10, 20, 30, 40, 50]
每个item在arr执行
  输出item
结束`,
    
    function: `// 函数示例
函数加法参数a b
  返回a加b
结束

函数平方参数x
  返回x乘x
结束

输出"10 + 20 = "
输出调用加法参数10 20

输出"5的平方 = "
输出调用平方参数5`,
    
    array: `// 数组操作
定义数组arr为[3, 1, 4, 1, 5, 9, 2, 6]

输出"原数组: "
输出arr

输出"排序后: "
输出排序arr

输出"求和: "
输出求和arr

输出"平均值: "
输出平均值arr

输出"最大值: "
输出最大值arr

输出"最小值: "
输出最小值arr`,
    
    fibonacci: `// 斐波那契数列
函数斐波那契参数n
  如果n小于等于1则
    返回n
  否则
    返回调用斐波那契参数n减1 加 调用斐波那契参数n减2
  结束
结束

输出"斐波那契数列前10项:"
循环10次执行
  输出调用斐波那契参数i
结束`
};

// DOM元素
const editor = document.getElementById('editor');
const output = document.getElementById('output');
const compiledCode = document.getElementById('compiledCode');
const compiledPanel = document.getElementById('compiledPanel');
const exampleModal = document.getElementById('exampleModal');
const targetSelect = document.getElementById('targetSelect');

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

// 运行代码
function runCode() {
    const code = editor.value;
    if (!code.trim()) {
        showOutput('请输入代码', 'error');
        return;
    }
    
    clearOutput();
    showOutput('正在运行...', 'info');
    
    // 模拟运行（实际应该调用后端API）
    setTimeout(() => {
        try {
            const result = simulateRun(code);
            clearOutput();
            result.forEach(line => {
                showOutput(line, 'success');
            });
        } catch (error) {
            clearOutput();
            showOutput('运行错误: ' + error.message, 'error');
        }
    }, 500);
}

// 编译代码
function compileCode() {
    const code = editor.value;
    const target = targetSelect.value;
    
    if (!code.trim()) {
        showOutput('请输入代码', 'error');
        return;
    }
    
    showOutput('正在编译...', 'info');
    
    // 模拟编译（实际应该调用后端API）
    setTimeout(() => {
        try {
            const compiled = simulateCompile(code, target);
            compiledCode.textContent = compiled;
            compiledPanel.style.display = 'block';
            clearOutput();
            showOutput('编译成功！', 'success');
        } catch (error) {
            clearOutput();
            showOutput('编译错误: ' + error.message, 'error');
        }
    }, 500);
}

// 模拟运行
function simulateRun(code) {
    const results = [];
    const lines = code.split('\n');
    
    for (const line of lines) {
        const trimmed = line.trim();
        
        // 处理输出语句
        if (trimmed.startsWith('输出')) {
            const content = trimmed.substring(2).trim();
            
            // 移除引号
            let value = content;
            if (value.startsWith('"') && value.endsWith('"')) {
                value = value.slice(1, -1);
            } else if (value.startsWith("'") && value.endsWith("'")) {
                value = value.slice(1, -1);
            }
            
            results.push('=> ' + value);
        }
        
        // 处理循环
        if (trimmed.startsWith('循环')) {
            const match = trimmed.match(/循环(\d+)次执行/);
            if (match) {
                const times = parseInt(match[1]);
                for (let i = 0; i < times; i++) {
                    results.push('=> ' + i);
                }
            }
        }
    }
    
    return results.length > 0 ? results : ['=> (无输出)'];
}

// 模拟编译
function simulateCompile(code, target) {
    const lines = code.split('\n');
    const compiled = [];
    
    for (const line of lines) {
        const trimmed = line.trim();
        
        if (target === 'python') {
            // 转换为Python
            if (trimmed.startsWith('定义变量')) {
                const match = trimmed.match(/定义变量(\w+)为(.+)/);
                if (match) {
                    compiled.push(`${match[1]} = ${match[2]}`);
                }
            } else if (trimmed.startsWith('输出')) {
                const content = trimmed.substring(2).trim();
                compiled.push(`print(${content})`);
            }
        } else if (target === 'javascript') {
            // 转换为JavaScript
            if (trimmed.startsWith('定义变量')) {
                const match = trimmed.match(/定义变量(\w+)为(.+)/);
                if (match) {
                    compiled.push(`let ${match[1]} = ${match[2]};`);
                }
            } else if (trimmed.startsWith('输出')) {
                const content = trimmed.substring(2).trim();
                compiled.push(`console.log(${content});`);
            }
        }
    }
    
    return compiled.join('\n') || '// (无代码生成)';
}

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
