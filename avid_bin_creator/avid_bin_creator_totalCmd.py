import logging
import os
import socket
import sys

import avb

# Version 1.1

LOGGING_FILE = ""
logging.basicConfig(filename=LOGGING_FILE, filemode="a", format="%(asctime)s %(levelname)s {} - %(message)s".format(socket.gethostname()), datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

tmp_file_path = sys.argv[1]
output_dir = sys.argv[2]

bin_names = []

# retrieves dir names from .tmp file passed by totalcmd 
with open(tmp_file_path) as f:
    for item in f:
        if os.path.isdir(item[:-2]): # only valid path without last 2 chars
            print(item)
            bin_names.append(os.path.basename(item[:-2]))
        else:
            logging.warning(f"{item[:-1]} is not a directory")

# create bins in totalcmd target dir
for bin in bin_names:
    with avb.file.AVBFile() as avb_new:
        current_bin = bin + ".avb"
        try:
            avb_new.write(output_dir + current_bin) 
            logging.info(f"{current_bin} was created")
        except Exception as e:
            logging.error(f"{current_bin[:-1]} returned exception {e}")
