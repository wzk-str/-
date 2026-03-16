import os
from typing import Dict, Any, Optional
from constants import FILENAME_PATTERN, OUTPUT_DIR


class Renamer:
    
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata
        self._new_filename: Optional[str] = None
    
    def generate_new_filename(self) -> str:
        if not self.metadata:
            return ""
        
        date = self.metadata.get("date", "nodate")
        camera = self.metadata.get("camera", "unknown")
        original = self.metadata.get("original_name", "unknown")
        ext = self.metadata.get("extension", "")
        
        new_name = FILENAME_PATTERN.format(
            date=date,
            camera=camera,
            original=original,
            ext=ext
        )
        
        self._new_filename = new_name
        return new_name
    
    def get_target_path(self, date_folder: str) -> Optional[str]:
        if not self._new_filename:
            return None
        
        target_dir = os.path.join(OUTPUT_DIR, date_folder)
        target_path = os.path.join(target_dir, self._new_filename)
        
        return os.path.normpath(target_path)
    
    def has_valid_metadata(self) -> bool:
        return bool(self.metadata)
    
    def get_new_filename(self) -> Optional[str]:
        return self._new_filename
