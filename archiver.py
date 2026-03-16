"""
archiver.py - 负责写入归档文件
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import settings


def ensure_archive_dir() -> None:
    """
    确保归档目录存在，如果不存在则创建。
    """
    settings.ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def generate_archive_filename() -> str:
    """
    生成归档文件名，基于当前时间戳。
    
    Returns:
        归档文件名
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"archive_{timestamp}{settings.ARCHIVE_FORMAT}"


def write_jsonl(records: List[Dict[str, Any]], output_path: Path) -> int:
    """
    将记录写入 JSON Lines 文件。
    
    Args:
        records: 要写入的记录列表
        output_path: 输出文件路径
        
    Returns:
        写入的记录数
    """
    count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            json_line = json.dumps(record, ensure_ascii=False)
            f.write(json_line + '\n')
            count += 1
    return count


def archive_records(records: List[Dict[str, Any]]) -> Path:
    """
    将清洗后的记录归档到 JSONL 文件。
    
    Args:
        records: 清洗后的记录列表
        
    Returns:
        归档文件的路径
    """
    ensure_archive_dir()
    
    filename = generate_archive_filename()
    output_path = settings.ARCHIVE_DIR / filename
    
    write_jsonl(records, output_path)
    
    return output_path


def create_summary_report(total_files: int, total_records: int, archive_path: Path) -> Dict[str, Any]:
    """
    创建归档摘要报告。
    
    Args:
        total_files: 处理的文件总数
        total_records: 处理的记录总数
        archive_path: 归档文件路径
        
    Returns:
        摘要报告字典
    """
    return {
        "timestamp": datetime.now().strftime(settings.TIMESTAMP_FORMAT),
        "total_files_processed": total_files,
        "total_records_archived": total_records,
        "archive_file": str(archive_path),
        "status": "success"
    }
