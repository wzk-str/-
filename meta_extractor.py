from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import os

from constants import SUPPORTED_EXTENSIONS


class MetadataExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.original_name = os.path.splitext(os.path.basename(file_path))[0]
        self.extension = os.path.splitext(file_path)[1].lower()
        self.is_valid_extension = self.extension in SUPPORTED_EXTENSIONS
        self.date_taken = None
        self.camera_model = None
        self.has_exif = False
        self.is_processed = False

    def extract_metadata(self) -> dict:
        if not self.is_valid_extension:
            return self._get_empty_result()

        try:
            with Image.open(self.file_path) as img:
                exif_data = img._getexif()
                
                if exif_data is not None:
                    self.has_exif = True
                    exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
                    
                    self.date_taken = self._extract_date_taken(exif)
                    self.camera_model = self._extract_camera_model(exif)
                else:
                    self.date_taken = self._get_file_modification_date()
                    self.camera_model = "Unknown"
                
                self.is_processed = True
                
        except Exception:
            self.date_taken = self._get_file_modification_date()
            self.camera_model = "Unknown"
            self.is_processed = True

        return self._get_result()

    def _extract_date_taken(self, exif: dict) -> str:
        date_str = exif.get("DateTimeOriginal") or exif.get("DateTime") or exif.get("DateTimeDigitized")
        
        if date_str:
            try:
                dt = datetime.strptime(str(date_str), "%Y:%m:%d %H:%M:%S")
                return dt.strftime("%Y%m%d")
            except ValueError:
                pass
        
        return self._get_file_modification_date()

    def _extract_camera_model(self, exif: dict) -> str:
        make = exif.get("Make", "").strip()
        model = exif.get("Model", "").strip()
        
        if make and model:
            camera = f"{make}_{model}"
        elif model:
            camera = model
        elif make:
            camera = make
        else:
            camera = "Unknown"
        
        camera = camera.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        return camera

    def _get_file_modification_date(self) -> str:
        try:
            mtime = os.path.getmtime(self.file_path)
            return datetime.fromtimestamp(mtime).strftime("%Y%m%d")
        except OSError:
            return datetime.now().strftime("%Y%m%d")

    def _get_empty_result(self) -> dict:
        return {
            "original_name": self.original_name,
            "extension": self.extension,
            "date_taken": None,
            "camera_model": None,
            "is_valid": False,
            "has_exif": False
        }

    def _get_result(self) -> dict:
        return {
            "original_name": self.original_name,
            "extension": self.extension,
            "date_taken": self.date_taken,
            "camera_model": self.camera_model,
            "is_valid": self.is_valid_extension,
            "has_exif": self.has_exif
        }


def extract_image_metadata(file_path: str) -> dict:
    extractor = MetadataExtractor(file_path)
    return extractor.extract_metadata()
