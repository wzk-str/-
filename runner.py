from pathlib import Path
from datetime import datetime
from constants import SOURCE_DIR, OUTPUT_DIR, REPORT_FILE, ALLOWED_EXTENSIONS
from meta_extractor import extract_metadata
from renamer import generate_new_filename, rename_file
from organizer import get_date_folder_name, create_target_directory, move_file


def scan_source_directory() -> list:
    image_files = []
    if SOURCE_DIR.exists():
        for file in SOURCE_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in ALLOWED_EXTENSIONS:
                image_files.append(file)
    return image_files


def generate_report(results: list) -> None:
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# 图像处理报告\n\n")
        f.write("| 原始文件名 | 新文件名 | 目标目录 | 状态 |\n")
        f.write("|-----------|----------|----------|------|\n")
        for result in results:
            f.write(f"| {result['original_name']} | {result['new_name']} | {result['target_dir']} | {result['status']} |\n")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    
    image_files = scan_source_directory()
    results = []
    
    for file_path in image_files:
        result = {
            "original_name": file_path.name,
            "new_name": "",
            "target_dir": "",
            "status": "成功"
        }
        
        try:
            metadata = extract_metadata(file_path)
            
            new_filename = generate_new_filename(file_path, metadata)
            renamed_path = rename_file(file_path, new_filename)
            
            date_folder = get_date_folder_name(metadata.get("date_taken"))
            target_dir = create_target_directory(OUTPUT_DIR, date_folder)
            
            final_path = move_file(renamed_path, target_dir)
            
            result["new_name"] = final_path.name
            result["target_dir"] = date_folder
        except Exception as e:
            result["status"] = f"失败: {str(e)}"
        
        results.append(result)
    
    generate_report(results)
    print(f"处理完成! 共处理 {len(results)} 个文件。")
    print(f"报告已生成: {REPORT_FILE}")


if __name__ == "__main__":
    main()
