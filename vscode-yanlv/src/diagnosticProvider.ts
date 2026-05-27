import * as vscode from 'vscode';

export class YanLvDiagnosticProvider {
    provideDiagnostics(
        document: vscode.TextDocument,
        diagnostics: vscode.DiagnosticCollection
    ): void {
        const diagnosticList: vscode.Diagnostic[] = [];
        const text = document.getText();
        const lines = text.split('\n');
        
        // 检查未闭合的块
        const blockStack: { keyword: string; line: number }[] = [];
        
        lines.forEach((line, lineIndex) => {
            const trimmedLine = line.trim();
            
            // 检查块开始
            if (trimmedLine.match(/^(如果|当|循环|函数|尝试|捕获|模块)/)) {
                const keyword = trimmedLine.split(/\s+/)[0];
                blockStack.push({ keyword, line: lineIndex });
            }
            
            // 检查块结束
            if (trimmedLine === '结束') {
                if (blockStack.length === 0) {
                    // 多余的结束
                    const range = new vscode.Range(
                        new vscode.Position(lineIndex, 0),
                        new vscode.Position(lineIndex, line.length)
                    );
                    const diagnostic = new vscode.Diagnostic(
                        range,
                        '多余的结束语句',
                        vscode.DiagnosticSeverity.Error
                    );
                    diagnosticList.push(diagnostic);
                } else {
                    blockStack.pop();
                }
            }
        });
        
        // 检查未闭合的块
        blockStack.forEach(block => {
            const range = new vscode.Range(
                new vscode.Position(block.line, 0),
                new vscode.Position(block.line, lines[block.line].length)
            );
            const diagnostic = new vscode.Diagnostic(
                range,
                `未闭合的${block.keyword}块`,
                vscode.DiagnosticSeverity.Error
            );
            diagnosticList.push(diagnostic);
        });
        
        // 检查语法错误
        lines.forEach((line, lineIndex) => {
            const trimmedLine = line.trim();
            
            // 检查变量定义
            if (trimmedLine.startsWith('定义变量')) {
                if (!trimmedLine.match(/定义变量\s+\S+\s+为\s+\S+/)) {
                    const range = new vscode.Range(
                        new vscode.Position(lineIndex, 0),
                        new vscode.Position(lineIndex, line.length)
                    );
                    const diagnostic = new vscode.Diagnostic(
                        range,
                        '变量定义语法错误，应为：定义变量 名字 为 值',
                        vscode.DiagnosticSeverity.Warning
                    );
                    diagnosticList.push(diagnostic);
                }
            }
            
            // 检查函数定义
            if (trimmedLine.startsWith('函数')) {
                if (!trimmedLine.match(/函数\s+\S+\s+参数/)) {
                    const range = new vscode.Range(
                        new vscode.Position(lineIndex, 0),
                        new vscode.Position(lineIndex, line.length)
                    );
                    const diagnostic = new vscode.Diagnostic(
                        range,
                        '函数定义语法错误，应为：函数 名字 参数 参数列表',
                        vscode.DiagnosticSeverity.Warning
                    );
                    diagnosticList.push(diagnostic);
                }
            }
            
            // 检查条件语句
            if (trimmedLine.startsWith('如果')) {
                if (!trimmedLine.match(/如果\s+.+\s+则/)) {
                    const range = new vscode.Range(
                        new vscode.Position(lineIndex, 0),
                        new vscode.Position(lineIndex, line.length)
                    );
                    const diagnostic = new vscode.Diagnostic(
                        range,
                        '条件语句语法错误，应为：如果 条件 则',
                        vscode.DiagnosticSeverity.Warning
                    );
                    diagnosticList.push(diagnostic);
                }
            }
        });
        
        diagnostics.set(document.uri, diagnosticList);
    }
}
