from pathlib import Path
from settings import INPUT_DIR, ALLOWED_EXTENSIONS, FORBIDDEN_FILE

def scan_log_files():
    valid_files = []
    if not INPUT_DIR.exists():
        return valid_files
    
    for item in INPUT_DIR.iterdir():
        if item.name == FORBIDDEN_FILE:
            continue
        if not item.is_file():
            continue
        if item.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        valid_files.append(item)
    
    return valid_files
