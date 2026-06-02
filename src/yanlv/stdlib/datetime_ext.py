"""
言律语言datetime模块扩展
提供datetime标准库的中文版本
"""

from datetime import datetime, date, time, timedelta, timezone
from typing import Optional, Union


class 日期时间(datetime):
    """
    日期时间对象
    
    示例:
        >>> 现在 = 日期时间.现在()
        >>> 打印(现在.格式化('%Y年%m月%d日 %H:%M:%S'))
        2024年01月15日 10:30:45
    """
    
    @classmethod
    def 现在(cls) -> '日期时间':
        """获取当前日期时间"""
        return cls.从datetime(datetime.now())
    
    @classmethod
    def 当前时间戳(cls) -> float:
        """获取当前时间戳"""
        return datetime.now().timestamp()
    
    @classmethod
    def 从时间戳(cls, 时间戳: float) -> '日期时间':
        """从时间戳创建日期时间"""
        return cls.从datetime(datetime.fromtimestamp(时间戳))
    
    @classmethod
    def 从字符串(cls, 字符串: str, 格式: str) -> '日期时间':
        """从字符串解析日期时间"""
        return cls.从datetime(datetime.strptime(字符串, 格式))
    
    @classmethod
    def 从datetime(cls, dt: datetime) -> '日期时间':
        """从datetime对象创建"""
        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            dt.tzinfo
        )
    
    def 格式化(self, 格式: str = '%Y-%m-%d %H:%M:%S') -> str:
        """格式化日期时间"""
        return self.strftime(格式)
    
    def 获取年份(self) -> int:
        """获取年份"""
        return self.year
    
    def 获取月份(self) -> int:
        """获取月份"""
        return self.month
    
    def 获取日期(self) -> int:
        """获取日期"""
        return self.day
    
    def 获取小时(self) -> int:
        """获取小时"""
        return self.hour
    
    def 获取分钟(self) -> int:
        """获取分钟"""
        return self.minute
    
    def 获取秒数(self) -> int:
        """获取秒数"""
        return self.second
    
    def 获取星期(self) -> int:
        """获取星期（0=周一, 6=周日）"""
        return self.weekday()
    
    def 获取星期名称(self) -> str:
        """获取星期名称"""
        星期名称 = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return 星期名称[self.weekday()]
    
    def 获取年份第几天(self) -> int:
        """获取年份中的第几天"""
        return self.timetuple().tm_yday
    
    def 获取年份第几周(self) -> int:
        """获取年份中的第几周"""
        return self.isocalendar()[1]
    
    def 添加时间(
        self,
        天数: int = 0,
        秒数: int = 0,
        微秒: int = 0,
        毫秒: int = 0,
        分钟: int = 0,
        小时: int = 0,
        周数: int = 0
    ) -> '日期时间':
        """添加时间"""
        delta = 时间差(
            days=天数,
            seconds=秒数,
            microseconds=微秒,
            milliseconds=毫秒,
            minutes=分钟,
            hours=小时,
            weeks=周数
        )
        return 日期时间.fromdatetime(self + delta)
    
    def 减去时间(
        self,
        天数: int = 0,
        秒数: int = 0,
        微秒: int = 0,
        毫秒: int = 0,
        分钟: int = 0,
        小时: int = 0,
        周数: int = 0
    ) -> '日期时间':
        """减去时间"""
        return self.添加时间(
            天数=-天数,
            秒数=-秒数,
            微秒=-微秒,
            毫秒=-毫秒,
            分钟=-分钟,
            小时=-小时,
            周数=-周数
        )
    
    def 转换时区(self, 时区: timezone) -> '日期时间':
        """转换时区"""
        return 日期时间.从datetime(self.astimezone(时区))
    
    def 转为日期(self) -> '日期':
        """转换为日期对象"""
        return 日期.从date(self.date())
    
    def 转为时间(self) -> '时间':
        """转换为时间对象"""
        return 时间.从time(self.time())
    
    def 转为时间戳(self) -> float:
        """转换为时间戳"""
        return self.timestamp()


