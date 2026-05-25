"""
言律语言词法分析器 - 常量定义

包含所有常量、配置和默认值
"""

from typing import Dict, Set, Tuple, List, Any
from .lexer_token import TokenType


# ============================================================================
# 中文标点符号映射
# ============================================================================

CHINESE_PUNCTUATION: Dict[str, TokenType] = {
    '。': TokenType.PERIOD,
    '，': TokenType.COMMA,
    '；': TokenType.SEMICOLON,
    '：': TokenType.COLON,
    '、': TokenType.ENUMERATION,
    '！': TokenType.EXCLAMATION,
    '？': TokenType.QUESTION,
    '《': TokenType.BOOK_TITLE,
    '》': TokenType.BOOK_TITLE,
    '……': TokenType.ELLIPSIS,
    '——': TokenType.DASH,
    '～': TokenType.TILDE,
    '·': TokenType.MIDDLE_DOT,
    '【': TokenType.SQUARE_BRACKETS,
    '】': TokenType.SQUARE_BRACKETS,
    '（': TokenType.LPAREN,
    '）': TokenType.RPAREN,
    '「': TokenType.LBRACKET,
    '」': TokenType.RBRACKET,
    '『': TokenType.LBRACE,
    '』': TokenType.RBRACE,
}


# ============================================================================
# 运算符映射
# ============================================================================

OPERATORS: Dict[str, TokenType] = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '%': TokenType.MODULO,
    '^': TokenType.POWER,
    '=': TokenType.EQUAL,
    '≠': TokenType.NOT_EQUAL,
    '<': TokenType.LESS,
    '>': TokenType.GREATER,
    '≤': TokenType.LESS_EQUAL,
    '≥': TokenType.GREATER_EQUAL,
    '且': TokenType.AND,
    '或': TokenType.OR,
    '¬': TokenType.NOT,
    '&': TokenType.AND,
    '|': TokenType.OR,
    '!': TokenType.NOT,
}


# ============================================================================
# 分组符号映射
# ============================================================================

GROUPING_SYMBOLS: Dict[str, TokenType] = {
    '(': TokenType.LPAREN,
    ')': TokenType.RPAREN,
    '[': TokenType.LBRACKET,
    ']': TokenType.RBRACKET,
    '{': TokenType.LBRACE,
    '}': TokenType.RBRACE,
}


# ============================================================================
# 关键词映射
# ============================================================================

