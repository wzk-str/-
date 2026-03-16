import json
from pathlib import Path
from typing import List, Dict, Any
import settings


def ensure_output_directory() -> None:
    output_path = settings.OUTPUT_DIR.resolve()
    output_path.mkdir(parents=True, exist_ok=True)


def generate_output_filename(source_file: Path) -> Path:
    output_dir = settings.OUTPUT_DIR.resolve()
    base_name = source_file.stem
    output_filename = f"{base_name}_archived{settings.OUTPUT_FILE_EXTENSION}"
    return output_dir / output_filename


def write_jsonl(file_path: Path, entries: List[Dict[str, Any]]) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        return True
    except IOError:
        return False


def archive_entries(entries: List[Dict[str, Any]], source_file: Path) -> bool:
    if not entries:
        return False
    
    ensure_output_directory()
    output_path = generate_output_filename(source_file)
    return write_jsonl(output_path, entries)
