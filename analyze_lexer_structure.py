"""
分析lexer.py文件结构
"""

import re
import os

def analyze_lexer_structure():
    """分析lexer.py文件结构"""
    lexer_path = 'src/yanlv/lexer/lexer.py'
    
    if not os.path.exists(lexer_path):
        print(f"文件不存在: {lexer_path}")
        return
    
    print("分析lexer.py文件结构")
    print("=" * 80)
    
    # 读取文件
    with open(lexer_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # 分析类定义
    class_pattern = r'^class\s+(\w+)\s*\(?([^)]*)\)?\s*:'
    classes = []
    for match in re.finditer(class_pattern, content, re.MULTILINE):
        class_name = match.group(1)
        inheritance = match.group(2).strip()
        line_num = content[:match.start()].count('\n') + 1
        classes.append((line_num, class_name, inheritance))
    
    print(f"找到 {len(classes)} 个类:")
    for line_num, class_name, inheritance in classes:
        try:
            print(f"  第{line_num:4d}行: class {class_name}({inheritance})")
        except UnicodeEncodeError:
            print(f"  第{line_num:4d}行: class {class_name.encode('ascii', 'ignore').decode()}({inheritance.encode('ascii', 'ignore').decode()})")
    
    # 分析函数定义
    function_pattern = r'^def\s+(\w+)\s*\(([^)]*)\)\s*(->\s*[^:]+)?\s*:'
    functions = []
    for match in re.finditer(function_pattern, content, re.MULTILINE):
        func_name = match.group(1)
        params = match.group(2)
        return_type = match.group(3) or ''
        line_num = content[:match.start()].count('\n') + 1
        functions.append((line_num, func_name, params, return_type))
    
    print(f"\n找到 {len(functions)} 个函数 (显示前50个):")
    for i, (line_num, func_name, params, return_type) in enumerate(functions[:50]):
        print(f"  第{line_num:4d}行: def {func_name}({params}){return_type}")
    
    # 分析导入语句
    import_pattern = r'^(import\s+[\w., ]+|from\s+[\w.]+\s+import\s+[\w., *]+)'
    imports = []
    for match in re.finditer(import_pattern, content, re.MULTILINE):
        import_stmt = match.group(1).strip()
        line_num = content[:match.start()].count('\n') + 1
        imports.append((line_num, import_stmt))
    
    print(f"\n找到 {len(imports)} 个导入语句:")
    for line_num, import_stmt in imports:
        print(f"  第{line_num:4d}行: {import_stmt}")
    
    # 分析常量定义
    constant_pattern = r'^([A-Z_][A-Z0-9_]*)\s*=\s*[^#\n]+'
    constants = []
    for match in re.finditer(constant_pattern, content, re.MULTILINE):
        const_name = match.group(1)
        line_num = content[:match.start()].count('\n') + 1
        constants.append((line_num, const_name))
    
    print(f"\n找到 {len(constants)} 个常量 (显示前20个):")
    for i, (line_num, const_name) in enumerate(constants[:20]):
        print(f"  第{line_num:4d}行: {const_name}")
    
    # 分析代码块
    print("\n代码块分析:")
    
    # 按缩进级别分析
    lines = content.split('\n')
    indent_levels = {}
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            indent_levels[indent] = indent_levels.get(indent, 0) + 1
    
    print("缩进级别统计:")
    for indent, count in sorted(indent_levels.items()):
        print(f"  缩进{indent}空格: {count}行")
    
    # 分析函数长度
    print("\n函数长度分析:")
    func_lengths = []
    current_func = None
    func_start = 0
    func_indent = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 检测函数开始
        if stripped.startswith('def '):
            if current_func:
                func_length = i - func_start
                func_lengths.append((current_func, func_length))
            
            current_func = stripped.split('def ')[1].split('(')[0]
            func_start = i
            func_indent = len(line) - len(line.lstrip())
        
        # 检测函数结束（遇到空行或缩进减少）
        elif current_func and stripped and (len(line) - len(line.lstrip())) <= func_indent:
            if not stripped.startswith('#'):  # 不是注释
                func_length = i - func_start
                func_lengths.append((current_func, func_length))
                current_func = None
    
    # 添加最后一个函数
    if current_func:
        func_length = len(lines) - func_start
        func_lengths.append((current_func, func_length))
    
    # 按长度排序
    func_lengths.sort(key=lambda x: x[1], reverse=True)
    
    print("最长的10个函数:")
    for func_name, length in func_lengths[:10]:
        print(f"  {func_name}: {length}行")
    
    print("\n最短的10个函数:")
    for func_name, length in func_lengths[-10:]:
        print(f"  {func_name}: {length}行")
    
    # 平均函数长度
    if func_lengths:
        avg_length = sum(length for _, length in func_lengths) / len(func_lengths)
        print(f"\n平均函数长度: {avg_length:.1f}行")
        print(f"函数总数: {len(func_lengths)}")
    
    return {
        'classes': classes,
        'functions': functions,
        'imports': imports,
        'constants': constants,
        'func_lengths': func_lengths
    }

if __name__ == "__main__":
    analysis = analyze_lexer_structure()
    
    # 基于分析结果建议模块划分
    print("\n" + "=" * 80)
    print("模块划分建议:")
    print("=" * 80)
    
    # 根据函数名分组
    func_groups = {
        'tokenize': [],
        'match': [],
        'pattern': [],
        'error': [],
        'util': [],
        'init': [],
        'other': []
    }
    
    for line_num, func_name, params, return_type in analysis['functions']:
        func_lower = func_name.lower()
        
        if 'tokenize' in func_lower:
            func_groups['tokenize'].append(func_name)
        elif 'match' in func_lower:
            func_groups['match'].append(func_name)
        elif 'pattern' in func_lower:
            func_groups['pattern'].append(func_name)
        elif 'error' in func_lower or 'handle' in func_lower or 'warn' in func_lower:
            func_groups['error'].append(func_name)
        elif 'init' in func_lower or 'setup' in func_lower:
            func_groups['init'].append(func_name)
        elif 'util' in func_lower or 'helper' in func_lower or 'get_' in func_lower or 'set_' in func_lower:
            func_groups['util'].append(func_name)
        else:
            func_groups['other'].append(func_name)
    
    print("建议的模块划分:")
    print(f"  1. tokenizer模块: {len(func_groups['tokenize'])}个函数")
    print(f"  2. matcher模块: {len(func_groups['match'])}个函数")
    print(f"  3. pattern模块: {len(func_groups['pattern'])}个函数")
    print(f"  4. error模块: {len(func_groups['error'])}个函数")
    print(f"  5. util模块: {len(func_groups['util'])}个函数")
    print(f"  6. 其他函数: {len(func_groups['other'])}个")
    
    # 显示每个组的示例函数
    for group, funcs in func_groups.items():
        if funcs:
            print(f"\n  {group}模块示例函数:")
            for func in funcs[:5]:
                print(f"    - {func}")
            if len(funcs) > 5:
                print(f"    ... 还有{len(funcs)-5}个函数")