from PIL import Image
from PIL.ExifTags import TAGS
import os
from typing import Optional, Dict, Any
from constants import ALLOWED_EXTENSIONS


class MetaExtractor:
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.is_valid = self._check_extension()
        self._metadata: Optional[Dict[str, Any]] = None
    
    def _check_extension(self) -> bool:
        ext = os.path.splitext(self.file_path)[1].lower()
        return ext in ALLOWED_EXTENSIONS
    
    def _get_exif_data(self) -> Dict[str, Any]:
        exif_data = {}
        try:
            with Image.open(self.file_path) as img:
                raw_exif = img._getexif()
                if raw_exif:
                    for tag_id, value in raw_exif.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        exif_data[tag_name] = value
        except (AttributeError, OSError, ValueError):
            pass
        return exif_data
    
    def extract_metadata(self) -> Dict[str, Any]:
        if not self.is_valid:
            return {}
        
        exif_data = self._get_exif_data()
        
        date_time = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
        camera_model = exif_data.get("Model")
        
        formatted_date = self._format_date(date_time)
        clean_camera = self._clean_camera_model(camera_model)
        
        self._metadata = {
            "date": formatted_date,
            "camera": clean_camera,
            "original_name": os.path.splitext(os.path.basename(self.file_path))[0],
            "extension": os.path.splitext(self.file_path)[1].lower()
        }
        
        return self._metadata
    
    def _format_date(self, date_time: Optional[str]) -> str:
        if not date_time:
            return "nodate"
        
        try:
            date_part = date_time.split()[0]
            formatted = date_part.replace(":", "")
            return formatted
        except (IndexError, AttributeError):
            return "nodate"
    
    def _clean_camera_model(self, camera_model: Optional[str]) -> str:
        if not camera_model:
            return "unknown"
        
        cleaned = camera_model.strip()
        cleaned = cleaned.replace(" ", "_")
        cleaned = "".join(c for c in cleaned if c.isalnum() or c == "_")
        
        return cleaned if cleaned else "unknown"
    
    def get_metadata(self) -> Optional[Dict[str, Any]]:
        return self._metadata
