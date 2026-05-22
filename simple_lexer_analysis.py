"""
简单分析lexer.py文件结构
"""

import os

def simple_analysis():
    """简单分析lexer.py结构"""
    lexer_path = 'src/yanlv/lexer/lexer.py'
    
    if not os.path.exists(lexer_path):
        print(f"文件不存在: {lexer_path}")
        return
    
    print("简单分析lexer.py文件结构")
    print("=" * 60)
    
    # 读取文件并统计
    with open(lexer_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"总行数: {total_lines}")
    
    # 统计各类内容
    class_count = 0
    function_count = 0
    import_count = 0
    comment_count = 0
    empty_count = 0
    
    class_names = []
    function_names = []
    import_statements = []
    
    for i, line in enumerate(lines[:1000]):  # 只分析前1000行
        stripped = line.strip()
        
        if stripped.startswith('class '):
            class_count += 1
            class_name = stripped.split('class ')[1].split('(')[0].split(':')[0]
            class_names.append((i+1, class_name))
        
        elif stripped.startswith('def '):
            function_count += 1
            func_name = stripped.split('def ')[1].split('(')[0]
            function_names.append((i+1, func_name))
        
        elif stripped.startswith('import ') or stripped.startswith('from '):
            import_count += 1
            import_statements.append((i+1, stripped))
        
        elif stripped.startswith('#'):
            comment_count += 1
        
        elif stripped == '':
            empty_count += 1
    
    print(f"\n类数量: {class_count}")
    for line_num, name in class_names:
        print(f"  第{line_num:4d}行: {name}")
    
    print(f"\n函数数量 (前20个): {function_count}")
    for line_num, name in function_names[:20]:
        print(f"  第{line_num:4d}行: {name}")
    
    print(f"\n导入语句数量: {import_count}")
    for line_num, stmt in import_statements:
        print(f"  第{line_num:4d}行: {stmt[:80]}...")
    
    # 分析函数分组
    print(f"\n函数分组分析:")
    
    tokenize_funcs = [name for _, name in function_names if 'tokenize' in name.lower()]
    match_funcs = [name for _, name in function_names if 'match' in name.lower()]
    pattern_funcs = [name for _, name in function_names if 'pattern' in name.lower()]
    error_funcs = [name for _, name in function_names if any(x in name.lower() for x in ['error', 'handle', 'warn', 'exception'])]
    init_funcs = [name for _, name in function_names if any(x in name.lower() for x in ['init', 'setup', 'config'])]
    util_funcs = [name for _, name in function_names if any(x in name.lower() for x in ['util', 'helper', 'get_', 'set_', 'is_', 'has_'])]
    
    print(f"  tokenize相关函数: {len(tokenize_funcs)}个")
    print(f"  match相关函数: {len(match_funcs)}个")
    print(f"  pattern相关函数: {len(pattern_funcs)}个")
    print(f"  error相关函数: {len(error_funcs)}个")
    print(f"  init相关函数: {len(init_funcs)}个")
    print(f"  util相关函数: {len(util_funcs)}个")
    
    # 建议模块划分
    print(f"\n模块划分建议:")
    print(f"  1. base.py - 基础类和主类 (1个类)")
    print(f"  2. tokenizer.py - 分词器相关 ({len(tokenize_funcs)}个函数)")
    print(f"  3. matcher.py - 词元匹配 ({len(match_funcs)}个函数)")
    print(f"  4. patterns.py - 模式管理 ({len(pattern_funcs)}个函数)")
    print(f"  5. errors.py - 错误处理 ({len(error_funcs)}个函数)")
    print(f"  6. utils.py - 工具函数 ({len(util_funcs)}个函数)")
    print(f"  7. constants.py - 常量定义")
    print(f"  8. config.py - 配置管理")
    
    # 查看文件大小
    size = os.path.getsize(lexer_path)
    print(f"\n文件大小: {size} 字节 ({size/1024:.2f} KB)")
    print(f"平均每KB代码行数: {total_lines/(size/1024):.1f} 行/KB")
    
    return {
        'total_lines': total_lines,
        'class_count': class_count,
        'function_count': function_count,
        'import_count': import_count,
        'class_names': class_names,
        'function_names': function_names[:50]
    }

if __name__ == "__main__":
    result = simple_analysis()
    
    # 基于分析创建模块化计划
    print("\n" + "=" * 60)
    print("模块化实施计划:")
    print("=" * 60)
    
    print("\n第一阶段: 创建基础结构")
    print("  1. 创建 base.py - 包含YanLuLexer基类")
    print("  2. 创建 constants.py - 常量定义")
    print("  3. 创建 __init__.py - 模块导出")
    
    print("\n第二阶段: 提取功能模块")
    print("  1. 创建 tokenizer.py - 提取分词相关函数")
    print("  2. 创建 matcher.py - 提取匹配相关函数")
    print("  3. 创建 patterns.py - 提取模式相关函数")
    print("  4. 创建 errors.py - 提取错误处理函数")
    print("  5. 创建 utils.py - 提取工具函数")
    
    print("\n第三阶段: 重构主类")
    print("  1. 将YanLuLexer拆分为多个组件")
    print("  2. 更新导入语句")
    print("  3. 确保向后兼容")
    
    print("\n第四阶段: 测试和优化")
    print("  1. 编写单元测试")
    print("  2. 性能测试")
    print("  3. 文档更新")