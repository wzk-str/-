#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Processor - 高质量Python代码示例

一个多功能文本处理工具，支持多种文本转换和分析操作。

:author: Python Developer
:date: 2024-01-01
:version: 1.0.0
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from typing import Dict, List, Optional, Tuple, Union


def count_words(text: str) -> int:
    """
    统计文本中的单词数量。

    Args:
        text: 输入文本字符串

    Returns:
        单词数量

    Raises:
        TypeError: 如果text不是字符串类型
    """
    if not isinstance(text, str):
        raise TypeError("text参数必须是字符串类型")
    
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def count_characters(text: str, include_spaces: bool = True) -> int:
    """
    统计文本中的字符数量。

    Args:
        text: 输入文本字符串
        include_spaces: 是否包含空格，默认为True

    Returns:
        字符数量

    Raises:
        TypeError: 如果text不是字符串类型
    """
    if not isinstance(text, str):
        raise TypeError("text参数必须是字符串类型")
    
    if include_spaces:
        return len(text)
    return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))


def get_word_frequency(text: str, 
                        top_n: Optional[int] = None,
                        case_sensitive: bool = False) -> Dict[str, int]:
    """
    获取文本中单词的频率统计。

    Args:
        text: 输入文本字符串
        top_n: 返回前N个高频词，None表示返回全部
        case_sensitive: 是否区分大小写，默认为False

    Returns:
        单词频率字典，键为单词，值为出现次数

    Raises:
        TypeError: 如果text不是字符串类型
        ValueError: 如果top_n小于0
    """
    if not isinstance(text, str):
        raise TypeError("text参数必须是字符串类型")
    if top_n is not None and top_n < 0:
        raise ValueError("top_n不能小于0")
    
    if not case_sensitive:
        text = text.lower()
    
    words = re.findall(r'\b\w+\b', text)
    word_counts = Counter(words)
    
    if top_n is not None:
        return dict(word_counts.most_common(top_n))
    return dict(word_counts)


def transform_text(text: str, 
                   operation: str,
                   **kwargs) -> str:
    """
    对文本进行转换操作。

    Args:
        text: 输入文本字符串
        operation: 转换操作类型，可选值：
            - 'upper': 转换为大写
            - 'lower': 转换为小写
            - 'title': 转换为标题格式
            - 'capitalize': 首字母大写
            - 'reverse': 反转文本
            - 'remove_duplicates': 移除连续重复字符

    Returns:
        转换后的文本

    Raises:
        ValueError: 如果operation不是支持的操作类型
    """
    operations = {
        'upper': str.upper,
        'lower': str.lower,
        'title': str.title,
        'capitalize': str.capitalize,
        'reverse': lambda t: t[::-1],
        'remove_duplicates': _remove_consecutive_duplicates
    }
    
    if operation not in operations:
        supported = ', '.join(operations.keys())
        raise ValueError(f"不支持的操作: {operation}。支持的操作: {supported}")
    
    return operations[operation](text)


def _remove_consecutive_duplicates(text: str) -> str:
    """移除连续重复的字符。"""
    if not text:
        return text
    
    result = [text[0]]
    for char in text[1:]:
        if char != result[-1]:
            result.append(char)
    return ''.join(result)


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """
    读取文件内容。

    Args:
        file_path: 文件路径
        encoding: 文件编码，默认为utf-8

    Returns:
        文件内容字符串

    Raises:
        FileNotFoundError: 文件不存在
        PermissionError: 权限不足
        IsADirectoryError: 路径是目录而不是文件
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if os.path.isdir(file_path):
        raise IsADirectoryError(f"路径是目录: {file_path}")
    
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        return f.read()


def write_file(content: str, 
               file_path: str, 
               encoding: str = 'utf-8',
               overwrite: bool = False) -> None:
    """
    写入内容到文件。

    Args:
        content: 要写入的内容
        file_path: 输出文件路径
        encoding: 文件编码，默认为utf-8
        overwrite: 是否覆盖已存在的文件

    Raises:
        FileExistsError: 文件已存在且overwrite为False
        PermissionError: 权限不足
    """
    if os.path.exists(file_path) and not overwrite:
        raise FileExistsError(f"文件已存在: {file_path}。使用--overwrite参数覆盖")
    
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)


def analyze_text(text: str) -> Dict[str, Union[int, Dict[str, int]]]:
    """
    综合分析文本信息。

    Args:
        text: 输入文本字符串

    Returns:
        包含分析结果的字典
    """
    return {
        'word_count': count_words(text),
        'char_count_with_spaces': count_characters(text, include_spaces=True),
        'char_count_without_spaces': count_characters(text, include_spaces=False),
        'line_count': len(text.splitlines()) if text else 0,
        'top_words': get_word_frequency(text, top_n=5)
    }


def main() -> int:
    """主入口函数。"""
    parser = argparse.ArgumentParser(
        description='文本处理工具 - 支持文本分析和转换',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''使用示例:
  # 分析文本文件
  python text_processor.py analyze input.txt

  # 转换文本为大写
  python text_processor.py transform input.txt -o output.txt --op upper

  # 从标准输入读取
  echo "Hello World" | python text_processor.py analyze -

  # 输出JSON格式
  python text_processor.py analyze input.txt --json
'''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # analyze子命令
    analyze_parser = subparsers.add_parser('analyze', help='分析文本信息')
    analyze_parser.add_argument('input', help='输入文件路径，使用"-"表示标准输入')
    analyze_parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    analyze_parser.add_argument('--encoding', default='utf-8', help='文件编码，默认utf-8')
    
    # transform子命令
    transform_parser = subparsers.add_parser('transform', help='转换文本')
    transform_parser.add_argument('input', help='输入文件路径，使用"-"表示标准输入')
    transform_parser.add_argument('-o', '--output', help='输出文件路径，默认输出到控制台')
    transform_parser.add_argument('--op', required=True, 
                                  choices=['upper', 'lower', 'title', 'capitalize', 'reverse', 'remove_duplicates'],
                                  help='转换操作类型')
    transform_parser.add_argument('--encoding', default='utf-8', help='文件编码，默认utf-8')
    transform_parser.add_argument('--overwrite', action='store_true', help='覆盖已存在的输出文件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        # 读取输入
        if args.input == '-':
            text = sys.stdin.read()
        else:
            text = read_file(args.input, args.encoding)
        
        # 执行命令
        if args.command == 'analyze':
            result = analyze_text(text)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("=== 文本分析结果 ===")
                print(f"单词数量: {result['word_count']}")
                print(f"字符数量(含空格): {result['char_count_with_spaces']}")
                print(f"字符数量(不含空格): {result['char_count_without_spaces']}")
                print(f"行数: {result['line_count']}")
                print("\n高频词:")
                for word, count in result['top_words'].items():
                    print(f"  {word}: {count}")
        
        elif args.command == 'transform':
            result = transform_text(text, args.op)
            if args.output:
                write_file(result, args.output, args.encoding, args.overwrite)
                print(f"转换完成，结果已保存到: {args.output}")
            else:
                print(result)
        
        return 0
    
    except (FileNotFoundError, PermissionError, IsADirectoryError, 
            FileExistsError, ValueError, TypeError) as e:
        print(f"错误: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"未知错误: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
