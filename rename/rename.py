# rename.py
# Script to rename files based on selected metadata from a CSV file. 

###############################
# Overview of functions
###############################

# 1. Start the following routine for all .txt files in a folder.
# 2. Read CSV file with metadata
# 2. Construct a new filename based on selected metadata from CSV file.
# 3. Give each file the new filename. 


###############################
# User settings
###############################

# The script assumes you have plain text files, this script and a CSV file with metadata all in one folder.
# 1. Adapt the filename filter
# 2. Modify the filename of the metadata file as needed
# 3. Indicate which metadata should be selected and in which order it should be used to build the new filename.


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
    newfilename = "output/" + persp+"_"+author+"-"+stitle+"-"+idno+".txt"  # Supposes there is a subfolder called "output". 
    print(idno + ": " + newfilename)
    os.rename(file,newfilename)
    

###############################
# Main
###############################

def main(datapath,metadatafile):
    for file in glob.glob(datapath):
        transnomino(file,metadatafile)

main("./input/*.txt","./input/metadata.csv") 							# USER: Enter absolute or relative path to folder with files, define pattern for filename (e.g., extension), enter path for metadata file.
