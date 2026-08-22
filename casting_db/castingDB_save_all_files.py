"""Scans the entire Casting DB media directory and saves metadata for every file (excluding known junk files) to a CSV.
Outputs filename, user-ID, path, file type, copy date/time, and size in MB for the full inventory."""

import os
import csv
import re
import datetime
import time
import sys
from pathlib import Path

# Add project root to path 
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.config import config

# Paths loaded dynamically from config.json
search_dir = config["CASTING_MEDIA_DIR"]
# search_dir = config["TEST_MEDIA_DIR"]
black_list = ["Thumbs.db", "FNAM", ".DS_Store"]
today = datetime.date.today().strftime("%Y_%m_%d")

output_path = config["NAS_TRANSFER_SHARE"] + r'\Personen\user'
csv_file = f"castingDB_inventory_all_files_{today}.csv"

start = time.time()
results = []
total_size = 0
searched_files_counter = 0
found_files_counter = 0

print(f"Suche alle Dateien aus der Casting Datenbank...")

def find_id(path):
    parts = path.split(os.sep)
    for part in parts:
        if re.fullmatch(r"\d{5,6}", part):
            return part
    return ""

for root, dirs, files in os.walk(search_dir):
    for file in files:
        searched_files_counter += 1
        try:
            file_path = os.path.join(root, file)
            copy_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

            if str(file) not in black_list:
                filetype = os.path.splitext(file)[1].lower()
                filesize_bytes = os.path.getsize(file_path)
                total_size += filesize_bytes
                id = find_id(file_path)

                results.append([
                    file,
                    id,
                    file_path,
                    filetype,
                    copy_date.strftime("%Y_%m_%d"),
                    copy_date.strftime("%H:%M:%S"),
                    round(filesize_bytes / (1024 * 1024), 2)
                ])
                found_files_counter += 1
        except (PermissionError, FileNotFoundError):
            continue

        if searched_files_counter % 1000 == 0:
            now = datetime.datetime.now()
            print(f"{now.strftime("%d.%m.%Y %H:%M:%S")} | Durchsuchte Dateien: {searched_files_counter} | Gefunden: {found_files_counter}")

with open(os.path.join(output_path, csv_file), mode='w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Dateiname", "ID", "Dateipfad", "Dateityp", "Kopierdatum", "Kopierzeit", "Größe (MB)"])
    writer.writerows(results)

endtime = time.time()
duration = int(endtime - start)
hours, rest = divmod(duration, 3600)
mins, secs = divmod(rest, 60)
str_dur = f"{hours:02}:{mins:02}:{secs:02}"

print("\nFertig!")
print(f"{found_files_counter} Dateien in gefunden.")
print(f"Gesamtgröße: {round(total_size / (1024 * 1024 * 1024), 2)} GB")
print(f"Ergebnisse gespeichert in: {output_path + csv_file}")
print(f"Die Suche hat {str_dur} gedauert.")