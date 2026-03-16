from pathlib import Path
import re
from constants import FILENAME_TEMPLATE, DATE_FORMAT


def sanitize_camera_model(model: str) -> str:
    if not model:
        return "UnknownCamera"
    cleaned = re.sub(r'[^\w]', '', str(model))
    return cleaned if cleaned else "UnknownCamera"


def generate_new_filename(file_path: Path, metadata: dict) -> str:
    original_name = file_path.stem
    ext = file_path.suffix.lower().lstrip(".")
    
    date_taken = metadata.get("date_taken")
    if date_taken:
        date_str = date_taken.strftime(DATE_FORMAT)
    else:
        date_str = "UnknownDate"
    
    camera_model = sanitize_camera_model(metadata.get("camera_model"))
    
    return FILENAME_TEMPLATE.format(
        date=date_str,
        camera=camera_model,
        original=original_name,
        ext=ext
    )


def rename_file(source_path: Path, new_filename: str) -> Path:
    new_path = source_path.parent / new_filename
    if source_path != new_path:
        counter = 1
        while new_path.exists():
            stem = Path(new_filename).stem
            ext = Path(new_filename).suffix
            new_path = source_path.parent / f"{stem}_{counter}{ext}"
            counter += 1
        source_path.rename(new_path)
    return new_path
