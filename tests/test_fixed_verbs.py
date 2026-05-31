"""
测试修复后的动词分类词典
"""

import sys
import os

def test_verb_categories():
"""测试动词分类词典"""
print("测试修复后的动词分类词典")
print("=" * 60)

try:
# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 尝试导入修复后的文件
import importlib.util

# 首先检查原始文件
print("检查原始文件...")
try:
spec_orig = importlib.util.spec_from_file_location(
"verb_categories_final",
os.path.join(os.path.dirname(__file__), 'src', 'yanlv', 'lexer', 'verb_categories_final.py')
)
module_orig = importlib.util.module_from_spec(spec_orig)
spec_orig.loader.exec_module(module_orig)
print("原始文件导入成功")
except Exception as e:
print(f"原始文件导入失败: {e}")
return False

# 检查修复后的文件
print("\n检查修复后的文件...")
fixed_files = [
'verb_categories_final_fixed.py',
'verb_categories_final_fixed2.py',
'verb_categories_final_fixed3.py',
'verb_categories_final_corrected.py'
]

for file in fixed_files:
file_path = os.path.join(os.path.dirname(__file__), 'src', 'yanlv', 'lexer', file)
if os.path.exists(file_path):
print(f"\n检查文件: {file}")
try:
spec = importlib.util.spec_from_file_location(
f"verb_categories_{file}",
file_path
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# 检查VERB_CATEGORIES
if hasattr(module, 'VERB_CATEGORIES'):
verb_categories = module.VERB_CATEGORIES
print(f"  VERB_CATEGORIES类型: {type(verb_categories)}")
print(f"  VERB_CATEGORIES键数量: {len(verb_categories)}")

# 检查每个值是否是字典
all_dicts = True
non_dict_keys = []
for key, value in verb_categories.items():
if not isinstance(value, dict):
all_dicts = False
non_dict_keys.append((key, type(value)))

if all_dicts:
print("  所有VERB_CATEGORIES值都是字典")
else:
print(f"  VERB_CATEGORIES中有非字典值: {non_dict_keys[:5]}")  # 只显示前5个

# 检查VERB_ARITY
if hasattr(module, 'VERB_ARITY'):
verb_arity = module.VERB_ARITY
print(f"  VERB_ARITY类型: {type(verb_arity)}")
print(f"  VERB_ARITY键数量: {len(verb_arity)}")

print("  导入成功")

except Exception as e:
print(f"  导入失败: {e}")

# 现在测试一个简单的修复
print("\n" + "=" * 60)
print("创建简单的修复版本...")

# 读取原始文件
with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
content = f.read()

# 简单的修复：确保TRANSFORMATION类别后有逗号，然后结束字典
# 查找TRANSFORMATION类别的结束
trans_pattern = '"解析数据。"\n        ]\n    }'
trans_end = content.find(trans_pattern)

if trans_end != -1:
trans_end_pos = trans_end + len(trans_pattern)

# 检查后面是否有逗号
if content[trans_end_pos:trans_end_pos+1] != ',':
# 添加逗号
content = content[:trans_end_pos] + ',' + content[trans_end_pos:]
trans_end_pos += 1

# 现在查找VERB_ARITY开始
arity_start = content.find('VERB_ARITY: Dict[str, int] = {')

if arity_start != -1:
# 构建修复后的内容
# 第一部分：到TRANSFORMATION结束
part1 = content[:trans_end_pos]

# 确保VERB_CATEGORIES字典正确结束
if not part1.strip().endswith('}'):
# 查找最后一个大括号
last_brace = part1.rfind('}')
if last_brace != -1:
# 在最后一个大括号后添加字典结束
part1 = part1[:last_brace+1]

# 第二部分：VERB_ARITY及之后的内容
part2 = content[arity_start:]

# 合并
fixed_content = part1 + '\n\n\n' + part2

# 写入修复后的文件
with open('src/yanlv/lexer/verb_categories_final_simple_fix.py', 'w', encoding='utf-8') as f:
f.write(fixed_content)

print("已创建简单修复版本: verb_categories_final_simple_fix.py")

# 测试简单修复版本
print("\n测试简单修复版本...")
try:
spec = importlib.util.spec_from_file_location(
"verb_categories_final_simple_fix",
"src/yanlv/lexer/verb_categories_final_simple_fix.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# 检查VERB_CATEGORIES
if hasattr(module, 'VERB_CATEGORIES'):
verb_categories = module.VERB_CATEGORIES
print(f"VERB_CATEGORIES键数量: {len(verb_categories)}")

# 检查是否是字典
is_dict = isinstance(verb_categories, dict)
print(f"VERB_CATEGORIES是字典: {is_dict}")

if is_dict:
# 检查前几个键
keys = list(verb_categories.keys())[:5]
print(f"前5个键: {keys}")

# 检查值类型
valid_count = 0
total_count = 0
for key, value in verb_categories.items():
total_count += 1
if isinstance(value, dict):
valid_count += 1
else:
print(f"  非字典值: {key} = {type(value)}")
if total_count > 10:  # 只显示前10个错误
break

print(f"有效字典值: {valid_count}/{total_count}")

# 检查VERB_ARITY
if hasattr(module, 'VERB_ARITY'):
verb_arity = module.VERB_ARITY
print(f"VERB_ARITY键数量: {len(verb_arity)}")
print(f"VERB_ARITY是字典: {isinstance(verb_arity, dict)}")

print("简单修复版本测试通过!")
return True

except Exception as e:
print(f"简单修复版本测试失败: {e}")
import traceback
traceback.print_exc()
return False
else:
print("错误: 未找到VERB_ARITY字典")
return False
else:
print("错误: 未找到TRANSFORMATION类别")
return False

except Exception as e:
print(f"测试过程中出现错误: {e}")
import traceback
traceback.print_exc()
return False

if __name__ == "__main__":
success = test_verb_categories()

print("\n" + "=" * 60)
if success:
print("测试通过!")
else:
print("测试失败!")