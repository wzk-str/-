import re
from datetime import datetime
from typing import List, Dict, Any
import settings


def remove_empty_lines(lines: List[str]) -> List[str]:
    return [line for line in lines if line.strip()]


def filter_debug_lines(lines: List[str]) -> List[str]:
    return [
        line for line in lines
        if not any(keyword in line for keyword in settings.FILTER_KEYWORDS)
    ]


def format_timestamp(line: str) -> str:
    timestamp_patterns = [
        (r'\b(\d{4}-\d{2}-\d{2})\b', '%Y-%m-%d'),
        (r'\b(\d{4}/\d{2}/\d{2})\b', '%Y/%m/%d'),
        (r'\b(\d{2}-\d{2}-\d{4})\b', '%m-%d-%Y'),
        (r'\b(\d{2}/\d{2}/\d{4})\b', '%m/%d/%Y'),
    ]
    
    for pattern, date_format in timestamp_patterns:
        match = re.search(pattern, line)
        if match:
            try:
                original_date = match.group(1)
                parsed_date = datetime.strptime(original_date, date_format)
                iso_format = parsed_date.isoformat()
                line = line.replace(original_date, iso_format)
            except ValueError:
                pass
    
    return line


def clean_lines(lines: List[str]) -> List[str]:
    lines = remove_empty_lines(lines)
    lines = filter_debug_lines(lines)
    lines = [format_timestamp(line) for line in lines]
    return lines


def convert_to_jsonl_entry(line: str, source_file: str, line_number: int) -> Dict[str, Any]:
    return {
        "source": source_file,
        "line_number": line_number,
        "content": line.strip(),
        "processed_at": datetime.now().isoformat()
    }
