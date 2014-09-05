# ana2csv.py
# Script to extract tags and text content from individually tagged sentences from a TEI document and save them to a CSV file.
# Assumes that each sentence is tagged as "s" with an attribute "ana" that takes one or several values. 
# Output will be a CSV file that has one row per sentence, with the first column containing the value of ana and the second row containing the text of that sentence.
# Relies on "lxml" for parsing the TEI file, on XPath for selecting parts of the TEI file, and on "re" for text cleanup.
# Note: the namespace solution used here makes this incompatible with plain XML or TEI P4. Tested on Python 3.4. 
# Many thanks to Katrin Betz for solving some newline issues in an earlier version of this script.


###############################
# Overview of functions
###############################

# 1. Load several TEI files from a folder one after the other.
# 2. For each file, parse the file to build a Python element tree representation.
# 3. For each sentence in each file, extract the value of the @ana and the corresponding text content.
# 4. For each file, create a table from the the values and text and write it to a CSV file.


###############################     
# User settings
###############################

# 1. Mandatory: Modify the path to the working directory
# 2. Optional: Modify the filename filter (default: *.xml)
# 3. Optional: Modify the XPath expressions as needed.
# 4. Optional: Select which cleanup procedures should be used and/or adapt them to your needs.


###############################
# Import statements
###############################

from lxml import etree
import re
import glob
import numpy as np
import csv
from itertools import *


###############################
# Text processing
###############################

def ana2csv(file):
    """Load TEI files from folder, extract selected data, save to new CSV files"""
    xmltree = etree.parse(file)                                         # Loads and parses the XML input file.
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}                  # Defines the namespace to be used in the xpathexpr.

    xpath_value = '//tei:body//tei:s//@ana'                             # For each sentence, identify the value of the attribute "ana".
    values = xmltree.xpath(xpath_value, namespaces=namespaces)          # Extracts the values and saves to variable as a list.
    #print(values[0:3])
    
    xpath_content = '//tei:body//tei:s'
    contents = xmltree.xpath(xpath_content, namespaces=namespaces)          # X-Path to s-Elements
    text = [' '.join(etree.ElementTextIterator(sent)) for sent in contents] # Iterates over the textnodes of each subtree and join the result
    delWS=[re.sub('\s{2,}|\r+|\n+', ' ', s) for s in text]                  # Replaces multiple whitespaces and linebreaks

    outputfile = file[:-4] + ".csv"                                     # Builds filename from inputfile with new extension.

    csv_output = open(outputfile, 'w')                      # Opens a file for writing. Uses parameter newline to handle linebreaks

    csvwriter = csv.writer(csv_output)                                  # Creates the csv writer object.
    for row in zip(values, delWS):
        print(row)                                                      # writerow - one row of data at a time.
        csvwriter.writerow(row)
    csv_output.close()


###############################
# Main
###############################

def main(inputpath):
    for file in glob.glob(inputpath):
        ana2csv(file)

main('./tagged/*.xml')                                                # Enter absolute or relative path to folder with XML files and define filename filter.
