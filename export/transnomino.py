# transnomino.py
# Script to rename files based on selected metadata from a CSV file. 

###############################
# Overview of functions
###############################

# 1. Read filenames for several files in a given folder.
# 2. Read CSV file with metadata
# 2. Construct a new filename based on selected metadata from CSV file.
# 3. Give each file the new filename. ########### unimplemented as of 2014-04-30 ##################


###############################
# User settings
###############################

# 1. Modify the path to the working directory
# 2. Modify the filename filter
# 3. Select which metadate should be selected in which order


###############################
# Import statements
###############################

import glob
import pandas
import os


###############################
# File renaming
###############################

def transnomino(file,metadatafile):
    """Read filenames for several files in a given folder and for each filename, construct a new filename based on selected metadata from CSV file."""
    idno = file[-9:-4]
    #print(idno)
    metadata = pandas.read_csv(metadatafile)
    #print(metadata)
    metadatax = metadata.set_index('idno', drop=True)
    #print(metadatax.index)
    #print(metadatax)
    author = metadatax.loc[idno, 'author']
    stitle = metadatax.loc[idno, 'short-title']
    date = metadatax.loc[idno, 'date']
    decade = metadatax.loc[idno, 'decade']
    persp = metadatax.loc[idno, 'persp']    
    newfilename = persp+"_"+author+"-"+decade+"-"+idno+".txt"
    print(idno + ": " + newfilename)
    pos.rename(file,newname)
    

###############################
# Main
###############################

def main(datafolder,metadatafile):
    for file in glob.glob(datafolder):
        transnomino(file,metadatafile)

main("./texts/*.txt","metadata.csv") 								# USER: Enter absolute or relative path to folder with files, define pattern for filename (e.g., extension), enter path for metadata file.
