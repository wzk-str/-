import json
from pathlib import Path
from settings import OUTPUT_DIR, get_archive_filename

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write_archive(data):
    ensure_output_dir()
    filename = get_archive_filename()
    output_path = OUTPUT_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    return output_path
