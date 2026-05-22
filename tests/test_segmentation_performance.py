"""
分词性能测试

比较jieba和THULAC的性能
"""

import time
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from yanlv.lexer.lexer import YanLuLexer
import jieba
import thulac


class SegmentationPerformanceTest:
    """分词性能测试类"""
    
    def __init__(self):
        """初始化测试"""
        self.test_texts = [
            # 短文本
            "温度升高，风扇开启。",
            "如果温度超过30度，就开启空调。",
            "张三、李四和王五，发送消息。",
            
            # 中等长度文本
            "在智能家居系统中，温度传感器检测到高温后，自动开启空调制冷模式，同时风扇也开始工作以加速空气流通。",
            "用户通过手机应用程序远程控制家中的智能设备，包括灯光、窗帘、空调和安防系统，实现智能化的生活体验。",
            
            # 长文本
            "言律语言是一种基于认知科学的中文原生编程语言，它采用元数驱动解析和上下文感知的语义分析技术。该语言支持自然的中文语法结构，包括因果链语法、上下文省略、状态流和多轨设计等特性。开发者可以使用言律语言编写更加直观和易于理解的中文代码，提高开发效率和代码可读性。",
            "在智能家居控制场景中，言律语言可以用于编写设备控制逻辑。例如，当温度传感器检测到室内温度超过设定阈值时，系统会自动开启空调并调整到合适的温度；当光线传感器检测到光线不足时，系统会自动打开灯光；当用户离开家时，系统会自动关闭所有不必要的电器设备以节省能源。",
            
            # 复杂文本
            "张三、李四和王五三个用户分别设置了不同的温度偏好：张三喜欢25度，李四喜欢26度，王五喜欢24度。系统需要根据当前用户自动调整空调温度，同时考虑节能模式和舒适度的平衡。如果多个用户同时在家，系统需要计算平均温度或根据优先级进行调节。",
        ]
        
        # 初始化分词器
        self.jieba_lexer = YanLuLexer()
        self.thulac_seg = thulac.thulac(seg_only=True)  # 只分词模式
    
    def test_jieba_performance(self):
        """测试jieba分词性能"""
        print("测试jieba分词性能...")
        
        total_time = 0
        total_tokens = 0
        
        for text in self.test_texts:
            start_time = time.time()
            
            # 使用jieba分词
            words = jieba.lcut(text)
            
            # 词法分析
            tokens = list(self.jieba_lexer.tokenize(text))
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            total_time += elapsed
            total_tokens += len(tokens)
            
            print(f"  文本长度: {len(text)}字符, 分词时间: {elapsed:.6f}秒, 词数: {len(words)}, 词元数: {len(tokens)}")
        
        avg_time = total_time / len(self.test_texts)
        avg_tokens = total_tokens / len(self.test_texts)
        
        print(f"jieba平均分词时间: {avg_time:.6f}秒/文本")
        print(f"jieba平均词元数: {avg_tokens:.2f}词元/文本")
        print()
        
        return avg_time, avg_tokens
    
    def test_thulac_performance(self):
        """测试THULAC分词性能"""
        print("测试THULAC分词性能...")
        
        total_time = 0
        total_tokens = 0
        
        for text in self.test_texts:
            start_time = time.time()
            
            # 使用THULAC分词
            words = self.thulac_seg.cut(text, text=True)
            word_list = words.split()
            
            # 词法分析（使用jieba的词法分析器，但分词用THULAC）
            # 这里我们只测试分词性能，不测试完整的词法分析
            end_time = time.time()
            elapsed = end_time - start_time
            
            total_time += elapsed
            total_tokens += len(word_list)
            
            print(f"  文本长度: {len(text)}字符, 分词时间: {elapsed:.6f}秒, 词数: {len(word_list)}")
        
        avg_time = total_time / len(self.test_texts)
        avg_tokens = total_tokens / len(self.test_texts)
        
        print(f"THULAC平均分词时间: {avg_time:.6f}秒/文本")
        print(f"THULAC平均词数: {avg_tokens:.2f}词/文本")
        print()
        
        return avg_time, avg_tokens
    
    def test_accuracy_comparison(self):
        """测试分词准确性比较"""
        print("测试分词准确性比较...")
        
        test_cases = [
            ("温度升高，风扇开启。", ["温度", "升高", "，", "风扇", "开启", "。"]),
            ("如果温度超过30度，就开启空调。", ["如果", "温度", "超过", "30", "度", "，", "就", "开启", "空调", "。"]),
            ("张三、李四和王五，发送消息。", ["张三", "、", "李四", "和", "王五", "，", "发送", "消息", "。"]),
        ]
        
        print("jieba分词结果:")
        for text, expected in test_cases:
            jieba_result = list(jieba.cut(text))
            print(f"  原文: {text}")
            print(f"  jieba: {jieba_result}")
            print(f"  期望: {expected}")
            print(f"  匹配度: {self._calculate_match_rate(jieba_result, expected):.2%}")
            print()
        
        print("THULAC分词结果:")
        for text, expected in test_cases:
            thulac_result = self.thulac_seg.cut(text, text=True).split()
            print(f"  原文: {text}")
            print(f"  THULAC: {thulac_result}")
            print(f"  期望: {expected}")
            print(f"  匹配度: {self._calculate_match_rate(thulac_result, expected):.2%}")
            print()
    
    def _calculate_match_rate(self, result, expected):
        """计算分词匹配率"""
        # 简单的匹配率计算：相同位置相同词的比例
        matches = 0
        min_len = min(len(result), len(expected))
        
        for i in range(min_len):
            if result[i] == expected[i]:
                matches += 1
        
        return matches / len(expected) if expected else 0
    
    def test_memory_usage(self):
        """测试内存使用"""
        import psutil
        import os
        
        print("测试内存使用...")
        
        # 测试jieba内存使用
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # 初始化jieba分词器
        jieba_lexer = YanLuLexer()
        
        mem_after_jieba = process.memory_info().rss / 1024 / 1024
        jieba_mem_usage = mem_after_jieba - mem_before
        
        # 初始化THULAC分词器
        thulac_seg = thulac.thulac(seg_only=True)
        
        mem_after_thulac = process.memory_info().rss / 1024 / 1024
        thulac_mem_usage = mem_after_thulac - mem_after_jieba
        
        print(f"jieba内存使用: {jieba_mem_usage:.2f} MB")
        print(f"THULAC内存使用: {thulac_mem_usage:.2f} MB")
        print()
        
        return jieba_mem_usage, thulac_mem_usage
    
    def test_batch_processing(self):
        """测试批量处理性能"""
        print("测试批量处理性能...")
        
        # 生成大量测试数据
        batch_size = 1000
        test_text = "温度升高，风扇开启。如果温度超过30度，就开启空调。"
        
        print(f"批量处理 {batch_size} 个文本...")
        
        # jieba批量处理
        start_time = time.time()
        for _ in range(batch_size):
            list(jieba.cut(test_text))
        jieba_batch_time = time.time() - start_time
        
        # THULAC批量处理
        start_time = time.time()
        for _ in range(batch_size):
            self.thulac_seg.cut(test_text, text=True)
        thulac_batch_time = time.time() - start_time
        
        print(f"jieba批量处理时间: {jieba_batch_time:.3f}秒 ({batch_size/jieba_batch_time:.1f} 文本/秒)")
        print(f"THULAC批量处理时间: {thulac_batch_time:.3f}秒 ({batch_size/thulac_batch_time:.1f} 文本/秒)")
        print()
        
        return jieba_batch_time, thulac_batch_time
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("分词性能测试")
        print("=" * 60)
        
        results = {}
        
        # 运行性能测试
        print("\n1. 单文本分词性能测试:")
        print("-" * 40)
        jieba_time, jieba_tokens = self.test_jieba_performance()
        thulac_time, thulac_tokens = self.test_thulac_performance()
        
        results["jieba_single_time"] = jieba_time
        results["thulac_single_time"] = thulac_time
        results["speedup"] = jieba_time / thulac_time if thulac_time > 0 else 0
        
        # 运行准确性测试
        print("\n2. 分词准确性测试:")
        print("-" * 40)
        self.test_accuracy_comparison()
        
        # 运行内存测试
        print("\n3. 内存使用测试:")
        print("-" * 40)
        try:
            jieba_mem, thulac_mem = self.test_memory_usage()
            results["jieba_memory"] = jieba_mem
            results["thulac_memory"] = thulac_mem
            results["memory_ratio"] = thulac_mem / jieba_mem if jieba_mem > 0 else 0
        except ImportError:
            print("  需要安装psutil库进行内存测试")
            print("  安装命令: pip install psutil")
        
        # 运行批量处理测试
        print("\n4. 批量处理性能测试:")
        print("-" * 40)
        jieba_batch, thulac_batch = self.test_batch_processing()
        results["jieba_batch_time"] = jieba_batch
        results["thulac_batch_time"] = thulac_batch
        results["batch_speedup"] = jieba_batch / thulac_batch if thulac_batch > 0 else 0
        
        # 输出总结
        print("\n5. 性能测试总结:")
        print("-" * 40)
        print(f"单文本分词速度提升: {results['speedup']:.2f}x")
        print(f"   - jieba: {results['jieba_single_time']:.6f}秒/文本")
        print(f"   - THULAC: {results['thulac_single_time']:.6f}秒/文本")
        
        if "memory_ratio" in results:
            print(f"内存使用比例: {results['memory_ratio']:.2f}x")
            print(f"   - jieba: {results['jieba_memory']:.2f} MB")
            print(f"   - THULAC: {results['thulac_memory']:.2f} MB")
        
        print(f"批量处理速度提升: {results['batch_speedup']:.2f}x")
        print(f"   - jieba: {results['jieba_batch_time']:.3f}秒 ({1000/results['jieba_batch_time']:.1f} 文本/秒)")
        print(f"   - THULAC: {results['thulac_batch_time']:.3f}秒 ({1000/results['thulac_batch_time']:.1f} 文本/秒)")
        
        # 给出建议
        print("\n6. 优化建议:")
        print("-" * 40)
        if results["speedup"] > 1.5:
            print("THULAC在单文本分词速度上明显优于jieba")
        elif results["speedup"] > 1.1:
            print("THULAC在单文本分词速度上略有优势")
        else:
            print("THULAC在单文本分词速度上没有明显优势")
        
        if "memory_ratio" in results:
            if results["memory_ratio"] < 0.8:
                print("THULAC在内存使用上更高效")
            elif results["memory_ratio"] < 1.2:
                print("THULAC和jieba在内存使用上相当")
            else:
                print("THULAC在内存使用上不如jieba高效")
        
        if results["batch_speedup"] > 1.5:
            print("THULAC在批量处理速度上明显优于jieba")
        elif results["batch_speedup"] > 1.1:
            print("THULAC在批量处理速度上略有优势")
        else:
            print("THULAC在批量处理速度上没有明显优势")
        
        print("\n" + "=" * 60)
        
        return results


def main():
    """主函数"""
    print("分词性能测试开始...")
    print("=" * 60)
    
    try:
        # 检查THULAC是否可用
        import thulac
        print("THULAC已安装")
    except ImportError:
        print("THULAC未安装，请先安装: pip install thulac")
        return
    
    try:
        # 运行测试
        tester = SegmentationPerformanceTest()
        results = tester.run_all_tests()
        
        # 根据测试结果决定是否切换到THULAC
        if results["speedup"] > 1.2 and results["batch_speedup"] > 1.2:
            print("\n建议：切换到THULAC分词器以获得更好的性能")
            print("实现步骤：")
            print("  1. 修改lexer.py中的分词逻辑")
            print("  2. 添加THULAC分词器选项")
            print("  3. 更新相关测试")
        else:
            print("\n建议：保持使用jieba分词器")
            print("原因：THULAC性能提升不明显")
            
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()