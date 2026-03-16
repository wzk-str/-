from pathlib import Path

SOURCE_DIR = Path("./assets/source/")
OUTPUT_DIR = Path("./assets/sorted/")
REPORT_FILE = Path("process_report.md")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
DATE_FORMAT = "%Y%m%d"
FILENAME_TEMPLATE = "{date}_{camera}_{original}.{ext}"
