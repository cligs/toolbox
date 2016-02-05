# verspers.py
# Script to assess percentage of verse, prose and stage directions in TEI-encoded plays.
# Assumes that prose is marked-up as "s", verse as "l" and stage directions as "stage". 
# Version 0.1, 8.6.2014, by #cf.   


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

###############################
# Actual text processing
###############################

def verspers(file): 
    """Count the number and length of prose, verse, and stage sections in a TEI-encoded play."""                                      
    xmltree = etree.parse(file)                                     # Loads and parses the XML input file.
    basename = os.path.basename(file)                           # Retrieves just the basename from the filename.    
    xpath_stage = '//body//*[self::stage]//text()'                  # All stage directions in body of plays.
    xpath_prose = '//body//*[self::s]//text()'                      # All text of s in body of plays.
    xpath_verse = '//body//*[self::l]//text()'                      # All text of l in body of plays.

    stage = xmltree.xpath(xpath_stage)                              # Extracts the text according to the XPath expression.
    stage = "\n".join(stage)                                        # Puts all text pieces together as a string, each match on a new line.
    #print(basename + ", stage: " + stage[0:151])

    prose = xmltree.xpath(xpath_prose)                              # Extracts the text according to the XPath expression.
    prose = "\n".join(prose)                                        # Puts all text pieces together as a string, each match on a new line.
    prose = re.sub("\n\n","\n",prose)
    #print(basename + ", prose: " + prose[0:151])

    verse = xmltree.xpath(xpath_verse)                              # Extracts the text according to the XPath expression.
    verse = "\n".join(verse)                                        # Puts all text pieces together as a string, each match on a new line.
    #print(basename + ", verse: " + verse[0:151])

    length_prose = len(prose)
    length_verse = len(verse)
    length_stage = len(stage)
    length_all = len(verse) + len(prose) + len(stage)

    prop_prose = length_prose / length_all
    prop_verse = length_verse / length_all
    prop_stage = length_stage / length_all
    
    output = basename[:-4] + "," + str(round(prop_prose,3)) + "," + str(round(prop_verse,3)) + "," + str(round(prop_stage,3)) + "," + str(length_all) + "\n"
    #print(output)
    with open("verspers-results.csv", "a") as resultfile:           # Creates a new file in "appending" mode.
        resultfile.write(output)                                    # Adds output from current text to the results file. 


###############################
# Main
###############################

def main(inputpath): 
    for file in glob.glob(inputpath): 
        verspers(file)

main('./input/*.xml')                                    # Enter absolute or relative path to folder with XML files and define filename filter.
