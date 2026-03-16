"""
settings.py - 定义所有常量、路径和规则
"""
from pathlib import Path

# 输入目录 - 相对路径 ./logs/raw/
INPUT_DIR = Path("./logs/raw/")

# 输出归档目录 - 相对路径 ./logs/archive/
ARCHIVE_DIR = Path("./logs/archive/")

# 支持的文件扩展名
VALID_EXTENSIONS = {".log", ".txt"}

# 归档报告文件格式
ARCHIVE_FORMAT = ".jsonl"

# 需要跳过的特殊文件
LOCK_FILE = "system.lock"

# 清洗规则
SKIP_EMPTY_LINES = True
SKIP_DEBUG_LINES = True
DEBUG_KEYWORD = "DEBUG"

# 时间戳格式化（示例格式）
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
