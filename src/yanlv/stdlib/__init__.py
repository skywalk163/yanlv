"""
言律语言标准库扩展模块
提供Python 3.12+标准库的中文版本
"""

from .collections_ext import *
from .itertools_ext import *
from .functools_ext import *
from .pathlib_ext import *
from .datetime_ext import *
from .math_ext import *
from .json_ext import *
from .random_ext import *
from .re_ext import *
from .statistics_ext import *
from .string_ext import *
from .typing_ext import *
from .dataclasses_ext import *
from .enum_ext import *
from .csv_ext import *
from .hashlib_ext import *
from .contextlib_ext import *
from .textwrap_ext import *
from .pprint_ext import *
from .pickle_ext import *
from .copy_ext import *
from .glob_ext import *
from .operator_ext import *
from .tempfile_ext import *
from .shutil_ext import *
from .bisect_ext import *
# from .heapq_ext import *  # 暂时禁用，有语法错误

__all__ = [
    'collections_ext',
    'itertools_ext', 
    'functools_ext',
    'pathlib_ext',
    'datetime_ext',
    'math_ext',
    'json_ext',
    'random_ext',
    're_ext',
    'statistics_ext',
    'string_ext',
    'typing_ext',
    'dataclasses_ext',
    'enum_ext',
    'csv_ext',
    'hashlib_ext',
    'contextlib_ext',
    'textwrap_ext',
    'pprint_ext',
    'pickle_ext',
    'copy_ext',
    'glob_ext',
    'operator_ext',
    'tempfile_ext',
    'shutil_ext',
    'bisect_ext',
    # 'heapq_ext',  # 暂时禁用
]
