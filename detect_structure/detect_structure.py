# ./bin/env python3
# detect_structure.py

"""
# Script to count some basic structural features of plays, such as acts, scenes, and roles.
# Version 0.1, 8.6.2014, by #cf.
"""


###############################
# Overview of functions
###############################

# 1. Load files from a folder.
# 2. For each file containing one play, list the lines.
# 3. For each line, determine whether it is verse, prose, stage or other and store the length of the line in characters.
# 4. For each type, make a list of line lengths.
# 5. Write a CSV file with comma-separated values for: filename, number of verse, prose, stage and other lines as well as percentages.


###############################
# User settings
###############################

# 1. Mandatory: Put all files to be analysed in the subfolder "input" (or change location in main).
# 2. Optional: Adjust the XPath to verse and prose depending on the encoding scheme of your files.


###############################
# Import statements
###############################

from lxml import etree
import re
import glob
import os
import pandas
import matplotlib.pyplot as plt

###############################
# Actual text processing
###############################

def detect_structure(file):
    """Count the number of acts, scenes and roles in a TEI-encoded play."""
    parser = etree.XMLParser(collect_ids=False, recover=True)
    xmltree = etree.parse(file, parser)
    with open(file,"r") as text:
        xmlstring = text.read()
    xmllist = xmlstring.split()
    #print(xmllist)
    basename = os.path.basename(file)
    print(basename)
    xpath_stage = '//body//*[self::stage]//text()'
    xpath_prose = '//body//*[self::s]//text()'
    xpath_verse = '//body//*[self::l]//text()'
    xpath_acts = '//body//*[self::div1]//text()'
    xpath_scenes = '//body//*[self::div2]//text()'
    xpath_cast = '//body//*[self::castList]//text()'
    number_of_acts = 0
    for word in xmllist:
        if "<div1" in word:
            number_of_acts += 1
    #print(number_of_acts)
    number_of_scenes = 0
    for word in xmllist:
        if "<div2" in word:
            number_of_scenes += 1
    #print(number_of_scenes)
    number_of_roles = 0
    for word in xmllist:
        if "<role" in word:
            number_of_roles += 1
    #print(number_of_roles)
    result = basename[:-4] + "," + str(number_of_acts) + "," + str(number_of_scenes) + "," + str(number_of_roles) + "\n"
    #print(result)
    with open("structure.csv", "a") as resultfile:
        resultfile.write(result)

###############################
# Main
###############################

def main(inputpath):
    numberoffiles = 0
    for file in glob.glob(inputpath):
        detect_structure(file)
        numberoffiles +=1
    print("Done. Number of files treated: " + str(numberoffiles))



main('./tei4/*.xml')
