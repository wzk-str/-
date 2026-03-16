from pathlib import Path
from datetime import datetime

INPUT_DIR = Path("./logs/raw/")
OUTPUT_DIR = Path("./logs/archive/")

ALLOWED_EXTENSIONS = {".log", ".txt"}
FORBIDDEN_FILE = "system.lock"

FILTER_KEYWORD = "DEBUG"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_archive_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"cleaned_logs_{timestamp}.jsonl"
