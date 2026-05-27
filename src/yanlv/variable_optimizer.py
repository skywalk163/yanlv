"""
言律语言变量查找优化器

实现优化的变量查找机制,包括局部变量缓存、全局变量索引和作用域链优化
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time


@dataclass
class VariableStats:
    """变量查找统计信息"""
    total_lookups: int = 0          # 总查找次数
    cache_hits: int = 0             # 缓存命中次数
    scope_searches: int = 0         # 作用域链搜索次数
    total_time: float = 0.0         # 总查找时间(毫秒)
    
    @property
    def cache_hit_rate(self) -> float:
        """缓存命中率"""
        return self.cache_hits / self.total_lookups if self.total_lookups > 0 else 0.0
    
    @property
    def average_time(self) -> float:
        """平均查找时间(微秒)"""
        return (self.total_time * 1000) / self.total_lookups if self.total_lookups > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'total_lookups': self.total_lookups,
            'cache_hits': self.cache_hits,
            'cache_hit_rate': f"{self.cache_hit_rate:.2%}",
            'scope_searches': self.scope_searches,
            'average_time_us': f"{self.average_time:.2f}μs"
        }


class Scope:
    """
    作用域类
    
    管理单个作用域内的变量
    """
    
    def __init__(self, name: str = "global", parent: Optional['Scope'] = None):
        """
        初始化作用域
        
        Args:
            name: 作用域名称
            parent: 父作用域
        """
        self.name = name
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}  # 变量值缓存
        self._cache_enabled = True
    
    def get(self, name: str, stats: Optional[VariableStats] = None) -> Any:
        """
        获取变量值(支持作用域链查找)
        
        Args:
            name: 变量名
            stats: 统计信息对象
            
        Returns:
            变量值
            
        Raises:
            NameError: 变量未定义
        """
        start_time = time.time()
        
        # 尝试从缓存获取
        if self._cache_enabled and name in self._cache:
            if stats:
                stats.total_lookups += 1
                stats.cache_hits += 1
                stats.total_time += (time.time() - start_time) * 1000
            return self._cache[name]
        
        # 在当前作用域查找
        if name in self.variables:
            value = self.variables[name]
            # 更新缓存
            if self._cache_enabled:
                self._cache[name] = value
            
            if stats:
                stats.total_lookups += 1
                stats.total_time += (time.time() - start_time) * 1000
            
            return value
        
        # 在父作用域查找
        if self.parent:
            if stats:
                stats.scope_searches += 1
            return self.parent.get(name, stats)
        
        # 变量未定义
        raise NameError(f"未定义的变量: {name}")
    
    def set(self, name: str, value: Any, local: bool = False) -> None:
        """
        设置变量值
        
        Args:
            name: 变量名
            value: 变量值
            local: 是否为局部变量(仅在当前作用域设置)
        """
        if local:
            # 强制在当前作用域设置
            self.variables[name] = value
        else:
            # 查找变量是否已存在
            if name in self.variables:
                self.variables[name] = value
            elif self.parent and self._exists_in_chain(name):
                # 在定义的作用域更新
                self._set_in_chain(name, value)
            else:
                # 在当前作用域创建新变量
                self.variables[name] = value
        
        # 更新缓存
        if self._cache_enabled:
            self._cache[name] = value
    
    def _exists_in_chain(self, name: str) -> bool:
        """检查变量是否在作用域链中存在"""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent._exists_in_chain(name)
        return False
    
    def _set_in_chain(self, name: str, value: Any) -> bool:
        """在作用域链中设置变量"""
        if name in self.variables:
            self.variables[name] = value
            if self._cache_enabled:
                self._cache[name] = value
            return True
        if self.parent:
            return self.parent._set_in_chain(name, value)
        return False
    
    def delete(self, name: str) -> bool:
        """
        删除变量
        
        Args:
            name: 变量名
            
        Returns:
            是否成功删除
        """
        if name in self.variables:
            del self.variables[name]
            if name in self._cache:
                del self._cache[name]
            return True
        return False
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def enable_cache(self) -> None:
        """启用缓存"""
        self._cache_enabled = True
    
    def disable_cache(self) -> None:
        """禁用缓存"""
        self._cache_enabled = False
        self._cache.clear()
    
    def get_all_variables(self) -> Dict[str, Any]:
        """获取所有变量(包括父作用域)"""
        result = {}
        if self.parent:
            result.update(self.parent.get_all_variables())
        result.update(self.variables)
        return result
    
    def __contains__(self, name: str) -> bool:
        """检查变量是否存在"""
        return name in self.variables or (self.parent and name in self.parent)
    
    def __repr__(self) -> str:
        return f"Scope(name='{self.name}', variables={len(self.variables)})"


class OptimizedVariableManager:
    """
    优化的变量管理器
    
    管理多个作用域,提供快速的变量查找和设置
    """
    
    def __init__(self, enable_cache: bool = True):
        """
        初始化变量管理器
        
        Args:
            enable_cache: 是否启用缓存
        """
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scope_stack: List[Scope] = [self.global_scope]
        self.stats = VariableStats()
        self._cache_enabled = enable_cache
        
        if not enable_cache:
            self.global_scope.disable_cache()
    
    def enter_scope(self, name: str = "local") -> Scope:
        """
        进入新作用域
        
        Args:
            name: 作用域名称
            
        Returns:
            新作用域对象
        """
        new_scope = Scope(name, self.current_scope)
        if not self._cache_enabled:
            new_scope.disable_cache()
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self) -> Optional[Scope]:
        """
        退出当前作用域
        
        Returns:
            退出的作用域对象
        """
        if len(self.scope_stack) > 1:
            exited_scope = self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            return exited_scope
        return None
    
    def get(self, name: str) -> Any:
        """
        获取变量值
        
        Args:
            name: 变量名
            
        Returns:
            变量值
        """
        return self.current_scope.get(name, self.stats)
    
    def set(self, name: str, value: Any, local: bool = False) -> None:
        """
        设置变量值
        
        Args:
            name: 变量名
            value: 变量值
            local: 是否为局部变量
        """
        self.current_scope.set(name, value, local)
    
    def set_global(self, name: str, value: Any) -> None:
        """
        设置全局变量
        
        Args:
            name: 变量名
            value: 变量值
        """
        self.global_scope.set(name, value, local=True)
    
    def delete(self, name: str) -> bool:
        """
        删除变量
        
        Args:
            name: 变量名
            
        Returns:
            是否成功删除
        """
        return self.current_scope.delete(name)
    
    def exists(self, name: str) -> bool:
        """
        检查变量是否存在
        
        Args:
            name: 变量名
            
        Returns:
            是否存在
        """
        return name in self.current_scope
    
    def get_stats(self) -> VariableStats:
        """获取统计信息"""
        return self.stats
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        self.stats = VariableStats()
    
    def clear_all_caches(self) -> None:
        """清空所有作用域的缓存"""
        for scope in self.scope_stack:
            scope.clear_cache()
    
    def enable_cache(self) -> None:
        """启用缓存"""
        self._cache_enabled = True
        for scope in self.scope_stack:
            scope.enable_cache()
    
    def disable_cache(self) -> None:
        """禁用缓存"""
        self._cache_enabled = False
        for scope in self.scope_stack:
            scope.disable_cache()
    
    def get_all_variables(self) -> Dict[str, Any]:
        """获取所有变量"""
        return self.current_scope.get_all_variables()
    
    def get_scope_depth(self) -> int:
        """获取当前作用域深度"""
        return len(self.scope_stack)
    
    def __repr__(self) -> str:
        return (
            f"OptimizedVariableManager("
            f"scope_depth={self.get_scope_depth()}, "
            f"cache_hit_rate={self.stats.cache_hit_rate:.2%})"
        )


# 全局变量管理器实例
_global_manager: Optional[OptimizedVariableManager] = None


def get_global_variable_manager() -> OptimizedVariableManager:
    """获取全局变量管理器"""
    global _global_manager
    if _global_manager is None:
        _global_manager = OptimizedVariableManager()
    return _global_manager
