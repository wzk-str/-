from pathlib import Path
import scanner
import cleaner
import archiver


def process_file(file_path: Path) -> bool:
    raw_lines = scanner.read_file_content(file_path)
    if not raw_lines:
        return False
    
    cleaned_lines = cleaner.clean_lines(raw_lines)
    
    entries = []
    for idx, line in enumerate(cleaned_lines, start=1):
        entry = cleaner.convert_to_jsonl_entry(line, file_path.name, idx)
        entries.append(entry)
    
    return archiver.archive_entries(entries, file_path)


def main():
    target_files = scanner.scan_directory()
    
    processed_count = 0
    skipped_count = 0
    
    for file_path in target_files:
        if process_file(file_path):
            processed_count += 1
        else:
            skipped_count += 1
    
    print(f"处理完成: {processed_count} 个文件已归档, {skipped_count} 个文件被跳过")


if __name__ == "__main__":
    main()
