"""Casting DB helper that lists all files recursively and can strip user-ID prefixes from filenames for comparison.
Also provides a utility to write the resulting file list to a CSV for further analysis."""

import glob
import json
from itertools import chain
from os import path
from pathlib import Path
import csv
import re
import time
# import numpy as np
#from deepdiff import DeepDiff
# possible useful modules: deepdiff, numpy, dircmp, difflib

start =time.time()

media = r"path\to\media"
convertedmedia = r"path\to\convertedmedia"
backup = r"\\nas-server\backup"

csv_path = r".\rs_casting_converter\csv\\"

mac_path = "/path/to/testing_files"
json_path_mac = "/path/to/json/"

# remove user-id from filename (123456_)
# ? index out of range if file.name doesn't contain UID -> doesn't matter if every file contains UID
def remove_user_id(generator):
    """Removes User-ID (first 7 digits (eg '123456_')) from all filenames in a generator"""
    # rsplit discards user-id up to the first '_' and with_name updates file.name inside of the generator
    # re.match uses regex to match files that start with 4-6 digits follwed by a '_'
    files_without_uid = (util_remove_user_id_value(file) for file in generator if file.is_file())

    return files_without_uid 
    # if re.match(r"\b\d{4,6}_", file.name) -> only returns files that had UID prefix

def util_remove_user_id_index(file):
    try:
        return re.split(r"\b\d{4,6}_", file.name, 1)[1]
    except IndexError:
        print(f"List index out of range for file {file} with filename {file.name}")

def util_remove_user_id_value(file):
    try:
        return file.with_name(util_remove_user_id_index(file))
    except ValueError:
        print(f"Value Error: {file} contains invalid name {file.name}")

# ignore files that end with FNAM, .DS_Store, Thumbs.db
def remove_file_from_generator(generator, file_to_remove:str):
    """Removes a file from a generator that ends with file_to_remove"""
    return (file for file in generator if not type(file) == None or file.name.endswith(file_to_remove)) # returns a generator of all files where the file name != file_to_remove

# list all files in a directory
def list_all_files_recursively(path:str):
    """Creates a generator for all files inside of a directory (works recursively)"""
    pathlib_path = Path(path)
    return pathlib_path.glob("**/*.*") # returns a generator of pathlib objects

def write_to_csv(generator, file_name):
    func_start = time.time()
    counter = 1

    with open (f"{file_name}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="≠")
        for file in generator:
            writer.writerow(str(file))
            print(f"{counter} filenames written.")
            counter += 1

    func_end = time.time()
    print(f"Saved {counter} filenames to {file_name}.csv. That took {func_end-func_start} seconds.")

def calculate_runtime(start):
    end = time.time()

    runtime_seconds = (end-start)
    runtime_minutes = int(runtime_seconds / 60)

    print("--------------------")
    if runtime_minutes != 0:
        print(f"The whole program took {runtime_minutes}m {int((runtime_seconds - (runtime_minutes * 60 )) % runtime_minutes)}s to run.")
    else:
        print(f"The whole program took {runtime_minutes}m {runtime_seconds * 10**3}ms to run.")

# create lists for all locations
media_files = list_all_files_recursively(convertedmedia)
""" convertedmedia_file_no_UID = remove_user_id(list_all_files_recursively(convertedmedia))
convertedmedia_file_no_UID = remove_file_from_generator(convertedmedia_file_no_UID, "Thumbs.db")
backup_files = remove_file_from_generator(list_all_files_recursively(backup), "Thumbs.db")
backup_files = remove_user_id(backup_files)

# chain all file that went through the converter
converted_files = chain(convertedmedia_file_no_UID, backup_files) """


write_to_csv(media_files, f"{csv_path}converted_2024_08_16")
#write_to_csv(media_files, f"{csv_path}converted_2024_08_08")

# compare converted_files to files from media

calculate_runtime(start)