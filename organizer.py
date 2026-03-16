import os
import shutil
from pathlib import Path

from constants import OUTPUT_DIR


class FileOrganizer:
    def __init__(self):
        self.output_base = Path(OUTPUT_DIR)
        self.is_initialized = False
        self.processed_files = []
        self.failed_files = []

    def initialize_output_directory(self):
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.is_initialized = True

    def organize_file(self, source_path: str, new_file_name: str, date_taken: str) -> bool:
        if not self.is_initialized:
            self.initialize_output_directory()

        try:
            date_folder = self._get_date_folder(date_taken)
            target_dir = self.output_base / date_folder
            target_dir.mkdir(parents=True, exist_ok=True)

            target_path = target_dir / new_file_name

            counter = 1
            original_target = target_path
            while target_path.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = original_target.parent / f"{stem}_{counter:03d}{suffix}"
                counter += 1

            shutil.move(source_path, target_path)
            
            self.processed_files.append({
                "source": source_path,
                "target": str(target_path),
                "is_success": True
            })
            
            return True

        except Exception as e:
            self.failed_files.append({
                "source": source_path,
                "error": str(e),
                "is_success": False
            })
            return False

    def _get_date_folder(self, date_taken: str) -> str:
        if date_taken and len(date_taken) == 8:
            year = date_taken[:4]
            month = date_taken[4:6]
            day = date_taken[6:8]
            return f"{year}-{month}-{day}"
        return "unknown_date"

    def get_organization_summary(self) -> dict:
        return {
            "total_processed": len(self.processed_files),
            "total_failed": len(self.failed_files),
            "processed_files": self.processed_files,
            "failed_files": self.failed_files
        }


def organize_single_file(source_path: str, new_file_name: str, date_taken: str) -> bool:
    organizer = FileOrganizer()
    return organizer.organize_file(source_path, new_file_name, date_taken)


def batch_organize_files(file_mappings: list) -> dict:
    organizer = FileOrganizer()
    
    for mapping in file_mappings:
        source_path = mapping.get("source_path", "")
        new_name = mapping.get("new_name", "")
        date_taken = mapping.get("date_taken", "")
        
        if source_path and new_name:
            organizer.organize_file(source_path, new_name, date_taken)
    
    return organizer.get_organization_summary()
