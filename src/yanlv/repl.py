#!/usr/bin/env python3
"""
言律语言交互式环境 (REPL)

提供命令行交互式编程体验
"""

import sys
import os
import readline
from typing import Optional, List

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from yanlv.lexer import create_lexer, TokenType
from yanlv.semantic import SemanticContextTracker, TypeInferenceSystem, AmbiguityResolver
from yanlv.feedback import FeedbackCollector


class YanLvREPL:
    """言律语言交互式环境"""

    def __init__(self):
        """初始化REPL"""
        self.lexer = create_lexer("jieba")
        self.tracker = SemanticContextTracker()
        self.inference = TypeInferenceSystem(self.tracker)
        self.resolver = AmbiguityResolver(self.tracker, self.inference)
        self.collector = FeedbackCollector()

        self.history: List[str] = []
        self.variables = {}
        self.running = True

        # 设置历史记录
        self.history_file = os.path.expanduser("~/.yanlv_history")
        self._setup_readline()

    def _setup_readline(self):
        """设置readline"""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass

    def _save_history(self):
        """保存历史记录"""
        try:
            readline.write_history_file(self.history_file)
        except:
            pass

    def show_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*60)
        print("  言律语言交互式环境 v2.0.0")
        print("  一个现代化的中文编程语言")
        print("="*60)
        print("\n输入 '帮助' 查看可用命令")
        print("输入 '退出' 或 'exit' 退出程序\n")

    def show_help(self):
        """显示帮助信息"""
        print("\n" + "="*60)
        print("  可用命令")
        print("="*60)
        print("\n基本命令:")
        print("  帮助          - 显示帮助信息")
        print("  退出/exit     - 退出交互环境")
        print("  清空/clear    - 清空屏幕")
        print("  历史/history  - 显示命令历史")
        print("  统计/stats    - 显示性能统计")
        print("  变量/vars     - 显示所有变量")
        print("  重置/reset    - 重置环境")

        print("\n编程示例:")
        print("  如果 条件 成立 则 输出 'Hello'")
        print("  定义 变量 x 为 10")
        print("  循环 5 次 执行 输出 '测试'")
        print("  函数 加法 参数 a b 返回 a + b")

        print("\n特殊命令:")
        print("  分析 <代码>   - 分析代码结构")
        print("  测试 <代码>   - 测试代码执行")
        print("  反馈 <内容>   - 提交用户反馈")
        print()

    def clear_screen(self):
        """清空屏幕"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_history(self):
        """显示历史记录"""
        print("\n命令历史:")
        for i, cmd in enumerate(self.history[-20:], 1):
            print(f"  {i}. {cmd}")
        print()

    def show_stats(self):
        """显示统计信息"""
        stats = self.lexer.get_performance_stats()
        print("\n性能统计:")
        print(f"  处理的词元数: {stats.get('tokens_processed', 0)}")
        print(f"  历史命令数: {len(self.history)}")
        print(f"  定义的变量数: {len(self.variables)}")

        feedback_stats = self.collector.get_statistics()
        print(f"  收集的反馈数: {feedback_stats.get('total_feedbacks', 0)}")
        print()

    def show_variables(self):
        """显示所有变量"""
        if not self.variables:
            print("\n当前没有定义变量")
        else:
            print("\n已定义的变量:")
            for name, value in self.variables.items():
                print(f"  {name} = {value}")
        print()

    def reset_environment(self):
        """重置环境"""
        self.lexer = create_lexer("jieba")
        self.tracker = SemanticContextTracker()
        self.inference = TypeInferenceSystem(self.tracker)
        self.resolver = AmbiguityResolver(self.tracker, self.inference)
        self.collector = FeedbackCollector()
        self.variables = {}
        print("\n环境已重置\n")

    def analyze_code(self, code: str):
        """分析代码"""
        print("\n代码分析:")
        print(f"  源代码: {code}")

        tokens = self.lexer.tokenize(code)
        print(f"  词元数量: {len(tokens)}")

        print("\n  词元列表:")
        for i, token in enumerate(tokens[:20], 1):  # 只显示前20个
            print(f"    {i}. {token.type.name}: '{token.value}'")

        if len(tokens) > 20:
            print(f"    ... 还有 {len(tokens) - 20} 个词元")

        print()

    def test_code(self, code: str):
        """测试代码"""
        print("\n测试执行:")
        tokens = self.lexer.tokenize(code)

        # 简单的解释执行
        for token in tokens:
            if token.type == TokenType.OUTPUT:
                print("  [输出]", end=" ")
            elif token.type == TokenType.STRING:
                print(f"{token.value}")
            elif token.type == TokenType.NUMBER:
                print(f"  [数字] {token.value}")

        print()

    def submit_feedback(self, content: str):
        """提交反馈"""
        parts = content.split(maxsplit=2)
        if len(parts) >= 3:
            segment = parts[0]
            system = parts[1]
            user = parts[2]

            feedback_id = self.collector.collect_ambiguity_feedback(
                source_text=content,
                ambiguous_segment=segment,
                system_interpretation=system,
                user_correction=user,
                context=[],
                confidence=0.8
            )
            print(f"\n反馈已提交，ID: {feedback_id}\n")
        else:
            print("\n用法: 反馈 <片段> <系统解释> <用户修正>")
            print("示例: 反馈 测试 名词 动词\n")

    def process_command(self, command: str) -> bool:
        """处理命令"""
        command = command.strip()

        if not command:
            return True

        # 保存到历史
        self.history.append(command)

        # 处理特殊命令
        if command in ['退出', 'exit', 'quit']:
            self._save_history()
            print("\n再见！\n")
            return False

        elif command in ['帮助', 'help']:
            self.show_help()

        elif command in ['清空', 'clear', 'cls']:
            self.clear_screen()

        elif command in ['历史', 'history']:
            self.show_history()

        elif command in ['统计', 'stats']:
            self.show_stats()

        elif command in ['变量', 'vars']:
            self.show_variables()

        elif command in ['重置', 'reset']:
            self.reset_environment()

        elif command.startswith('分析 '):
            code = command[3:].strip()
            self.analyze_code(code)

        elif command.startswith('测试 '):
            code = command[3:].strip()
            self.test_code(code)

        elif command.startswith('反馈 '):
            content = command[3:].strip()
            self.submit_feedback(content)

        else:
            # 执行代码
            self.execute_code(command)

        return True

    def execute_code(self, code: str):
        """执行代码"""
        try:
            tokens = self.lexer.tokenize(code)

            # 简单的解释器
            i = 0
            while i < len(tokens):
                token = tokens[i]

                # 处理输出语句
                if token.type == TokenType.OUTPUT:
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.STRING:
                        print(f"=> {tokens[i].value}")
                    elif i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                        var_name = tokens[i].value
                        if var_name in self.variables:
                            print(f"=> {self.variables[var_name]}")
                        else:
                            print(f"=> 变量 '{var_name}' 未定义")

                # 处理变量定义
                elif token.type == TokenType.DEFINE:
                    i += 1
                    if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                        var_name = tokens[i].value
                        i += 2  # 跳过 '为'
                        if i < len(tokens):
                            if tokens[i].type == TokenType.NUMBER:
                                self.variables[var_name] = float(tokens[i].value)
                            elif tokens[i].type == TokenType.STRING:
                                self.variables[var_name] = tokens[i].value
                            else:
                                self.variables[var_name] = tokens[i].value
                            print(f"=> 定义变量 {var_name} = {self.variables[var_name]}")

                # 处理如果语句
                elif token.type == TokenType.IF:
                    print("=> [条件语句]")

                # 处理循环语句
                elif token.type == TokenType.LOOP:
                    print("=> [循环语句]")

                # 处理函数定义
                elif token.type == TokenType.FUNCTION:
                    print("=> [函数定义]")

                i += 1

        except Exception as e:
            print(f"错误: {e}")

    def run(self):
        """运行REPL"""
        self.show_welcome()

        while self.running:
            try:
                # 读取输入
                command = input("言律> ").strip()

                # 处理命令
                self.running = self.process_command(command)

            except KeyboardInterrupt:
                print("\n\n使用 '退出' 命令退出程序")
            except EOFError:
                print("\n再见！\n")
                break
            except Exception as e:
                print(f"错误: {e}")

        self._save_history()


def main():
    """主函数"""
    repl = YanLvREPL()
    repl.run()


if __name__ == "__main__":
    main()
