import glob
import os
import shutil
from datetime import datetime

unconverted_path = "m:/00_mp3_converter_48kHz_24b/testing/input/**/*.*" # path where glob looks for files
unconverted_filepaths = []

time = datetime.now()
today = time.strftime("%Y_%m_%d_%H%M") # YYYY_mm_dd_HHMM

music_output = f"music_output_{today}"
shutil_output = f'm:/00_mp3_converter_48kHz_24b/testing/output/{music_output}' # a unique output path for shutil with the current date & time

for f in glob.glob(unconverted_path, recursive=True):
    unconverted_filepaths.append(f)
unconverted_filepaths.sort()

unconverted_filepaths_list = [i.replace("\\", "/") for i in unconverted_filepaths] # replaces one forward slash with two backward slashes so the path is Windows compatible

for unconverted in unconverted_filepaths_list:
    os.mkdir(shutil_output)
    os.mkdir(f"{shutil_output}/00_NichtKonvertiert")
    shutil.move(unconverted, f"{shutil_output}/00_NichtKonvertiert")
