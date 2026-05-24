#!/usr/bin/env python3
"""
言律语言 Playground 后端服务

提供Web API接口
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
import time

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from yanlv.lexer import create_lexer, TokenType
from yanlv.semantic import SemanticContextTracker, TypeInferenceSystem, AmbiguityResolver
from yanlv.feedback import FeedbackCollector

app = Flask(__name__)
CORS(app)

# 全局实例
lexer = create_lexer("jieba")
tracker = SemanticContextTracker()
inference = TypeInferenceSystem(tracker)
resolver = AmbiguityResolver(tracker, inference)
collector = FeedbackCollector()


@app.route('/')
def index():
    """首页"""
    # 返回 HTML 页面
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(os.path.dirname(__file__), 'index.html')
    else:
        # 如果没有 HTML 文件，返回 API 信息
        return jsonify({
            'name': '言律语言 Playground',
            'version': '2.0.0',
            'description': '中文编程语言在线体验平台',
            'endpoints': {
                'run': '/api/run',
                'analyze': '/api/analyze',
                'feedback': '/api/feedback',
                'stats': '/api/stats',
                'examples': '/api/examples'
            },
            'status': 'running'
        })


@app.route('/api/run', methods=['POST'])
def run_code():
    """运行代码"""
    try:
        data = request.json
        code = data.get('code', '')

        if not code.strip():
            return jsonify({
                'success': False,
                'error': '请输入代码'
            })

        # 记录开始时间
        start_time = time.time()

        # 词法分析
        tokens = lexer.tokenize(code)

        # 执行代码
        output = []
        variables = {}

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # 处理输出语句
            if token.type == TokenType.OUTPUT:
                i += 1
                if i < len(tokens):
                    if tokens[i].type == TokenType.STRING:
                        output.append(f"=> {tokens[i].value}")
                    elif tokens[i].type == TokenType.IDENTIFIER:
                        var_name = tokens[i].value
                        if var_name in variables:
                            output.append(f"=> {variables[var_name]}")
                        else:
                            output.append(f"=> 变量 '{var_name}' 未定义")

            # 处理变量定义
            elif token.type == TokenType.DEFINE:
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                    var_name = tokens[i].value
                    i += 2  # 跳过 '为'
                    if i < len(tokens):
                        if tokens[i].type == TokenType.NUMBER:
                            variables[var_name] = float(tokens[i].value)
                        elif tokens[i].type == TokenType.STRING:
                            variables[var_name] = tokens[i].value
                        else:
                            variables[var_name] = tokens[i].value
                        output.append(f"=> 定义变量 {var_name} = {variables[var_name]}")

            # 处理条件语句
            elif token.type == TokenType.IF:
                output.append("=> [条件语句]")

            # 处理循环语句
            elif token.type == TokenType.LOOP:
                output.append("=> [循环语句]")

            # 处理函数定义
            elif token.type == TokenType.FUNCTION:
                output.append("=> [函数定义]")

            i += 1

        # 计算执行时间
        exec_time = round((time.time() - start_time) * 1000, 2)

        # 统计信息
        stats = {
            'tokens': len(tokens),
            'lines': len([l for l in code.split('\n') if l.strip()]),
            'exec_time': exec_time,
            'variables': len(variables)
        }

        return jsonify({
            'success': True,
            'output': '\n'.join(output) if output else '代码已分析，但没有输出语句',
            'stats': stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """分析代码"""
    try:
        data = request.json
        code = data.get('code', '')

        if not code.strip():
            return jsonify({
                'success': False,
                'error': '请输入代码'
            })

        # 词法分析
        tokens = lexer.tokenize(code)

        # 提取词元信息
        token_list = []
        for token in tokens[:100]:  # 限制返回数量
            token_list.append({
                'type': token.type.name,
                'value': token.value,
                'line': token.position.line if hasattr(token, 'position') else 0,
                'column': token.position.column if hasattr(token, 'position') else 0
            })

        return jsonify({
            'success': True,
            'tokens': token_list,
            'total_tokens': len(tokens)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交反馈"""
    try:
        data = request.json
        segment = data.get('segment', '')
        system = data.get('system', '')
        user = data.get('user', '')

        if not all([segment, system, user]):
            return jsonify({
                'success': False,
                'error': '请提供完整的反馈信息'
            })

        feedback_id = collector.collect_ambiguity_feedback(
            source_text=f"{segment} {system} {user}",
            ambiguous_segment=segment,
            system_interpretation=system,
            user_correction=user,
            context=[],
            confidence=0.8
        )

        return jsonify({
            'success': True,
            'feedback_id': feedback_id,
            'message': '反馈已提交'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        lexer_stats = lexer.get_performance_stats()
        feedback_stats = collector.get_statistics()

        return jsonify({
            'success': True,
            'lexer': lexer_stats,
            'feedback': feedback_stats
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """获取示例代码"""
    examples = [
        {
            'name': '输出语句',
            'code': "输出 'Hello, 言律语言！'\n输出 '这是一个中文编程语言'"
        },
        {
            'name': '变量定义',
            'code': "定义 变量 x 为 10\n定义 变量 y 为 20\n输出 x\n输出 y"
        },
        {
            'name': '条件语句',
            'code': "如果 条件 成立 则 输出 '条件为真'\n如果 条件 不成立 则 输出 '条件为假'"
        },
        {
            'name': '循环语句',
            'code': "循环 5 次 执行 输出 '这是循环'\n循环 3 次 执行 输出 '另一个循环'"
        },
        {
            'name': '函数定义',
            'code': "函数 加法 参数 a b 返回 a + b\n输出 '函数已定义'"
        }
    ]

    return jsonify({
        'success': True,
        'examples': examples
    })


if __name__ == '__main__':
    print("="*60)
    print("  言律语言 Playground 后端服务")
    print("  访问地址: http://localhost:5000")
    print("="*60)
    print("\nAPI端点:")
    print("  POST /api/run      - 运行代码")
    print("  POST /api/analyze  - 分析代码")
    print("  POST /api/feedback - 提交反馈")
    print("  GET  /api/stats    - 获取统计")
    print("  GET  /api/examples - 获取示例")
    print()

    app.run(debug=True, port=5000)
