#!/usr/bin/env python3
# Filename: rename_files.py
# Author: #cf

"""
# Rename files based on selected metadata from a CSV file.
"""

import glob
import pandas
import os
import shutil

def rename_files(wdir, inpath, metadatafile, main_category, sec_category):
    """Renames files based on metadata from a CSV file."""
    outfolder = main_category+"/"
    if not os.path.exists(wdir+outfolder):
        os.makedirs(wdir+outfolder)
    for file in glob.glob(wdir+inpath):
        shutil.copy(file,wdir+outfolder+file[-10:])
    for file in glob.glob(wdir+outfolder+"*.txt"):
        filename = os.path.basename(file)
        idno, extension = os.path.splitext(filename)
        idno = idno[-6:]
        #print("Treating file with idno: ", idno)
        metadata = pandas.read_csv(wdir+metadatafile)
        metadatax = metadata.set_index('idno_header', drop=True)
        main_label = metadatax.loc[idno, main_category]
        sec_label = metadatax.loc[idno, sec_category]
        newfilename = main_label+"_"+sec_label+"-"+idno+".txt"
        newoutputpath = wdir+outfolder+newfilename
        os.rename(file,newoutputpath)
    print("\nDone.")

def main(wdir, inpath, metadatafile, main_category, sec_category):
        rename_files(wdir, inpath, metadatafile, main_category, sec_category)


#### USER: Indicate parameters
## Possible values for main_category and sec_category: "author_short","title_short","genre","subgenre"
main("/home/christof/Repos/cligs/romanfrancais/", "txt/*.txt", "header-metadata.csv", "author_short", "title_short")

# TODO: add "decade" and "year" (str!) here and in get_metadata.py

