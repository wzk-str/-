import os
from typing import List, Dict, Any
from constants import SOURCE_DIR, OUTPUT_DIR, REPORT_FILE
from meta_extractor import MetaExtractor
from renamer import Renamer
from organizer import Organizer


def scan_source_directory() -> List[str]:
    file_paths = []
    
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR, exist_ok=True)
        return file_paths
    
    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    
    return file_paths


def generate_report(records: List[Dict[str, Any]]) -> None:
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Image Processing Report\n\n")
        f.write("| Original Name | New Name | Date | Camera | Status |\n")
        f.write("|---------------|----------|------|--------|--------|\n")
        
        for record in records:
            original = record.get("original_name", "N/A")
            new_name = record.get("new_name", "N/A")
            date = record.get("date", "N/A")
            camera = record.get("camera", "N/A")
            status = "Success" if record.get("is_success") else "Failed"
            
            f.write(f"| {original} | {new_name} | {date} | {camera} | {status} |\n")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    file_paths = scan_source_directory()
    organizer = Organizer()
    
    for file_path in file_paths:
        extractor = MetaExtractor(file_path)
        
        if not extractor.is_valid:
            continue
        
        metadata = extractor.extract_metadata()
        
        if not metadata:
            continue
        
        renamer = Renamer(metadata)
        new_filename = renamer.generate_new_filename()
        
        date_folder = metadata.get("date", "nodate")
        organizer.create_date_folder(date_folder)
        
        target_path = renamer.get_target_path(date_folder)
        
        if target_path:
            is_success = organizer.move_file(file_path, target_path)
            
            record = {
                "original_name": os.path.basename(file_path),
                "new_name": new_filename,
                "date": metadata.get("date", "nodate"),
                "camera": metadata.get("camera", "unknown"),
                "is_success": is_success
            }
            organizer.record_processing(record)
    
    generate_report(organizer.get_processed_files())
    print(f"Processing complete. Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
