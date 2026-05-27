import * as vscode from 'vscode';
import { YanLvCompletionItemProvider } from './completionProvider';
import { YanLvDiagnosticProvider } from './diagnosticProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('言律语言插件已激活');

    // 注册自动补全提供者
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        'yanlv',
        new YanLvCompletionItemProvider(),
        '.', ' ', '定', '函', '如', '循', '输'
    );

    // 注册诊断提供者
    const diagnosticProvider = new YanLvDiagnosticProvider();
    const diagnostics = vscode.languages.createDiagnosticCollection('yanlv');
    
    // 订阅文档变化事件
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => {
            diagnosticProvider.provideDiagnostics(event.document, diagnostics);
        })
    );

    // 订阅文档打开事件
    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(document => {
            diagnosticProvider.provideDiagnostics(document, diagnostics);
        })
    );

    // 注册编译命令
    const compileCommand = vscode.commands.registerCommand('yanlv.compile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            vscode.window.showInformationMessage('编译言律代码...');
            // 这里可以调用编译器
        }
    });

    // 注册运行命令
    const runCommand = vscode.commands.registerCommand('yanlv.run', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            vscode.window.showInformationMessage('运行言律代码...');
            // 这里可以调用解释器
        }
    });

    context.subscriptions.push(
        completionProvider,
        diagnostics,
        compileCommand,
        runCommand
    );
}

export function deactivate() {
    console.log('言律语言插件已停用');
}
