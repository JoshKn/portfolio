import os
import csv
from pathlib import Path
import argparse
import time
import datetime

# Standard Windows-UNC-Pfad
#default_root = Path(r"\\nas-server\farm-settings\99_Test_Footage\Casting_Medienordner_Out")
default_root = Path(r"\\nas-server\convertedmedia")

EXCLUDE_DIRS = {"Videos", "Bilder", "Dateien"}


start = time.time()

def list_subfolders_to_csv(root_dir: Path, output_csv: Path):
    searched_files_counter = 0
    found_dirs_counter = 0
    """
    Listet rekursiv alle Unterordner der ID-Ordner in root_dir auf und schreibt sie in eine CSV-Datei:
      - Header: ID, Path, Path ohne Stammverzeichnis + ID
      - Schließt Unterordner aus, deren letzter Ordnername in EXCLUDE_DIRS ist.
    """
    if not root_dir.is_dir():
        print(f"Fehler: {root_dir} ist kein gültiges Verzeichnis.")
        return

    
    results = []
    # Nur oberste Ebene: ID-Ordner (4-6 Ziffern)
    for folder in root_dir.iterdir():
        if not folder.is_dir():
            continue
        name = folder.name
        if not name.isdigit() or len(name) not in (4, 5, 6):
            continue
        
        id_str = name.zfill(6) # padded auf 6 ziffern mit nullen
        id_folder = root_dir / id_str
        if not id_folder.exists():
            id_folder = folder  # Fallback, falls noch nicht umbenannt wurde
        # Rekursiv durch alle Unterordner
        for dirpath, dirnames, filenames in os.walk(id_folder):
            searched_files_counter += 1
            current = Path(dirpath)
            # Skip the root ID folder itself
            if current == id_folder:
                continue
            last_part = current.name
            if last_part in EXCLUDE_DIRS:
                continue
            # Pfad relativ zum ID-Ordner
            rel = current.relative_to(id_folder)
            results.append([id_str, str(current), str(rel)])
            found_dirs_counter += 1

            if searched_files_counter % 1000 == 0:
                now = datetime.datetime.now()
                print(f"{now.strftime("%d.%m.%Y %H:%M:%S")} | Durchsuchte Verzeichnisse: {searched_files_counter} | Gefunden: {found_dirs_counter}")

    with open(output_csv, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Path", "Directory"])
        writer.writerows(results)

    # Abschlussmeldung
    endtime = time.time()
    duration = int(endtime - start)
    hours, rest = divmod(duration, 3600)
    mins, secs = divmod(rest, 60)
    str_dur = f"{hours:02}:{mins:02}:{secs:02}"

    print("\nFertig!")
    print(f"{found_dirs_counter} Unterordner in gefunden.")
    print(f"Ergebnisse gespeichert in: {output_csv}")
    print(f"Die Suche hat {str_dur} gedauert.")


list_subfolders_to_csv(default_root, r"c:\Users\knorz\dev\castingDB_subfolder_2025_08_08.csv")
