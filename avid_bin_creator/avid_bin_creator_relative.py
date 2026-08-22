'''Auto-creating Avid bins in a directory.'''
# https://towardsdatascience.com/how-to-easily-convert-a-python-script-to-an-executable-file-exe-4966e253c7e9

import glob
import logging
import os
import socket

import avb

# Version 1.2.1

LOGGING_FILE = ""
logging.basicConfig(filename=LOGGING_FILE, filemode="a", format="%(asctime)s %(levelname)s {} - %(message)s".format(socket.gethostname()), datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

RELATIVE_ROOT_PATH = ".\\"

# looks for files & dirs in RELATIVE_ROOT_PATH that contain _
GLOB_PATH_MASK = os.path.join(RELATIVE_ROOT_PATH, "*_*")
FILE_EXT = ".avb"

def getTapeNames():
    # stores all paths found by glob in full_paths
    full_paths = glob.glob(GLOB_PATH_MASK)
    tapenames = []

    # every item found by glob, that is a dir, is stored in tapenames
    for path in full_paths:
        if os.path.isdir(path):
            tapenames.append(os.path.basename(path))

    return tapenames

def createBins():
    for bin in getTapeNames():
        with avb.file.AVBFile() as avb_new:
            current_bin = bin + FILE_EXT
            avb_new.write(RELATIVE_ROOT_PATH + current_bin) 
            logging.info(f"{current_bin} was created")

if __name__ == "__main__":
    createBins()