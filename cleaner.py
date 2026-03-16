import re
from datetime import datetime
from settings import FILTER_KEYWORD, TIMESTAMP_FORMAT

def format_timestamp(line):
    timestamp_pattern = r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}'
    match = re.search(timestamp_pattern, line)
    if match:
        try:
            ts = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
            formatted_ts = ts.strftime(TIMESTAMP_FORMAT)
            line = line[:match.start()] + formatted_ts + line[match.end():]
        except ValueError:
            pass
    return line

def clean_line(line):
    stripped = line.strip()
    if not stripped:
        return None
    if FILTER_KEYWORD in stripped:
        return None
    cleaned = format_timestamp(stripped)
    return cleaned

def clean_file(file_path):
    cleaned_lines = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            cleaned = clean_line(line)
            if cleaned:
                cleaned_lines.append({
                    "content": cleaned,
                    "source_file": file_path.name
                })
    return cleaned_lines
