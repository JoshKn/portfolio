#! /usr/bin/env python
# https://www.hdhead.com/?p=829

"""
Automatically creates avid Projects from directories in the same working directory.
"""

# Version 1.1

import logging
import os
import shutil
import socket
import glob

LOGGING_FILE = ""
logging.basicConfig(filename=LOGGING_FILE, filemode="a", format="%(asctime)s %(levelname)s {} - %(message)s".format(socket.gethostname()), datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

#---------User configuration.---------

#projBasePath	= "path\\to\\projects\\test"
projBasePath 	= ".\\"

GLOB_PATH_MASK = os.path.join(projBasePath, "*_*")
full_paths = glob.glob(GLOB_PATH_MASK)

#-------End user configuration.--------

# stores directory (project) names in a list
def getProjNames() -> list:
	project_names = []

	for path in full_paths:
		if os.path.isdir(path):
			project_names.append(os.path.basename(path))
	
	return project_names

# creates avid Projects for every name/item in a list
def createProjects(dummyName: str):
	dummyPath = f"path\\to\\ingest_tools\\{dummyName}\\"
	dummyFiles = [f"{dummyName}.avp", f"{dummyName} Settings.xml"]

	for project in getProjNames():
		#projPath = os.path.join("path\\to\\projects", project) # directory for testing
		projPath = os.path.join(".", project) # directory where avid Project will be created

		# renames existing directories with suffix "_old"
		if os.path.exists(projPath):
			try:
				dir_old = (projPath + "_old")
				os.rename(projPath, dir_old)
			except:
				logging.error(f"Directory {project} already exists in this location.")
				return False
		
		# creates project files if they don't already exist
		try:
			shutil.copytree(dummyPath, projPath)
			for i in dummyFiles:
				renameSource = os.path.join(projPath, i)
				extension = os.path.splitext(i)[1]
				if extension == ".xml":
					extension = " Settings.xml"
				renameDestination = os.path.join(projPath, project + extension)
				os.rename(renameSource, renameDestination)
			logging.info(f"{project} avid Project was created using '{dummyName}'")
		except:
			logging.error(f"avid Project {project} already exists in this location.")
			return False

if __name__ == "__main__":
	createProjects()