KEYWORDS: Dict[str, TokenType] = {
    '如果': TokenType.IF,
    '要是': TokenType.IF,
    '否则': TokenType.ELSE,
    '不然': TokenType.ELSE,
    '当': TokenType.WHEN,
    '就': TokenType.THEN,
    '对于': TokenType.FOR,
    '在': TokenType.IN,
    '一直': TokenType.WHILE,
    '定': TokenType.DEF,
    '定义': TokenType.DEFINE,
    '设': TokenType.SET,
    '设置': TokenType.SET,  # 添加完整的"设置"关键词
    '是': TokenType.IS,
    '等于': TokenType.IS,
    '返回': TokenType.RETURN,
    '结束': TokenType.END,
    '循环': TokenType.LOOP,
    '遍历': TokenType.FOR_EACH,
    '每个': TokenType.FOR_EACH,
    '直到': TokenType.UNTIL,
    '否则如果': TokenType.ELIF,
    '否则要是': TokenType.ELIF,
    '真': TokenType.BOOLEAN,
    '假': TokenType.BOOLEAN,
    '空': TokenType.IDENTIFIER,
    '无': TokenType.IDENTIFIER,

    # 言律语言特定关键词
    '输出': TokenType.OUTPUT,
    '打印': TokenType.OUTPUT,
    '显示': TokenType.OUTPUT,
    '变量': TokenType.VARIABLE,
    '函数': TokenType.FUNCTION,
    '参数': TokenType.PARAMETER,
    '为': TokenType.IS,
    '调用': TokenType.CALL,
    '添加': TokenType.ADD,
    '删除': TokenType.REMOVE,
    '长度': TokenType.LENGTH,
    '查找': TokenType.FIND,
    '替换': TokenType.REPLACE,
    '分割': TokenType.SPLIT,
    '子串': TokenType.SUBSTRING,

    # 内置函数 - 数学
    '绝对值': TokenType.ABS,
    '平方根': TokenType.SQRT,
    '幂': TokenType.POW,
    '取整': TokenType.INT,
    '随机数': TokenType.RANDOM,

    # 内置函数 - 数学扩展
    '正弦': TokenType.SIN,
    '余弦': TokenType.COS,
    '正切': TokenType.TAN,
    '自然对数': TokenType.LOG,
    '常用对数': TokenType.LOG10,
    '指数': TokenType.EXP,
    '向上取整': TokenType.CEIL,
    '向下取整': TokenType.FLOOR,
    '四舍五入': TokenType.ROUND,
    '阶乘': TokenType.FACTORIAL,

    # 内置函数 - 数组
    '排序': TokenType.SORT,
    '反转': TokenType.REVERSE,
    '最大值': TokenType.MAX,
    '最小值': TokenType.MIN,
    '求和': TokenType.SUM,

    # 字符串操作增强
    '连接': TokenType.CONCAT,
    '切片': TokenType.SLICE,
    '查找全部': TokenType.FIND_ALL,
    '替换一次': TokenType.REPLACE_ONCE,
    '大写': TokenType.UPPER,
    '小写': TokenType.LOWER,
    '去空格': TokenType.TRIM,
    '去全部空格': TokenType.TRIM_ALL,
    '遍历字符': TokenType.FOR_EACH_CHAR,

    # 文件操作
    '读取文件': TokenType.READ_FILE,
    '读取行': TokenType.READ_LINES,
    '写入文件': TokenType.WRITE_FILE,
    '追加文件': TokenType.APPEND_FILE,
    '文件存在': TokenType.FILE_EXISTS,
    '文件大小': TokenType.FILE_SIZE,
    '文件名': TokenType.FILE_NAME,
    '目录名': TokenType.DIR_NAME,

    # 比较运算符
    '大于': TokenType.GREATER_THAN,
    '小于': TokenType.LESS_THAN,
    '等于': TokenType.EQUAL_TO,
    '大于等于': TokenType.GREATER_EQUAL,
    '小于等于': TokenType.LESS_EQUAL,
    '不等于': TokenType.NOT_EQUAL,

    # 异常处理
    '尝试': TokenType.TRY,
    '捕获': TokenType.CATCH,
    '抛出': TokenType.THROW,
    '异常': TokenType.EXCEPTION,
    '最终': TokenType.FINALLY,
}


# ============================================================================
# 中文数字映射
# ============================================================================

CHINESE_NUMBERS: Dict[str, int] = {
    '零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '十': 10, '百': 100, '千': 1000, '万': 10000,
    '亿': 100000000, '兆': 1000000000000,
}


# ============================================================================
# 百家姓（前100个）
# ============================================================================

BAI_JIA_XING: Set[str] = {
    '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈',
    '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏',
    '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦',
    '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
    '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺',
    '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
    '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余',
    '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹'
}


# ============================================================================
# 冲突姓氏（不能作为变量名）
# ============================================================================

CONFLICT_SURNAMES: Set[str] = {
    '空', '言', '印', '定', '设', '是', '返回', '结束', '循环'
}


# ============================================================================
# 正则表达式模式
# ============================================================================

# 数字模式
NUMBER_PATTERN = r'^\d+(\.\d+)?$'

# 标识符模式（支持中文）
IDENTIFIER_PATTERN = r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*$'

# 字符串字面量模式
STRING_PATTERN = r'^"[^"\\]*(?:\\.[^"\\]*)*"$'

# 注释模式
COMMENT_PATTERN = r'^#.*$'

# 中文数字模式
CHINESE_NUMBER_PATTERN = r'^[零〇一二三四五六七八九十百千万亿兆]+$'

