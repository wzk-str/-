"""
scanner.py - 负责遍历目录并识别目标文件
"""
from pathlib import Path
from typing import List
import settings


def scan_input_directory() -> List[Path]:
    """
    扫描输入目录，返回所有符合条件的文件路径列表。
    
    规则：
    1. 仅处理扩展名为 .log 和 .txt 的文件
    2. 跳过名为 system.lock 的文件（不读取、不修改、不移动、不删除）
    3. 如果目录不存在，返回空列表
    
    Returns:
        List[Path]: 符合条件的文件路径列表
    """
    target_files: List[Path] = []
    input_dir = settings.INPUT_DIR
    
    if not input_dir.exists():
        return target_files
    
    if not input_dir.is_dir():
        return target_files
    
    for item in input_dir.iterdir():
        if not item.is_file():
            continue
        
        # 显式检查并跳过 system.lock 文件
        if item.name == settings.LOCK_FILE:
            continue
        
        # 检查文件扩展名
        if item.suffix.lower() in settings.VALID_EXTENSIONS:
            target_files.append(item)
    
    return target_files
