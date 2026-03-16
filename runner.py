import os
from datetime import datetime
from pathlib import Path

from constants import SOURCE_DIR, OUTPUT_DIR, REPORT_FILE, SUPPORTED_EXTENSIONS
from meta_extractor import extract_image_metadata
from renamer import FileRenamer
from organizer import FileOrganizer


class ImageProcessor:
    def __init__(self):
        self.source_dir = Path(SOURCE_DIR)
        self.output_dir = Path(OUTPUT_DIR)
        self.report_file = REPORT_FILE
        self.renamer = FileRenamer()
        self.organizer = FileOrganizer()
        self.processing_log = []
        self.has_errors = False
        self.total_files = 0
        self.processed_count = 0
        self.skipped_count = 0

    def run(self):
        print("开始图像处理...")
        
        self._validate_source_directory()
        
        image_files = self._scan_source_directory()
        self.total_files = len(image_files)
        
        if self.total_files == 0:
            print("未找到支持的图像文件。")
            return

        print(f"找到 {self.total_files} 个图像文件")
        
        self.organizer.initialize_output_directory()
        
        for file_path in image_files:
            self._process_single_file(file_path)

        self._generate_report()
        
        print(f"\n处理完成!")
        print(f"成功: {self.processed_count}, 跳过: {self.skipped_count}")
        print(f"报告已保存至: {self.report_file}")

    def _validate_source_directory(self):
        if not self.source_dir.exists():
            raise FileNotFoundError(f"源目录不存在: {self.source_dir}")

    def _scan_source_directory(self) -> list:
        image_files = []
        if self.source_dir.exists():
            for file_path in self.source_dir.iterdir():
                if file_path.is_file():
                    ext = file_path.suffix.lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        image_files.append(str(file_path))
        return sorted(image_files)

    def _process_single_file(self, file_path: str):
        metadata = extract_image_metadata(file_path)
        metadata["file_path"] = file_path
        
        if not metadata.get("is_valid", False):
            self.skipped_count += 1
            self._log_entry(file_path, None, None, "不支持的文件格式", False)
            return

        new_name = self.renamer.generate_new_name(metadata)
        
        if not new_name:
            self.skipped_count += 1
            self._log_entry(file_path, None, None, "生成文件名失败", False)
            return

        date_taken = metadata.get("date_taken", "")
        is_success = self.organizer.organize_file(file_path, new_name, date_taken)

        if is_success:
            self.processed_count += 1
            self._log_entry(file_path, new_name, date_taken, "成功", True)
        else:
            self.has_errors = True
            self.skipped_count += 1
            self._log_entry(file_path, new_name, date_taken, "移动文件失败", False)

    def _log_entry(self, original_path: str, new_name: str, date_taken: str, status: str, is_success: bool):
        self.processing_log.append({
            "original_path": original_path,
            "new_name": new_name or "N/A",
            "date_taken": date_taken or "N/A",
            "status": status,
            "is_success": is_success
        })

    def _generate_report(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines = [
            "# 图像处理报告\n",
            f"\n生成时间: {timestamp}\n",
            f"\n## 统计信息\n",
            f"\n- 总文件数: {self.total_files}",
            f"- 成功处理: {self.processed_count}",
            f"- 跳过/失败: {self.skipped_count}",
            f"\n## 处理详情\n",
            "\n| 原始路径 | 新文件名 | 拍摄日期 | 状态 | 结果 |",
            "|----------|----------|----------|------|------|"
        ]

        for entry in self.processing_log:
            original = Path(entry["original_path"]).name
            new_name = entry["new_name"]
            date = entry["date_taken"]
            status = entry["status"]
            result = "成功" if entry["is_success"] else "失败"
            
            lines.append(f"| {original} | {new_name} | {date} | {status} | {result} |")

        with open(self.report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main():
    processor = ImageProcessor()
    processor.run()


if __name__ == "__main__":
    main()
