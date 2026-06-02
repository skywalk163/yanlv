"""
言律语言hashlib模块扩展
提供hashlib标准库的中文版本
"""

import hashlib
from typing import Union


def 计算MD5(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算MD5哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        MD5哈希值（十六进制字符串）
        
    示例:
        >>> 计算MD5('hello')
        '5d41402abc4b2a76b9719d911017c592'
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.md5(数据).hexdigest()


def 计算SHA1(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算SHA1哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        SHA1哈希值（十六进制字符串）
        
    示例:
        >>> 计算SHA1('hello')
        'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.sha1(数据).hexdigest()


def 计算SHA256(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算SHA256哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        SHA256哈希值（十六进制字符串）
        
    示例:
        >>> 计算SHA256('hello')
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.sha256(数据).hexdigest()


def 计算SHA512(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算SHA512哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        SHA512哈希值（十六进制字符串）
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.sha512(数据).hexdigest()


def 计算文件哈希(
    文件路径: str,
    算法: str = 'sha256',
    块大小: int = 65536
) -> str:
    """
    计算文件的哈希值
    
    参数:
        文件路径: 文件路径
        算法: 哈希算法（'md5', 'sha1', 'sha256', 'sha512'）
        块大小: 读取块大小
        
    返回:
        哈希值（十六进制字符串）
        
    示例:
        >>> 计算文件哈希('test.txt', 'md5')
        'd41d8cd98f00b204e9800998ecf8427e'
    """
    哈希对象 = hashlib.new(算法)
    
    with open(文件路径, 'rb') as 文件:
        while True:
            块 = 文件.read(块大小)
            if not 块:
                break
            哈希对象.update(块)
    
    return 哈希对象.hexdigest()


def 验证哈希(
    数据: Union[str, bytes],
    期望哈希值: str,
    算法: str = 'sha256',
    编码: str = 'utf-8'
) -> bool:
    """
    验证数据的哈希值
    
    参数:
        数据: 要验证的数据
        期望哈希值: 期望的哈希值
        算法: 哈希算法
        编码: 字符串编码
        
    返回:
        是否匹配
        
    示例:
        >>> 验证哈希('hello', '5d41402abc4b2a76b9719d911017c592', 'md5')
        True
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    
    哈希对象 = hashlib.new(算法)
    哈希对象.update(数据)
    实际哈希值 = 哈希对象.hexdigest()
    
    return 实际哈希值 == 期望哈希值


def 创建哈希对象(算法: str = 'sha256'):
    """
    创建哈希对象
    
    参数:
        算法: 哈希算法
        
    返回:
        哈希对象
        
    示例:
        >>> 哈希 = 创建哈希对象('md5')
        >>> 哈希.update(b'hello')
        >>> 哈希.hexdigest()
        '5d41402abc4b2a76b9719d911017c592'
    """
    return hashlib.new(算法)


def 计算哈希(
    数据: Union[str, bytes],
    算法: str = 'sha256',
    编码: str = 'utf-8'
) -> str:
    """
    计算指定算法的哈希值
    
    参数:
        数据: 要计算的数据
        算法: 哈希算法
        编码: 字符串编码
        
    返回:
        哈希值（十六进制字符串）
        
    示例:
        >>> 计算哈希('hello', 'md5')
        '5d41402abc4b2a76b9719d911017c592'
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    
    哈希对象 = hashlib.new(算法)
    哈希对象.update(数据)
    return 哈希对象.hexdigest()


def 获取可用算法() -> list:
    """
    获取所有可用的哈希算法
    
    返回:
        算法名称列表
        
    示例:
        >>> 获取可用算法()
        ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', ...]
    """
    return list(hashlib.algorithms_available)


def 计算密码哈希(
    密码: str,
    盐值: bytes = None,
    迭代次数: int = 100000,
    算法: str = 'sha256'
) -> tuple:
    """
    计算密码哈希（使用PBKDF2）
    
    参数:
        密码: 密码字符串
        盐值: 盐值（None表示自动生成）
        迭代次数: 迭代次数
        算法: 哈希算法
        
    返回:
        (哈希值, 盐值)元组
        
    示例:
        >>> 哈希值, 盐值 = 计算密码哈希('mypassword')
    """
    import os
    
    if 盐值 is None:
        盐值 = os.urandom(16)
    
    哈希值 = hashlib.pbkdf2_hmac(
        算法,
        密码.encode('utf-8'),
        盐值,
        迭代次数
    )
    
    return (哈希值.hex(), 盐值.hex())


def 验证密码哈希(
    密码: str,
    哈希值: str,
    盐值: str,
    迭代次数: int = 100000,
    算法: str = 'sha256'
) -> bool:
    """
    验证密码哈希
    
    参数:
        密码: 密码字符串
        哈希值: 存储的哈希值
        盐值: 盐值
        迭代次数: 迭代次数
        算法: 哈希算法
        
    返回:
        是否匹配
        
    示例:
        >>> 验证密码哈希('mypassword', 哈希值, 盐值)
        True
    """
    新哈希值, _ = 计算密码哈希(
        密码,
        bytes.fromhex(盐值),
        迭代次数,
        算法
    )
    
    return 新哈希值 == 哈希值


def 计算BLAKE2b(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算BLAKE2b哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        BLAKE2b哈希值
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.blake2b(数据).hexdigest()


def 计算BLAKE2s(数据: Union[str, bytes], 编码: str = 'utf-8') -> str:
    """
    计算BLAKE2s哈希值
    
    参数:
        数据: 要计算的数据
        编码: 字符串编码
        
    返回:
        BLAKE2s哈希值
    """
    if isinstance(数据, str):
        数据 = 数据.encode(编码)
    return hashlib.blake2s(数据).hexdigest()


# ============================================================================
# 导出所有函数
# ============================================================================

__all__ = [
    # 常用哈希函数
    '计算MD5', '计算SHA1', '计算SHA256', '计算SHA512',
    
    # 文件哈希
    '计算文件哈希',
    
    # 验证和工具
    '验证哈希', '创建哈希对象', '计算哈希', '获取可用算法',
    
    # 密码哈希
    '计算密码哈希', '验证密码哈希',
    
    # BLAKE2
    '计算BLAKE2b', '计算BLAKE2s',
]
