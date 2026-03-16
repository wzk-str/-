import os

SOURCE_DIR = os.path.normpath("./assets/source/")
OUTPUT_DIR = os.path.normpath("./assets/sorted/")
REPORT_FILE = os.path.normpath("./process_report.md")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

DATE_FORMAT = "%Y%m%d"
FILENAME_PATTERN = "{date}_{camera}_{original}{ext}"
