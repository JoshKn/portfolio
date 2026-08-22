"""CLI utility to check if a file's creation date (ctime) is older than 5 years.
Accepts a file path as argument and returns 1 (older than 5 years) or 0 (not older)."""

import argparse
import os
import time

FIVE_YEARS_UNIX = 157852800

def is_ctime_older_5y(file_path):
    ctime = os.path.getctime(file_path)
    time_diff = time.time() - ctime
    if time_diff < FIVE_YEARS_UNIX:
        return 0
    else:
        return 1

if __name__ == "__main__":
    # Argumente aus der Kommandozeile verarbeiten
    parser = argparse.ArgumentParser(
        description="Überprüft, ob das Creation Date einer Datei länger als 5 Jahre her ist."
    )
    # Ein erforderliches Argument: die Datei
    parser.add_argument(
        "file_path", 
        help="Der Pfad zur Datei, die überprüft werden soll."
    )

    args = parser.parse_args()

    print(is_ctime_older_5y(args.file_path))