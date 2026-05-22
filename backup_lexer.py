"""
备份lexer.py文件
"""

import shutil
import os

def backup_lexer():
    """备份lexer.py文件"""
    src_file = 'src/yanlv/lexer/lexer.py'
    backup_file = 'src/yanlv/lexer/lexer_original_backup.py'
    
    if os.path.exists(src_file):
        shutil.copy2(src_file, backup_file)
        print(f"已备份: {src_file} -> {backup_file}")
        
        # 检查备份文件大小
        if os.path.exists(backup_file):
            size = os.path.getsize(backup_file)
            print(f"备份文件大小: {size} 字节 ({size/1024:.2f} KB)")
            return True
        else:
            print("备份失败: 备份文件未创建")
            return False
    else:
        print(f"源文件不存在: {src_file}")
        return False

if __name__ == "__main__":
    if backup_lexer():
        print("备份成功!")
    else:
        print("备份失败!")