from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_data(file_path: Path) -> dict:
    exif_data = {}
    try:
        with Image.open(file_path) as img:
            raw_exif = img._getexif()
            if raw_exif:
                for tag_id, value in raw_exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[tag] = value
    except Exception:
        pass
    return exif_data


def extract_metadata(file_path: Path) -> dict:
    metadata = {
        "date_taken": None,
        "camera_model": None,
        "has_exif": False
    }
    
    exif_data = get_exif_data(file_path)
    
    if exif_data:
        metadata["has_exif"] = True
        
        date_time_original = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
        if date_time_original:
            try:
                dt = datetime.strptime(str(date_time_original), "%Y:%m:%d %H:%M:%S")
                metadata["date_taken"] = dt
            except ValueError:
                pass
        
        metadata["camera_model"] = exif_data.get("Model")
    
    return metadata
