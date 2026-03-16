from pathlib import Path
import shutil
from constants import DATE_FORMAT


def get_date_folder_name(date_taken) -> str:
    if date_taken:
        return date_taken.strftime(DATE_FORMAT)
    return "UnknownDate"


def create_target_directory(base_dir: Path, folder_name: str) -> Path:
    target_dir = base_dir / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def move_file(source_path: Path, target_dir: Path) -> Path:
    target_path = target_dir / source_path.name
    if target_path.exists():
        stem = source_path.stem
        ext = source_path.suffix
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{stem}_{counter}{ext}"
            counter += 1
    shutil.move(str(source_path), str(target_path))
    return target_path
