from pathlib import Path

INPUT_DIR = Path("./logs/raw/")
OUTPUT_DIR = Path("./logs/archive/")

VALID_EXTENSIONS = {".log", ".txt"}
LOCK_FILE_NAME = "system.lock"
OUTPUT_FILE_EXTENSION = ".jsonl"

FILTER_KEYWORDS = ["DEBUG"]
