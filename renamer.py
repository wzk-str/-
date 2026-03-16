import os
import re

from constants import FILE_NAME_TEMPLATE


class FileRenamer:
    def __init__(self):
        self.used_names = set()

    def generate_new_name(self, metadata: dict) -> str:
        if not metadata.get("is_valid", False):
            return None

        date_taken = metadata.get("date_taken", "Unknown")
        camera_model = metadata.get("camera_model", "Unknown")
        original_name = metadata.get("original_name", "")
        extension = metadata.get("extension", "")

        safe_camera_model = self._sanitize_string(camera_model)
        safe_original_name = self._sanitize_string(original_name)

        new_name = FILE_NAME_TEMPLATE.format(
            date=date_taken,
            camera_model=safe_camera_model,
            original_name=safe_original_name,
            ext=extension.lower()
        )

        new_name = self._ensure_unique_name(new_name)
        
        return new_name

    def _sanitize_string(self, input_string: str) -> str:
        if not input_string:
            return "Unknown"
        
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', input_string)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')
        
        if not sanitized:
            return "Unknown"
        
        return sanitized

    def _ensure_unique_name(self, file_name: str) -> str:
        if file_name not in self.used_names:
            self.used_names.add(file_name)
            return file_name

        base, ext = os.path.splitext(file_name)
        counter = 1
        
        while True:
            new_name = f"{base}_{counter:03d}{ext}"
            if new_name not in self.used_names:
                self.used_names.add(new_name)
                return new_name
            counter += 1


def generate_new_file_name(metadata: dict) -> str:
    renamer = FileRenamer()
    return renamer.generate_new_name(metadata)


def batch_generate_names(all_metadata: list) -> dict:
    renamer = FileRenamer()
    name_mapping = {}
    
    for metadata in all_metadata:
        original_path = metadata.get("file_path", "")
        if metadata.get("is_valid", False):
            new_name = renamer.generate_new_name(metadata)
            if new_name:
                name_mapping[original_path] = new_name
    
    return name_mapping
