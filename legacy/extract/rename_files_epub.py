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

def rename_files(wdir, inpath, metadatafile, primary_category, secondary_category):
    """Renames files based on metadata from a CSV file."""
    outfolder = primary_category+"/"
    ## Check if outfolder exists, if not create it.
    if not os.path.exists(wdir+outfolder):
        os.makedirs(wdir+outfolder)
    ### Copy the original files to the new folder.
    counter = 0
    for file in glob.glob(wdir+inpath):
        shutil.copy(file,wdir+outfolder+file[-11:])
    ## For each file in the new folder...
    for file in glob.glob(wdir+outfolder+"*.epub"):
        ## Get labels from metadatafile for primary and secondary category.
        filename = os.path.basename(file)
        idno, extension = os.path.splitext(filename)
        idno = idno[:6] # Assumes the original filename starts with idno.
        metadata = pandas.read_csv(wdir+metadatafile)
        metadatax = metadata.set_index('idno', drop=True)
        primary_label = metadatax.loc[idno, primary_category]
        secondary_label = metadatax.loc[idno, secondary_category]
        ## Construct new filename based on primary and secondary labels.
        newfilename = primary_label+"_"+secondary_label+"-"+idno+".epub"
        newoutputpath = wdir+outfolder+newfilename
        os.rename(file,newoutputpath)
        counter +=1
    print("\nDone. Files treated: " + str(counter))

def main(wdir, inpath, metadatafile, primary_category, secondary_category):
        rename_files(wdir, inpath, metadatafile, primary_category, secondary_category)


#### USER: Indicate parameters
## Possible values for main_category and sec_category: "author_short","title_short","genre","subgenre"

main("", "epub/*.epub", "metadata.csv", "author-name", "title")
