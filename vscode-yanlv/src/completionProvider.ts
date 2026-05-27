import * as vscode from 'vscode';

export class YanLvCompletionItemProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.ProviderResult<vscode.CompletionItem[] | vscode.CompletionList> {
        
        const items: vscode.CompletionItem[] = [];
        
        // 关键字补全
        const keywords = [
            '定义', '变量', '数组', '函数', '参数', '调用', '返回',
            '如果', '否则', '当', '循环', '执行', '结束',
            '输出', '设置', '添加', '删除', '长度',
            '尝试', '捕获', '抛出', '异常', '最终',
            '模块', '导入', '导出', '从', '为'
        ];
        
        keywords.forEach(keyword => {
            const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
            item.detail = '关键字';
            items.push(item);
        });
        
        // 内置函数补全
        const builtins = [
            { name: '输出', snippet: '输出${1:内容}' },
            { name: '定义变量', snippet: '定义变量${1:变量名}为${2:值}' },
            { name: '定义数组', snippet: '定义数组${1:数组名}为[${2:元素}]' },
            { name: '设置', snippet: '设置${1:变量}为${2:值}' },
            { name: '添加', snippet: '添加${1:元素}到${2:数组}' },
            { name: '删除', snippet: '从${1:数组}删除${2:元素}' },
            { name: '长度', snippet: '长度${1:数组或字符串}' },
            { name: '查找', snippet: '在${1:字符串}中查找${2:子串}' },
            { name: '替换', snippet: '在${1:字符串}中替换${2:旧值}为${3:新值}' },
            { name: '分割', snippet: '分割${1:字符串}为${2:分隔符}' },
            { name: '子串', snippet: '子串${1:字符串}从${2:开始}到${3:结束}' }
        ];
        
        builtins.forEach(builtin => {
            const item = new vscode.CompletionItem(builtin.name, vscode.CompletionItemKind.Function);
            item.insertText = new vscode.SnippetString(builtin.snippet);
            item.detail = '内置函数';
            items.push(item);
        });
        
        // 数学函数
        const mathFunctions = [
            { name: '加', snippet: '加${1:a}${2:b}' },
            { name: '减', snippet: '减${1:a}${2:b}' },
            { name: '乘', snippet: '乘${1:a}${2:b}' },
            { name: '除', snippet: '除${1:a}${2:b}' },
            { name: '取余', snippet: '取余${1:a}${2:b}' },
            { name: '幂', snippet: '幂${1:base}${2:exp}' },
            { name: '开方', snippet: '开方${1:x}' },
            { name: '绝对值', snippet: '绝对值${1:x}' },
            { name: '正弦', snippet: '正弦${1:x}' },
            { name: '余弦', snippet: '余弦${1:x}' },
            { name: '正切', snippet: '正切${1:x}' },
            { name: '对数', snippet: '对数${1:x}' },
            { name: '指数', snippet: '指数${1:x}' }
        ];
        
        mathFunctions.forEach(func => {
            const item = new vscode.CompletionItem(func.name, vscode.CompletionItemKind.Function);
            item.insertText = new vscode.SnippetString(func.snippet);
            item.detail = '数学函数';
            items.push(item);
        });
        
        // 比较运算符
        const operators = [
            { name: '等于', snippet: '等于' },
            { name: '不等于', snippet: '不等于' },
            { name: '大于', snippet: '大于' },
            { name: '小于', snippet: '小于' },
            { name: '大于等于', snippet: '大于等于' },
            { name: '小于等于', snippet: '小于等于' },
            { name: '且', snippet: '且' },
            { name: '或', snippet: '或' },
            { name: '非', snippet: '非' }
        ];
        
        operators.forEach(op => {
            const item = new vscode.CompletionItem(op.name, vscode.CompletionItemKind.Operator);
            item.insertText = new vscode.SnippetString(op.snippet);
            item.detail = '运算符';
            items.push(item);
        });
        
        return items;
    }
}
