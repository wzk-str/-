import os
import shutil
from typing import List, Dict, Any
from constants import OUTPUT_DIR


class Organizer:
    
    def __init__(self):
        self.has_created_dirs = False
        self._processed_files: List[Dict[str, Any]] = []
    
    def create_date_folder(self, date_str: str) -> str:
        folder_path = os.path.join(OUTPUT_DIR, date_str)
        folder_path = os.path.normpath(folder_path)
        
        os.makedirs(folder_path, exist_ok=True)
        self.has_created_dirs = True
        
        return folder_path
    
    def move_file(self, source_path: str, target_path: str) -> bool:
        is_success = False
        
        try:
            if os.path.exists(target_path):
                base, ext = os.path.splitext(target_path)
                counter = 1
                while os.path.exists(target_path):
                    target_path = f"{base}_{counter}{ext}"
                    counter += 1
            
            shutil.move(source_path, target_path)
            is_success = True
        except (OSError, shutil.Error):
            is_success = False
        
        return is_success
    
    def record_processing(self, record: Dict[str, Any]) -> None:
        self._processed_files.append(record)
    
    def get_processed_files(self) -> List[Dict[str, Any]]:
        return self._processed_files
