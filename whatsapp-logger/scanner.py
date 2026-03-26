import os
import time
from datetime import datetime

def get_modified_files(folder_path):
    try:
        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                modification_time = os.path.getmtime(file_path)
                last_scan_time = getattr(getattr(scanner, 'last_scan_time', {}), filename, 0)

                if modification_time > last_scan_time:
                    files.append((file_path, filename, modification_time))
                    scanner.last_scan_time[filename] = modification_time

        return files
    except Exception as e:
        print(f"Error scanning folder: {e}")
        return []

# Initialize the module with a dummy value
scanner = {'last_scan_time': {}}