#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to fix Unicode errors in Unicode files. Not for converting to Unicode.
Usage: Place files in need to be fixed in the folder "fixme" and run the script.
Result: The fixed files will be placed in the folder "fixed". 
@author: #cf. 
"""

inpath = "./fixme/*.txt"
outfolder = "fixed/"


import ftfy
import os
import glob

def fix_unicode(inpath): 
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for file in glob.glob(inpath): 
        filename = os.path.basename(file)
        with open(file, "r") as infile: 
            text = infile.read()
            result = ftfy.fix_text(text)
            with open(outfolder+filename, "w") as output:
                output.write(result)

fix_unicode(inpath)