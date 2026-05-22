"""
扩展动词分类词典

为言律语言添加更多动词到分类词典
"""

import json
from typing import Dict, List, Any

# 新的动词分类数据
NEW_VERB_CATEGORIES = {
    # 状态转换动词 - 增加更多状态变化动词
    "STATE_TRANSITION": {
        "verbs": ["变为", "变成", "转为", "切换为", "转换为", "变化为", "转成", "改成", "调整为", 
                 "转变为", "演化成", "发展成", "进化为", "退化为", "升级为", "降级为", "优化为", "简化为"],
        "count": 18
    },
    
    # 赋值动词 - 增加更多赋值相关动词
    "ASSIGNMENT": {
        "verbs": ["等于", "设为", "设置为", "赋值为", "=", "是", "定义为", "指定为", "赋给",
                 "赋值", "设定", "指定", "命名", "称为", "叫作", "标记为", "标识为", "标注为"],
        "count": 18
    },
    
    # 输出动词 - 增加更多输出相关动词
    "OUTPUT": {
        "verbs": ["印", "打印", "显示", "输出", "记录", "输出为", "展示", "呈现", "打印出", "显示为",
                 "输出到", "写入", "保存", "导出", "转储", "日志", "报告", "通报", "公布", "发布"],
        "count": 20
    },
    
    # 控制动词 - 增加更多控制相关动词
    "CONTROL": {
        "verbs": ["开启", "关闭", "启动", "停止", "执行", "运行", "暂停", "继续", "重启", "终止",
                 "激活", "禁用", "启用", "封锁", "解锁", "加载", "卸载", "安装", "卸载", "配置"],
        "count": 20
    },
    
    # 计算动词 - 增加更多计算相关动词
    "COMPUTATION": {
        "verbs": ["计算", "求和", "求积", "比较", "排序", "过滤", "映射", "归约", "统计", "分析",
                 "求平均", "求最大", "求最小", "求方差", "求标准差", "聚合", "分组", "连接", "合并", "拆分"],
        "count": 20
    },
    
    # 移动动词 - 增加更多移动相关动词
    "MOVEMENT": {
        "verbs": ["移动", "前进", "后退", "旋转", "转向", "跳跃", "飞行", "行走", "跑动", "滑动",
                 "平移", "缩放", "旋转", "倾斜", "翻转", "滚动", "拖动", "拉动", "推动", "举起"],
        "count": 20
    },
    
    # 创建动词 - 增加更多创建相关动词
    "CREATION": {
        "verbs": ["创建", "生成", "建立", "构造", "初始化", "新建", "产生", "制造", "组建", "设立",
                 "发明", "设计", "开发", "编写", "绘制", "建模", "模拟", "仿真", "复制", "克隆"],
        "count": 20
    },
    
    # 销毁动词 - 增加更多销毁相关动词
    "DESTRUCTION": {
        "verbs": ["删除", "销毁", "清除", "移除", "释放", "消灭", "拆除", "丢弃", "废除", "撤销",
                 "取消", "废止", "终止", "结束", "关闭", "销毁", "抹除", "擦除", "清空", "重置"],
        "count": 20
    },
    
    # 查询动词 - 增加更多查询相关动词
    "QUERY": {
        "verbs": ["查询", "搜索", "查找", "获取", "读取", "检索", "查找", "搜索", "获取", "读取",
                 "提取", "抽取", "选择", "筛选", "过滤", "查找", "搜索", "浏览", "查看", "检查"],
        "count": 20
    },
    
    # 修改动词 - 增加更多修改相关动词
    "MODIFICATION": {
        "verbs": ["修改", "更新", "编辑", "调整", "改变", "修正", "变更", "改动", "调节", "优化",
                 "改进", "增强", "减弱", "增加", "减少", "放大", "缩小", "扩展", "收缩", "变形"],
        "count": 20
    },
    
    # 通信动词 - 增加更多通信相关动词
    "COMMUNICATION": {
        "verbs": ["发送", "接收", "传输", "传递", "通知", "报告", "告知", "通信", "传达", "广播",
                 "分享", "转发", "回复", "响应", "呼叫", "联系", "连接", "断开", "同步", "异步"],
        "count": 20
    },
    
    # 比较动词 - 增加更多比较相关动词
    "COMPARISON": {
        "verbs": ["比较", "对比", "对照", "匹配", "检查", "验证", "测试", "评估", "衡量", "判断",
                 "评审", "审核", "检验", "检测", "监测", "观察", "监视", "跟踪", "追踪", "记录"],
        "count": 20
    },
    
    # 转换动词 - 增加更多转换相关动词
    "TRANSFORMATION": {
        "verbs": ["转换", "变换", "翻译", "解析", "编译", "解释", "编码", "解码", "格式化", "序列化",
                 "反序列化", "加密", "解密", "压缩", "解压", "转换", "变换", "翻译", "转码", "转义"],
        "count": 20
    },
    
    # 新增类别：数学运算动词
    "MATH_OPERATION": {
        "verbs": ["加", "减", "乘", "除", "模", "幂", "开方", "对数", "指数", "正弦",
                 "余弦", "正切", "反正弦", "反余弦", "反正切", "绝对值", "取整", "舍入", "取余", "求商"],
        "count": 20
    },
    
    # 新增类别：逻辑运算动词
    "LOGIC_OPERATION": {
        "verbs": ["与", "或", "非", "且", "或者", "不是", "异或", "同或", "蕴含", "等价",
                 "真", "假", "成立", "不成立", "满足", "不满足", "符合", "不符合", "匹配", "不匹配"],
        "count": 20
    },
    
    # 新增类别：时间操作动词
    "TIME_OPERATION": {
        "verbs": ["等待", "延迟", "暂停", "继续", "开始", "结束", "计时", "定时", "计划", "调度",
                 "提前", "推迟", "加速", "减速", "同步", "异步", "实时", "定时", "周期", "频率"],
        "count": 20
    },
    
    # 新增类别：文件操作动词
    "FILE_OPERATION": {
        "verbs": ["打开", "关闭", "读取", "写入", "保存", "加载", "导入", "导出", "复制", "移动",
                 "重命名", "删除", "创建", "查找", "搜索", "压缩", "解压", "加密", "解密", "备份"],
        "count": 20
    },
    
    # 新增类别：网络操作动词
    "NETWORK_OPERATION": {
        "verbs": ["连接", "断开", "发送", "接收", "请求", "响应", "下载", "上传", "同步", "异步",
                 "推送", "拉取", "订阅", "发布", "广播", "组播", "路由", "转发", "代理", "隧道"],
        "count": 20
    },
    
    # 新增类别：数据库操作动词
    "DATABASE_OPERATION": {
        "verbs": ["插入", "更新", "删除", "查询", "选择", "创建", "删除", "修改", "备份", "恢复",
                 "索引", "连接", "事务", "提交", "回滚", "锁定", "解锁", "优化", "迁移", "同步"],
        "count": 20
    },
    
    # 新增类别：用户界面动词
    "UI_OPERATION": {
        "verbs": ["显示", "隐藏", "启用", "禁用", "聚焦", "失焦", "点击", "双击", "拖动", "滚动",
                 "缩放", "旋转", "平移", "选择", "取消", "确认", "取消", "提交", "重置", "刷新"],
        "count": 20
    },
    
    # 新增类别：错误处理动词
    "ERROR_HANDLING": {
        "verbs": ["捕获", "抛出", "处理", "忽略", "记录", "报告", "恢复", "重试", "回退", "补偿",
                 "验证", "检查", "预防", "避免", "修复", "调试", "测试", "监控", "告警", "通知"],
        "count": 20
    },
    
    # 新增类别：安全操作动词
    "SECURITY_OPERATION": {
        "verbs": ["验证", "授权", "认证", "加密", "解密", "签名", "验签", "哈希", "加盐", "令牌",
                 "会话", "cookie", "证书", "密钥", "密码", "权限", "角色", "审计", "日志", "监控"],
        "count": 20
    }
}

