"""Compares a source Casting DB media directory to a converted output directory and reports missing files.
Walks the source tree, builds the expected destination path for each file, and outputs a CSV of all
files not yet present in the converted output, skipping files older than 5 years."""

import os
import re
import csv
import datetime
import time
import sys
from pathlib import Path

# Add project root to path so we can cleanly import our util setup
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.config import config

# Paths loaded dynamically from config.json
SOURCE_ROOT = config["CASTING_MEDIA_DIR"]
DEST_ROOT = config["CASTING_CONVERTED_DIR"]
#SOURCE_ROOT   = config["TEST_MEDIA_DIR"]
#DEST_ROOT   = config["TEST_MEDIA_DIR_OUT"]

OUTPUT_PATH = config["NAS_TRANSFER_SHARE"] + r"\Personen\user\castingDB_diff_files_"
CSV_OUTPUT  = f"{datetime.date.today().strftime('%Y_%m_%d')}.csv"

VIDEO_EXTS = {".mov", ".mp4", ".mxf", ".mts"}
IMG_EXTS   = {".jpg", ".jpeg", ".png", ".webp"}
IGNORE_NAMES = {"Thumbs.db", "FNAM", ".DS_Store"}

MAX_AGE_DAYS = 1827 # ignore files > 5 yars
PROGRESS_INTERVAL = 100

start = time.time()

def get_user_id_padded(path):
    """Sucht im Pfad nach einer 4 bis 6-stelligen Zahl, gibt sie zero-padded als 6-stelligen String zurück."""
    m = re.search(r"[\\/](\d{4,6})[\\/]", path)
    return m.group(1).zfill(6) if m else None

def get_dateityp(ext):
    ext = ext.lower()
    if ext in VIDEO_EXTS:
        return "Videos"
    elif ext in IMG_EXTS:
        return "Bilder"
    else:
        return "Dateien"

def build_dest_path(src_root, file_dir, filename, user_id, dateityp):
    """
    Rekonstruiert anhand des relativen Pfads (unter Berücksichtigung
    evtl. weiterer Unterordner) das Zielverzeichnis.
    """
    # relativer Pfad unter SOURCE_ROOT
    rel = os.path.relpath(file_dir, src_root)
    parts = rel.split(os.sep)
    # numeric folder auf 6-stellige ID ersetzen
    new_parts = [p.zfill(6) if re.fullmatch(r"\d{4,6}", p) else p for p in parts]
    # Zielpfad: DEST_ROOT / new_parts... / dateityp
    dest_dir = os.path.join(DEST_ROOT, *new_parts, dateityp)
    # Zielfilename: originalname_UserID.ext
    name, ext = os.path.splitext(filename)
    dest_file = os.path.join(dest_dir, f"{user_id}_{name}{ext.lower()}")
    return dest_file

def scan_and_report():
    rows = []
    total_files = 0
    found_diffs = 0
    total_size = 0
    now = datetime.datetime.now()

    for root, dirs, files in os.walk(SOURCE_ROOT):
        for fn in files:
            total_files += 1

            try:
                if fn in IGNORE_NAMES:
                    continue

                full_src = os.path.join(root, fn)
                st = os.stat(full_src)
                ts_created = os.path.getctime(full_src)
                created = datetime.datetime.fromtimestamp(ts_created)

                # skip if file has no user_id
                user_id_padded = get_user_id_padded(full_src)
                if not user_id_padded:
                    continue

                user_id = user_id_padded.lstrip("0")
                filename, _ = os.path.splitext(user_id)
                # skip if file is older than MAX_AGE_DAYS and filename is not user_id (file is not profile picture)
                #if (now - created).days > MAX_AGE_DAYS and filename != user_id:
                if (now - created).days > MAX_AGE_DAYS:
                    continue

                # build destination path
                _, ext = os.path.splitext(fn)
                dateityp = get_dateityp(ext)
                dest_file = build_dest_path(SOURCE_ROOT, root, fn, user_id_padded, dateityp)

                if not os.path.exists(dest_file):
                    size_mb = round(st.st_size / (1024 * 1024), 2)
                    total_size += size_mb
                    found_diffs += 1
                    rows.append([
                        fn,
                        user_id_padded,
                        full_src,
                        ext.lstrip("."),
                        created.strftime("%Y-%m-%d"),
                        created.strftime("%H:%M:%S"),
                        size_mb
                    ])
            except(PermissionError, FileNotFoundError):
                continue

            if total_files % PROGRESS_INTERVAL == 0:
                    print(f"{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | Durchsuchte Dateien: {total_files} | Gefundene Unterschiede: {found_diffs}")

    # CSV schreiben
    with open(OUTPUT_PATH + CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "Dateiname", "ID", "Dateipfad",
            "Dateityp", "Datum", "Uhrzeit", "Größe (MB)"
        ])
        writer.writerows(rows)

    endtime = time.time()
    duration = int(endtime - start)
    hours, rest = divmod(duration, 3600)
    mins, secs = divmod(rest, 60)
    str_dur = f"{hours:02}:{mins:02}:{secs:02}"

    print("\nFertig!")
    print(f"{total_files} Dateien durchsucht, {len(rows)} Unterschiede gefunden.")
    print(f"Gesamtgröße: {round(total_size / (1024), 2)} GB")
    print(f"Ergebnisse gespeichert in: {OUTPUT_PATH + CSV_OUTPUT}")
    print(f"Die Suche hat {str_dur} gedauert.")

if __name__ == "__main__":
    print("Die Suche wird gestartet!\n")
    scan_and_report()