class 日期(date):
    """
    日期对象
    
    示例:
        >>> 今天 = 日期.今天()
        >>> 打印(今天)
        2024-01-15
    """
    
    @classmethod
    def 今天(cls) -> '日期':
        """获取今天的日期"""
        return cls.从date(date.today())
    
    @classmethod
    def 从字符串(cls, 字符串: str, 格式: str = '%Y-%m-%d') -> '日期':
        """从字符串解析日期"""
        dt = datetime.strptime(字符串, 格式)
        return cls.从date(dt.date())
    
    @classmethod
    def 从date(cls, d: date) -> '日期':
        """从date对象创建"""
        return cls(d.year, d.month, d.day)
    
    def 格式化(self, 格式: str = '%Y-%m-%d') -> str:
        """格式化日期"""
        return self.strftime(格式)
    
    def 获取年份(self) -> int:
        """获取年份"""
        return self.year
    
    def 获取月份(self) -> int:
        """获取月份"""
        return self.month
    
    def 获取日期(self) -> int:
        """获取日期"""
        return self.day
    
    def 获取星期(self) -> int:
        """获取星期（0=周一, 6=周日）"""
        return self.weekday()
    
    def 获取星期名称(self) -> str:
        """获取星期名称"""
        星期名称 = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return 星期名称[self.weekday()]
    
    def 是否工作日(self) -> bool:
        """是否为工作日"""
        return self.weekday() < 5
    
    def 是否周末(self) -> bool:
        """是否为周末"""
        return self.weekday() >= 5
    
    def 添加天数(self, 天数: int) -> '日期':
        """添加天数"""
        return 日期.从date(self + timedelta(days=天数))
    
    def 添加周数(self, 周数: int) -> '日期':
        """添加周数"""
        return 日期.从date(self + timedelta(weeks=周数))
    
    def 添加月份(self, 月份: int) -> '日期':
        """添加月份"""
        年 = self.year + (self.month + 月份 - 1) // 12
        月 = (self.month + 月份 - 1) % 12 + 1
        日 = min(self.day, self._该月天数(年, 月))
        return 日期(年, 月, 日)
    
    def _该月天数(self, 年: int, 月: int) -> int:
        """获取该月的天数"""
        if 月 == 12:
            下月 = 日期(年 + 1, 1, 1)
        else:
            下月 = 日期(年, 月 + 1, 1)
        return (下月 - 日期(年, 月, 1)).days
    
    def 转为日期时间(self, 小时: int = 0, 分钟: int = 0, 秒数: int = 0) -> 日期时间:
        """转换为日期时间对象"""
        return 日期时间(
            self.year, self.month, self.day,
            小时, 分钟, 秒数
        )


class 时间(time):
    """
    时间对象
    
    示例:
        >>> t = 时间(10, 30, 45)
        >>> 打印(t.格式化('%H:%M:%S'))
        10:30:45
    """
    
    @classmethod
    def 当前时间(cls) -> '时间':
        """获取当前时间"""
        return cls.从time(datetime.now().time())
    
    @classmethod
    def 从字符串(cls, 字符串: str, 格式: str = '%H:%M:%S') -> '时间':
        """从字符串解析时间"""
        dt = datetime.strptime(字符串, 格式)
        return cls.从time(dt.time())
    
    @classmethod
    def 从time(cls, t: time) -> '时间':
        """从time对象创建"""
        return cls(t.hour, t.minute, t.second, t.microsecond, t.tzinfo)
    
    def 格式化(self, 格式: str = '%H:%M:%S') -> str:
        """格式化时间"""
        return self.strftime(格式)
    
    def 获取小时(self) -> int:
        """获取小时"""
        return self.hour
    
    def 获取分钟(self) -> int:
        """获取分钟"""
        return self.minute
    
    def 获取秒数(self) -> int:
        """获取秒数"""
        return self.second
    
    def 获取微秒(self) -> int:
        """获取微秒"""
        return self.microsecond
    
    def 转为秒数(self) -> int:
        """转换为总秒数"""
        return self.hour * 3600 + self.minute * 60 + self.second


class 时间差(timedelta):
    """
    时间差对象
    
    示例:
        >>> delta = 时间差(天数=7)
        >>> 打印(delta.总天数())
        7.0
    """
    
    def 总秒数(self) -> float:
        """获取总秒数"""
        return self.total_seconds()
    
    def 总天数(self) -> float:
        """获取总天数"""
        return self.total_seconds() / 86400
    
    def 总小时数(self) -> float:
        """获取总小时数"""
        return self.total_seconds() / 3600
    
    def 总分钟数(self) -> float:
        """获取总分钟数"""
        return self.total_seconds() / 60
    
    def 格式化(self) -> str:
        """格式化时间差"""
        总秒数 = abs(int(self.total_seconds()))
        天 = 总秒数 // 86400
        时 = (总秒数 % 86400) // 3600
        分 = (总秒数 % 3600) // 60
        秒 = 总秒数 % 60
        
        部分 = []
        if 天 > 0:
            部分.append(f'{天}天')
        if 时 > 0:
            部分.append(f'{时}小时')
        if 分 > 0:
            部分.append(f'{分}分钟')
        if 秒 > 0 or not 部分:
            部分.append(f'{秒}秒')
        
        结果 = ''.join(部分)
        return 结果 if self.total_seconds() >= 0 else f'-{结果}'


def 创建时区(小时偏移: int, 分钟偏移: int = 0, 名称: Optional[str] = None) -> timezone:
    """
    创建时区
    
    参数:
        小时偏移: 小时偏移量
        分钟偏移: 分钟偏移量
        名称: 时区名称
        
    返回:
        timezone对象
        
    示例:
        >>> 东八区 = 创建时区(8)
        >>> 西五区 = 创建时区(-5)
    """
    from datetime import timedelta
    offset = timedelta(hours=小时偏移, minutes=分钟偏移)
    if 名称 is not None:
        return timezone(offset, 名称)
    return timezone(offset)


# 常用时区
UTC = timezone.utc
东八区 = 创建时区(8, 名称='CST')


# ============================================================================
# 导出所有类和函数
# ============================================================================

__all__ = [
    '日期时间',
    '日期',
    '时间',
    '时间差',
    '创建时区',
    'UTC',
    '东八区',
]
