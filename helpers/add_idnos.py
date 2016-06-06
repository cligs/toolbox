#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to add idno from filename to teiHeader.
"""

inpath = "./tei/*.xml"
outfolder = "idnos/"


import os
import glob
import re

def add_idnos(inpath): 
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for file in glob.glob(inpath): 
        filename = os.path.basename(file)
        idno = filename[:-4]
        print(idno)
        with open(file, "r") as infile: 
            text = infile.read()
            text = re.sub("<idno type=\"cligs\"/>", "<idno type=\"cligs\">"+idno+"</idno>" , text)
            with open(outfolder+filename, "w") as output:
                output.write(text)

add_idnos(inpath)