# 动词模式（从verb_categories导入）
VERB_PATTERNS = {
    'STATE_TRANSITION': r'^[^变为]+变为[^。]+[。]$',
    'ASSIGNMENT': r'^[^设为]+设为[^。]+[。]$',
    'OUTPUT': r'^输出[^。]+[。]$',
    'CONTROL': r'^[^开启]+开启[^。]*[。]$',
    'COMPUTATION': r'^计算[^。]+[。]$',
    'MOVEMENT': r'^[^移动]+移动[^。]*[。]$',
    'CREATION': r'^创建[^。]+[。]$',
    'DESTRUCTION': r'^删除[^。]+[。]$',
    'QUERY': r'^查询[^。]+[。]$',
    'MODIFICATION': r'^修改[^。]+[。]$',
    'COMMUNICATION': r'^发送[^。]+[。]$',
    'COMPARISON': r'^比较[^。]+[。]$',
    'TRANSFORMATION': r'^转换[^。]+[。]$',
}


# ============================================================================
# 配置常量
# ============================================================================

# 默认配置
DEFAULT_CONFIG = {
    'segmenter': 'jieba',  # 分词器类型: 'jieba' 或 'thulac'
    'strict_mode': False,   # 严格模式
    'verbose': False,       # 详细输出
    'max_errors': 100,      # 最大错误数
    'enable_cache': True,   # 启用缓存
    'cache_size': 1000,     # 缓存大小
    'timeout': 30,          # 超时时间（秒）
    'max_line_length': 1000, # 最大行长度
}

# 分词器配置
SEGMENTER_CONFIG = {
    'jieba': {
        'dict_path': None,      # 自定义词典路径
        'hmm': True,           # 使用HMM模型
        'user_dict': None,     # 用户词典
    },
    'thulac': {
        'seg_only': True,      # 只分词
        'model_path': None,    # 模型路径
        'user_dict': None,     # 用户词典
    }
}

# 错误代码
ERROR_CODES = {
    'LEXER_ERROR': 'LEX001',
    'TOKENIZATION_ERROR': 'LEX002',
    'PATTERN_ERROR': 'LEX003',
    'SEGMENTATION_ERROR': 'LEX004',
    'MEMORY_ERROR': 'LEX005',
    'TIMEOUT_ERROR': 'LEX006',
}

# 警告代码
WARNING_CODES = {
    'LONG_LINE': 'LEXW001',
    'UNKNOWN_CHAR': 'LEXW002',
    'AMBIGUOUS_TOKEN': 'LEXW003',
    'DEPRECATED_SYNTAX': 'LEXW004',
}


# ============================================================================
# 性能统计常量
# ============================================================================

STATS_TEMPLATE = {
    'tokens_processed': 0,
    'lines_processed': 0,
    'characters_processed': 0,
    'errors': 0,
    'warnings': 0,
    'cache_hits': 0,
    'cache_misses': 0,
    'processing_time': 0.0,
}

# 性能阈值
PERFORMANCE_THRESHOLDS = {
    'max_tokens_per_second': 10000,
    'max_memory_mb': 100,
    'max_processing_time_ms': 1000,
}


# ============================================================================
# 工具函数
# ============================================================================

def get_token_type_name(token_type: TokenType) -> str:
    """获取词元类型名称"""
    return token_type.value

def is_chinese_character(char: str) -> bool:
    """检查字符是否为中文字符"""
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char: str) -> bool:
    """检查字符是否为中文标点"""
    return char in CHINESE_PUNCTUATION

def is_operator(char: str) -> bool:
    """检查字符是否为运算符"""
    return char in OPERATORS

def is_grouping_symbol(char: str) -> bool:
    """检查字符是否为分组符号"""
    return char in GROUPING_SYMBOLS

def is_keyword(word: str) -> bool:
    """检查单词是否为关键词"""
    return word in KEYWORDS

def is_bai_jia_xing(word: str) -> bool:
    """检查单词是否为百家姓"""
    return word in BAI_JIA_XING

def is_conflict_surname(word: str) -> bool:
    """检查单词是否为冲突姓氏"""
    return word in CONFLICT_SURNAMES