def extend_verb_categories():
    """扩展动词分类词典"""
    print("扩展动词分类词典")
    print("=" * 60)
    
    # 读取现有的verb_categories.py文件
    with open('src/yanlv/lexer/verb_categories.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到VERB_CATEGORIES定义的位置
    start_idx = content.find('VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {')
    if start_idx == -1:
        print("错误: 未找到VERB_CATEGORIES定义")
        return
    
    # 找到定义的结束位置
    brace_count = 0
    end_idx = start_idx
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if brace_count != 0:
        print("错误: 未找到匹配的大括号")
        return
    
    # 提取现有的分类
    existing_categories = content[start_idx:end_idx]
    
    # 统计现有的动词数量
    import re
    verb_matches = re.findall(r'"verbs": \[(.*?)\]', existing_categories, re.DOTALL)
    existing_verb_count = 0
    for match in verb_matches:
        verbs = re.findall(r'"([^"]+)"', match)
        existing_verb_count += len(verbs)
    
    print(f"现有动词数量: {existing_verb_count}")
    print(f"新添加动词数量: {sum(cat['count'] for cat in NEW_VERB_CATEGORIES.values())}")
    print(f"扩展后总动词数量: {existing_verb_count + sum(cat['count'] for cat in NEW_VERB_CATEGORIES.values())}")
    
    # 生成新的分类定义
    new_categories = []
    for category_name, category_data in NEW_VERB_CATEGORIES.items():
        verbs_str = ', '.join(f'"{verb}"' for verb in category_data["verbs"])
        new_categories.append(f'''    # {category_name.replace("_", " ").title()}动词 ({category_data["count"]}个)
    "{category_name}": {{
        "verbs": [{verbs_str}],
        "pattern": r'^[^{category_data["verbs"][0]}]+{category_data["verbs"][0]}[^。]*[。]$',
        "interpretation": "{category_name}_ACTION",
        "semantic_role": "{category_name}",
        "arity": 2,
        "examples": [
            "示例1。",
            "示例2。",
            "示例3。"
        ]
    }},''')
    
    # 创建新的文件内容
    new_content = content[:start_idx] + 'VERB_CATEGORIES: Dict[str, Dict[str, Any]] = {\n'
    new_content += existing_categories[existing_categories.find('{')+1:existing_categories.rfind('}')].rstrip(',\n')
    new_content += ',\n\n'
    new_content += '\n\n'.join(new_categories)
    new_content += '\n}\n\n'
    new_content += content[end_idx:]
    
    # 写入新文件
    with open('src/yanlv/lexer/verb_categories_extended.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n已生成扩展的动词分类词典: src/yanlv/lexer/verb_categories_extended.py")
    print(f"新增类别: {len(NEW_VERB_CATEGORIES)}个")
    
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
                    end_idx = i + 1
                    break