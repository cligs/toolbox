#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ulrike Henny
@filename: use_heideltime.py

Submodule calling HeidelTime Standalone
See https://github.com/HeidelTime for more information about this temporal tagger

"""

import os
import glob
import subprocess
import sys


def apply_ht(hdpath, infolder, outfolder, language="ENGLISH", outtype="TIMEML", pos="TREETAGGER"):
	"""
	Applies the HeidelTime Standalone version to a bunch of plain text files.
	Requires HeidelTime Standalone to be installed.
	Be careful: seems to need a lot of time.
	
	Arguments:
	hdpath (string): path to the HeidelTime installation
	infolder (string): path to the input folder (which should contain plain text files)
	outfolder (string): path to the output folder (which should exist)
	language (string): indicates the language of the documents, e. g. "SPANISH", "FRENCH", "ENGLISH", defaults to English
	outtype (string): type of result; "XMI" or "TIMEML", defaults to "TIMEML"
	pos (string): POS Tagger; "STANFORDPOSTAGGER", "TREETAGGER" or "NO", defaults to "TREETAGGER"
	"""
	inpath = os.path.join(infolder, "*.txt")
	filecounter = 0
	
	print("Starting...")
	
	for filepath in glob.glob(inpath):
		filecounter+= 1
		fn = os.path.basename(filepath)[:-4]
		fnout = fn + ".xml"
		command = "java -jar " + os.path.join(hdpath, "de.unihd.dbs.heideltime.standalone.jar") + " " + filepath + " -c " + os.path.join(hdpath, "config.props") + " -l " + language + " -o " + outtype + " > " + os.path.join(outfolder, fnout)
		print("Treating " + fn + " ...")
		subprocess.call(command, shell=True)
	
	print("Done. " + str(filecounter) + " files treated.")


if __name__ == "__main__":
	apply_ht(int(sys.argv[1]))
