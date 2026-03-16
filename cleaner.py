"""
cleaner.py - 包含核心数据清洗算法
"""
import re
from datetime import datetime
from typing import List, Dict, Any
import settings


def format_timestamp(line: str) -> str:
    """
    格式化行中的时间戳。
    尝试识别常见时间戳格式并统一格式化。
    
    Args:
        line: 输入行
        
    Returns:
        格式化后的行
    """
    # 常见时间戳模式
    timestamp_patterns = [
        # ISO 8601: 2024-01-15T10:30:00
        (r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),
        # 标准格式: 2024-01-15 10:30:00
        (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', '%Y-%m-%d %H:%M:%S'),
        # 斜杠格式: 2024/01/15 10:30:00
        (r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', '%Y/%m/%d %H:%M:%S'),
    ]
    
    for pattern, fmt in timestamp_patterns:
        match = re.search(pattern, line)
        if match:
            try:
                original = match.group(0)
                if 'T' in original:
                    dt = datetime.strptime(original, '%Y-%m-%dT%H:%M:%S')
                elif '/' in original:
                    dt = datetime.strptime(original, '%Y/%m/%d %H:%M:%S')
                else:
                    dt = datetime.strptime(original, '%Y-%m-%d %H:%M:%S')
                formatted = dt.strftime(settings.TIMESTAMP_FORMAT)
                line = line.replace(original, formatted)
            except ValueError:
                pass
    
    return line


def should_skip_line(line: str) -> bool:
    """
    判断是否应该跳过该行。
    
    规则：
    1. 空行（去除空白后为空）
    2. 包含 "DEBUG" 的行
    
    Args:
        line: 输入行
        
    Returns:
        如果应该跳过返回 True，否则返回 False
    """
    # 检查空行
    if settings.SKIP_EMPTY_LINES and line.strip() == "":
        return True
    
    # 检查 DEBUG 行
    if settings.SKIP_DEBUG_LINES and settings.DEBUG_KEYWORD in line:
        return True
    
    return False


def clean_line(line: str) -> str:
    """
    清洗单行数据。
    
    Args:
        line: 输入行
        
    Returns:
        清洗后的行
    """
    # 格式化时间戳
    line = format_timestamp(line)
    
    # 去除行尾换行符和多余空白
    line = line.rstrip('\n\r')
    
    return line


def process_file_content(file_path: str, lines: List[str]) -> List[Dict[str, Any]]:
    """
    处理文件内容，返回清洗后的结构化数据。
    
    Args:
        file_path: 源文件路径
        lines: 文件内容行列表
        
    Returns:
        清洗后的结构化数据列表，每个元素是一个字典
    """
    cleaned_records: List[Dict[str, Any]] = []
    line_number = 0
    
    for line in lines:
        line_number += 1
        
        # 检查是否需要跳过
        if should_skip_line(line):
            continue
        
        # 清洗行
        cleaned_line = clean_line(line)
        
        # 如果清洗后为空，跳过
        if cleaned_line.strip() == "":
            continue
        
        record = {
            "source_file": file_path,
            "line_number": line_number,
            "content": cleaned_line,
            "timestamp": datetime.now().strftime(settings.TIMESTAMP_FORMAT)
        }
        
        cleaned_records.append(record)
    
    return cleaned_records
