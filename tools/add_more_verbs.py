"""
添加更多动词到分类词典

为言律语言添加更多动词，扩展动词分类词典
"""

# 新的动词分类（按类别分组）
NEW_VERBS_BY_CATEGORY = {
    # 状态转换动词
    "STATE_TRANSITION": [
        "转变为", "演化成", "发展成", "进化为", "退化为", 
        "升级为", "降级为", "优化为", "简化为", "复杂化"
    ],
    
    # 赋值动词
    "ASSIGNMENT": [
        "赋值", "设定", "指定", "命名", "称为", 
        "叫作", "标记为", "标识为", "标注为", "记为"
    ],
    
    # 输出动词
    "OUTPUT": [
        "输出到", "写入", "保存", "导出", "转储", 
        "日志", "报告", "通报", "公布", "发布"
    ],
    
    # 控制动词
    "CONTROL": [
        "激活", "禁用", "启用", "封锁", "解锁", 
        "加载", "卸载", "安装", "卸载", "配置"
    ],
    
    # 计算动词
    "COMPUTATION": [
        "求平均", "求最大", "求最小", "求方差", "求标准差", 
        "聚合", "分组", "连接", "合并", "拆分"
    ],
    
    # 移动动词
    "MOVEMENT": [
        "平移", "缩放", "旋转", "倾斜", "翻转", 
        "滚动", "拖动", "拉动", "推动", "举起"
    ],
    
    # 创建动词
    "CREATION": [
        "发明", "设计", "开发", "编写", "绘制", 
        "建模", "模拟", "仿真", "复制", "克隆"
    ],
    
    # 销毁动词
    "DESTRUCTION": [
        "取消", "废止", "终止", "结束", "关闭", 
        "销毁", "抹除", "擦除", "清空", "重置"
    ],
    
    # 查询动词
    "QUERY": [
        "提取", "抽取", "选择", "筛选", "过滤", 
        "查找", "搜索", "浏览", "查看", "检查"
    ],
    
    # 修改动词
    "MODIFICATION": [
        "改进", "增强", "减弱", "增加", "减少", 
        "放大", "缩小", "扩展", "收缩", "变形"
    ],
    
    # 通信动词
    "COMMUNICATION": [
        "分享", "转发", "回复", "响应", "呼叫", 
        "联系", "连接", "断开", "同步", "异步"
    ],
    
    # 比较动词
    "COMPARISON": [
        "评审", "审核", "检验", "检测", "监测", 
        "观察", "监视", "跟踪", "追踪", "记录"
    ],
    
    # 转换动词
    "TRANSFORMATION": [
        "反序列化", "加密", "解密", "压缩", "解压", 
        "转换", "变换", "翻译", "转码", "转义"
    ],
    
    # 新增类别：数学运算动词
    "MATH_OPERATION": [
        "加", "减", "乘", "除", "模", 
        "幂", "开方", "对数", "指数", "正弦",
        "余弦", "正切", "反正弦", "反余弦", "反正切",
        "绝对值", "取整", "舍入", "取余", "求商"
    ],
    
    # 新增类别：逻辑运算动词
    "LOGIC_OPERATION": [
        "与", "或", "非", "且", "或者", 
        "不是", "异或", "同或", "蕴含", "等价",
        "真", "假", "成立", "不成立", "满足",
        "不满足", "符合", "不符合", "匹配", "不匹配"
    ]
}

