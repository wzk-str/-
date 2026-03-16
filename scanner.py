from pathlib import Path
from typing import List
import settings


def scan_directory() -> List[Path]:
    target_files = []
    input_path = settings.INPUT_DIR.resolve()
    
    if not input_path.exists():
        return target_files
    
    for file_path in input_path.iterdir():
        if file_path.is_file():
            if file_path.name == settings.LOCK_FILE_NAME:
                continue
            
            if file_path.suffix.lower() in settings.VALID_EXTENSIONS:
                target_files.append(file_path)
    
    return target_files


def read_file_content(file_path: Path) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except (IOError, UnicodeDecodeError):
        return []
