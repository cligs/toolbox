#!/usr/bin/env python3
# Filename: tei2txt.py

"""
# Script to rename files based on selected metadata from a CSV file.
"""

###############################
# Overview of functions
###############################

# Assumes there is a folder of plain text files, this script and a CSV file with metadata all in one folder.
# Starts the following routine for all .txt files in a folder.
# 2. Read CSV file with metadata
# 2. Construct a new filename based on selected metadata from CSV file.
# 3. Give each file the new filename.


###############################
# User settings
###############################

# 1. Adapt the inputfolder, metadatafile and outputfolder as needed.
# 2. Select metadata items and their order for new filename.


###############################
# WARNING
###############################

# It is quite difficult to undo the action of this script, so make a copy first!


###############################
# Import statements
###############################

import glob
import pandas
import os
import time


###############################
# File renaming
###############################

def rename_files(file,metadatafile,outputfolder):
    """Renames files based on metadata from a CSV file."""
    filename = os.path.basename(file)
    basename, extension = os.path.splitext(filename)
    idno = basename
    print("Treating file with idno: ", basename)
    metadata = pandas.read_csv(metadatafile)
    metadatax = metadata.set_index('idno', drop=True)
    author = metadatax.loc[idno, 'author']
    title = metadatax.loc[idno, 'title']
    genre = metadatax.loc[idno, 'label']
    year = metadatax.loc[idno, 'year']
    year = str(year)
    decade = year[0:3]+"0s"
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    #### USER: Construct new filename from metadata fields
    newfilename = genre+"_"+author+"-"+idno+".txt"
    newoutputpath = outputfolder+"/"+newfilename
    print("New filename: "+idno + ": " + newoutputpath)
    os.rename(file,newoutputpath)


###############################
# Main
###############################

def main(inputpath,metadatafile,outputfolder):
    numberoffiles = 0
    for file in glob.glob(inputpath):
        rename_files(file,metadatafile,outputfolder)
        numberoffiles +=1
    print("Number of files treated: " + str(numberoffiles))
    time.sleep(2)


#### USER: Indicate parameters
main("./input/*.txt","romanpolicier.csv","labeled-test")
