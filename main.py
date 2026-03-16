from scanner import scan_log_files
from cleaner import clean_file
from archiver import write_archive

def main():
    print("Starting log cleaning and archiving process...")
    
    files = scan_log_files()
    print(f"Found {len(files)} valid log files")
    
    all_data = []
    for file_path in files:
        print(f"Processing: {file_path.name}")
        cleaned = clean_file(file_path)
        all_data.extend(cleaned)
        print(f"  Extracted {len(cleaned)} valid records")
    
    if all_data:
        output_path = write_archive(all_data)
        print(f"\nArchived {len(all_data)} records to: {output_path}")
    else:
        print("\nNo valid records found to archive")
    
    print("Process completed!")

if __name__ == "__main__":
    main()
