"""
创建正确的动词分类词典文件
"""

def create_correct_file():
    """创建正确的verb_categories_final.py文件"""
    print("创建正确的verb_categories_final.py文件...")
    
    # 读取原始文件
    with open('src/yanlv/lexer/verb_categories_final.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到VERB_CATEGORIES字典的结束位置
    start_idx = content.find('VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {')
    if start_idx == -1:
        print("错误: 未找到VERB_CATEGORIES字典")
        return False
    
    # 找到字典的结束位置
    brace_count = 0
    in_dict = False
    dict_end_idx = -1
    
    for i, char in enumerate(content[start_idx:]):
        if char == '{':
            brace_count += 1
            in_dict = True
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and in_dict:
                dict_end_idx = start_idx + i
                break
    
    if dict_end_idx == -1:
        print("错误: 未找到VERB_CATEGORIES字典的结束位置")
        return False
    
   ాలు# 提取VERB_CATEGORIES字典内容（到TRANSFORMATION类别结束）
    # 查找"TRANSFORMATION"类别的结束
    transformation_end = content.find('        "examples": [\n            "转换格式。",\n            "翻译文本。",\n            "解析数据。"\n        ]\n    }')
    if transformation_end == -1:
        print("错误: 未找到TRANSFORMATION类别的结束")
        return False
    
    # 找到TRANSFORMATION类别的完整结束（包括逗号）
    transformation_full_end = content.find('\n    },', transformation_end)
    if transformation_full_end == -1:
        # 如果没有逗号，可能是最后一个元素
        transformation_full_end = content.find('\n}', transformation_end)
    
    if transformation_full_end == -1:
        print("错误: 未找到TRANSFORMATION类别的完整结束")
        return False
    
    # 计算TRANSFORMATION类别结束的位置
    trans_end_pos = transformation_full_end + len('\n    },')
    
    # 构建正确的文件内容
    header = """言律语言动词分类词典

扩展的动词分类词典，包含13个类别，119个动词
每个类别包含语义角色标注
"""

    imports = """from typing import Dict, List, Tuple, Any
from enum import Enum


class SemanticRole(Enum):
    \"\"\"语义角色枚举\"\"\"
    CHANGE_OF_STATE = "CHANGE_OF_STATE"          # 状态变化
    VALUE_ASSIGNMENT = "VALUE_ASSIGNMENT"        # 值赋值
    DATA_OUTPUT = "DATA_OUTPUT"                  # 数据输出
    DEVICE_CONTROL = "DEVICE_CONTROL"            # 设备控制
    DATA_PROCESSING = "DATA_PROCESSING"          # 数据处理
    SPATIAL_MOVEMENT = "SPATIAL_MOVEMENT"        # 空间移动
    OBJECT_CREATION = "OBJECT_CREATION"          # 对象创建
    OBJECT_DESTRUCTION = "OBJECT_DESTRUCTION"    # 对象销毁
    DATA_RETRIEVAL = "DATA_RETRIEVAL"            # 数据检索
    DATA_MODIFICATION = "DATA_MODIFICATION"      # 数据修改
    COMMUNICATION = "COMMUNICATION"              # 通信
    COMPARISON = "COMPARISON"                    # 比较
    TRANSFORMATION = "TRANSFORMATION"            # 转换


class VerbCategory(Enum):
    \"\"\"动词类别枚举\"\"\"
    STATE_TRANSITION = "STATE_TRANSITION"        # 状态转换
    ASSIGNMENT = "ASSాలుMENT"                    # 赋值
    OUTPUT = "OUTPUT"                            # 输出
    CONTROL = "CONTROL"ాలు                          # 控制
   ాలుCOMPUTాలుTION = "COMPUTATION"                  # 计算
    MOVEMENT = "MOVEMENT"                        # 移动
    CREATION = "CREATION"                        # 创建
    DESTRUCTION = "DESTRUCTION"                  # 销毁
    QUERY = "QUERY"                              # 查询
    MODIFICATION = "MODIFICATION"                # 修改
    COMMUNICATION = "COMMUNICATION"              # 通信
    COMPARISON = "COMPARISON"                    # 比较
    TRANSFORMATION = "TRANSFORMATION"            # 转换


# 扩展的动词分类词典 (13个类别，119个动词)
VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {"""
    
    # 提取VERB_CATEGORIES字典内容（到TRANSFORMATION结束）
    verb_categories_content = content[start_idx:trans_end_pos]
    
    # 确保以}结束
    if not verb_categories_content.strip().endswith('}'):
        verb_categories_content = verb_categories_content.rstrip() + '\n}'
    
    # 添加VERB_ARITY部分
    verb_arity_start = content.find('VERB_ARITY: Dict[str, int] = {')
    if verb_arity_start == -1:
        print("错误: 未找到VERB_ARITY字典")
        return False
    
    verb_arity_content = content[verb_arity_start:]
    
    # 构建完整内容
    full_content = header + '\n' + imports + '\n' + verb_categories_content + '\n\n' + verb_arity_content
    
    # 写入新文件
    with open('src/yanlv/lexer/verb_categories_final_correct.py', 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print("已创建正确的文件: verb_categories_final_correct.py")
    
    # 验证新文件
    print("\n验证新文件...")
    try:
        import ast
        ast.parse(full_content)
        print("语法检查通过")
        
        # 检查结构
        lines = full_content.split('\n')
        verb_categories_found = False
        verb_arity_found = False
        
        for line in lines:
            if 'VERB_CATEGORIES:' in line:
                verb_categories_found = True
            if 'VERB_ARITY:' in line:
                verb_arity_found = True
        
        if verb_categories_found and verb_arity_found:
            print("结构检查通过")
            return True
        else:
            print(f"结构检查失败: VERB_CATEGORIES={verb_categories_found}, VERB_ARITY={verb_arity_found}")
            return False
            
    except SyntaxError as e:
        print(f"语法错误: {e}")
        return False
    except Exception as e:
        print(f"验证错误: {e}")
        return False

if __name__ == "__main__":
    if create_correct_file():
        print("\n创建成功!")
    else:
        print("\n创建失败!")