def main():
    """主函数"""
    print("添加更多动词到分类词典")
    print("=" * 60)
    
    # 统计
    total_new_verbs = 0
    for category, verbs in NEW_VERBS_BY_CATEGORY.items():
        total_new_verbs += len(verbs)
        print(f"{category}: {len(verbs)}个新动词")
    
    print(f"\n总计: {total_new_verbs}个新动词")
    
    # 生成扩展的verb_categories.py内容
    print("\n生成扩展的动词分类词典...")
    
    # 读取现有的verb_categories.py文件
    try:
        with open('src/yanlv/lexer/verb_categories.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到VERB_CATEGORIES定义
        import re
        
        # 统计现有的动词数量
        verb_matches = re.findall(r'"verbs": \[(.*?)\]', content, re.DOTALL)
        existing_verb_count = 0
        for match in verb_matches:
            verbs = re.findall(r'"([^"]+)"', match)
            existing_verb_count += len(verbs)
        
        print(f"现有动词数量: {existing_verb_count}")
        print(f"新添加动词数量: {total_new_verbs}")
        print(f"扩展后总动词数量: {existing_verb_count + total_new_verbs}")
        
        # 创建扩展版本
        extended_content = content
        
        # 为每个现有类别添加新动词
        for category, new_verbs in NEW_VERBS_BY_CATEGORY.items():
            if category in ["MATH_OPERATION", "LOGIC_OPERATION"]:
                # 这是新类别，需要添加到文件末尾
                continue
            
            # 查找现有类别
            pattern = rf'"{category}": \{{[^}}]+"verbs": \[(.*?)\]\s*,\s*"pattern"'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # 提取现有的动词列表
                verbs_start = match.start(1)
                verbs_end = match.end(1)
                existing_verbs_str = content[verbs_start:verbs_end]
                
                # 添加新动词
                new_verbs_str = ', '.join(f'"{verb}"' for verb in new_verbs)
                updated_verbs_str = existing_verbs_str.rstrip() + ', ' + new_verbs_str
                
                # 更新内容
                extended_content = (
                    extended_content[:verbs_start] + 
                    updated_verbs_str + 
                    extended_content[verbs_end:]
                )
        
        # 添加新类别
        new_categories_section = "\n\n    # 数学运算动词 (20个)\n    \"MATH_OPERATION\": {\n        \"verbs\": [\"加\", \"减\", \"乘\", \"除\", \"模\", \"幂\", \"开方\", \"对数\", \"指数\", \"正弦\", \"余弦\", \"正切\", \"反正弦\", \"反余弦\", \"反正切\", \"绝对值\", \"取整\", \"舍入\", \"取余\", \"求商\"],\n        \"pattern\": r'^[^加]+加[^。]*[。]$',\n        \"interpretation\": \"MATH_OPERATION\",\n        \"semantic_role\": \"MATH_OPERATION\",\n        \"arity\": 2,\n        \"examples\": [\n            \"计算加法。\",\n            \"求平方根。\",\n            \"计算三角函数。\"\n        ]\n    },\n\n    # 逻辑运算动词 (20个)\n    \"LOGIC_OPERATION\": {\n        \"verbs\": [\"与\", \"或\", \"非\", \"且\", \"或者\", \"不是\", \"异或\", \"同或\", \"蕴含\", \"等价\", \"真\", \"假\", \"成立\", \"不成立\", \"满足\", \"不满足\", \"符合\", \"不符合\", \"匹配\", \"不匹配\"],\n        \"pattern\": r'^[^与]+与[^。]*[。]$',\n        \"interpretation\": \"LOGIC_OPERATION\",\n        \"semantic_role\": \"LOGIC_OPERATION\",\n        \"arity\": 2,\n        \"examples\": [\n            \"逻辑与运算。\",\n            \"判断条件。\",\n            \"验证逻辑。\"\n        ]\n    },"
        
        # 插入新类别到VERB_CATEGORIES字典的末尾（在最后一个类别之前）
        last_category_pos = extended_content.rfind('    }')
        if last_category_pos != -1:
            # 在最后一个}之前插入新类别
            insert_pos = extended_content.rfind('    }', 0, last_category_pos)
            if insert_pos != -1:
                extended_content = (
                    extended_content[:insert_pos] + 
                    new_categories_section + 
                    extended_content[insert_pos:]
                )
        
        # 写入扩展文件
        with open('src/yanlv/lexer/verb_categories_extended.py', 'w', encoding='utf-8') as f:
            f.write(extended_content)
        
        print(f"\n已生成扩展的动词分类词典: src/yanlv/lexer/verb_categories_extended.py")
        
        # 也更新VERB_ARITY表
        print("\n更新动词元数表...")
        
        # 提取现有的VERB_ARITY
        start_idx = content.find('VERB_ARITY: Dict[str, int] = {')
        if start_idx != -1:
            # 找到定义的结束位置
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
            
            if brace_count == 0:
                # 生成新的VERB_ARITY条目
                new_arity_entries = []
                for category, verbs in NEW_VERBS_BY_CATEGORY.items():
                    for verb in verbs:
                        # 根据动词类型确定元数
                        if category in ["STATE_TRANSITION", "ASSIGNMENT", "MODIFICATION", "COMMUNICATION", "COMPARISON", "TRANSFORMATION"]:
                            arity = 2
                        elif category in ["OUTPUT", "CONTROL", "MOVEMENT", "CREATION", "DESTRUCTION", "QUERY"]:
                            arity = 1
                        elif category in ["COMPUTATION"]:
                            arity = -1  # 可变参数
                        elif category in ["MATH_OPERATION"]:
                            arity = 2  # 大多数数学运算是二元运算
                        elif category in ["LOGIC_OPERATION"]:
                            arity = 2  # 大多数逻辑运算是二元运算
                        else:
                            arity = 1  # 默认
                        
                        new_arity_entries.append(f"    '{verb}': {arity},")
                
                # 插入新条目
                insert_pos = extended_content.rfind('}', 0, end_idx)
                if insert_pos != -1:
                    new_arity_str = '\n    # 新增动词元数\n' + '\n'.join(new_arity_entries) + '\n'
                    extended_content = (
                        extended_content[:insert_pos] + 
                        new_arity_str + 
                        extended_content[insert_pos:]
                    )
                
                # 写入最终文件
                with open('src/yanlv/lexer/verb_categories_final.py', 'w', encoding='utf-8') as f:
                    f.write(extended_content)
                
                print(f"已生成完整的动词分类词典: src/yanlv/lexer/verb_categories_final.py")
                print(f"统计:")
                print(f"   - 现有动词: {existing_verb_count}个")
                print(f"   - 新增动词: {total_new_verbs}个")
                print(f"   - 总计动词: {existing_verb_count + total_new_verbs}个")
                print(f"   - 类别数量: {len(NEW_VERBS_BY_CATEGORY) + 12}个")  # 原有12个类别
        
    except FileNotFoundError:
        print("错误: 未找到src/yanlv/lexer/verb_categories.py文件")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()