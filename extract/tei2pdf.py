#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ulrike Henny
@filename: tei2pdf.py

Converts a collection of TEI files into "reading versions" in PDF.
Needs an Apache FOP installation, see http://xmlgraphics.apache.org/fop/2.1/running.html for further information.
Uses tei2pdf.xsl which should be in the same directory as the current script.

"""

import sys
import glob
import os
import subprocess


def convert2pdf(foppath, infolder, outfolder, lang="es"):
	"""
	Converts a collection of TEI files into "reading versions" in PDF.
	
	Arguments:
	foppath (string): path to Apache FOP installation
	infolder (string): path to the input folder (which should contain the TEI files)
	outfolder (string): path to the output folder (which will be created if it does not exist)
	lang (string): language, default "es", also possible: "fr", "en"
	"""
	inpath = os.path.join(infolder, "*.xml")
	filecounter = 0
	
	print("Starting...")
	
	if not os.path.exists(outfolder):
		os.makedirs(outfolder)
    
	scriptdir = os.path.dirname(os.path.realpath(__file__))
	
	for filepath in glob.glob(inpath):
		print("Doing file " + filepath)
		filecounter+= 1
		fn = os.path.basename(filepath)[:-4]
		
		command = "java -Dfop.home=" + foppath + " -jar " + os.path.join(foppath, "build/fop.jar") + " -xml " + filepath + " -xsl " + os.path.join(scriptdir, "tei2pdf.xsl") + " -pdf " + os.path.join(outfolder, fn + ".pdf" + " -param lang '" + lang + "'")
		subprocess.call(command, shell=True)
	
	print("Done. " + str(filecounter) + " files treated.")
	
	

if __name__ == "__main__":
	convert2pdf(int(sys.argv[1]))
