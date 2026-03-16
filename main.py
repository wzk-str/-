"""
main.py - 程序入口，负责协调流程

本地日志归档与清洗系统
- 扫描 ./logs/raw/ 目录下的 .log 和 .txt 文件
- 清洗数据：去除空行、格式化时间戳、过滤 DEBUG 行
- 归档到 ./logs/archive/ 目录的 .jsonl 文件
- 完全跳过 system.lock 文件（不读取、不修改、不移动、不删除）
"""
import sys
from pathlib import Path
from typing import List, Dict, Any

import settings
import scanner
import cleaner
import archiver


def read_file_lines(file_path: Path) -> List[str]:
    """
    读取文件的所有行。
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容行列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except UnicodeDecodeError:
        # 尝试使用其他编码
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.readlines()
    except Exception as e:
        print(f"警告: 无法读取文件 {file_path}: {e}")
        return []


def process_files(file_paths: List[Path]) -> List[Dict[str, Any]]:
    """
    处理所有文件，返回清洗后的记录。
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        所有清洗后的记录
    """
    all_records: List[Dict[str, Any]] = []
    
    for file_path in file_paths:
        print(f"正在处理: {file_path.name}")
        
        lines = read_file_lines(file_path)
        if not lines:
            print(f"  - 文件为空或无法读取")
            continue
        
        records = cleaner.process_file_content(str(file_path), lines)
        all_records.extend(records)
        print(f"  - 提取 {len(records)} 条记录")
    
    return all_records


def main() -> int:
    """
    主函数，协调整个日志归档与清洗流程。
    
    Returns:
        退出码 (0 表示成功)
    """
    print("=" * 50)
    print("本地日志归档与清洗系统")
    print("=" * 50)
    
    # 步骤 1: 扫描输入目录
    print(f"\n[1/4] 扫描输入目录: {settings.INPUT_DIR}")
    
    target_files = scanner.scan_input_directory()
    
    if not target_files:
        print("未找到符合条件的文件 (.log 或 .txt)")
        print(f"请确保 {settings.INPUT_DIR} 目录存在且包含目标文件")
        return 0
    
    print(f"找到 {len(target_files)} 个目标文件:")
    for f in target_files:
        print(f"  - {f.name}")
    
    # 步骤 2: 读取并清洗数据
    print(f"\n[2/4] 读取并清洗数据...")
    all_records = process_files(target_files)
    print(f"总计提取 {len(all_records)} 条有效记录")
    
    if not all_records:
        print("没有有效记录需要归档")
        return 0
    
    # 步骤 3: 归档数据
    print(f"\n[3/4] 归档数据到: {settings.ARCHIVE_DIR}")
    archive_path = archiver.archive_records(all_records)
    print(f"归档文件: {archive_path.name}")
    
    # 步骤 4: 生成摘要报告
    print(f"\n[4/4] 生成摘要报告...")
    summary = archiver.create_summary_report(
        total_files=len(target_files),
        total_records=len(all_records),
        archive_path=archive_path
    )
    
    print("\n" + "=" * 50)
    print("处理完成!")
    print("=" * 50)
    print(f"处理文件数: {summary['total_files_processed']}")
    print(f"归档记录数: {summary['total_records_archived']}")
    print(f"归档文件: {summary['archive_file']}")
    print(f"状态: {summary['status']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
