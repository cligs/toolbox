#!/usr/bin/env python3
# Filename: find-and-replace.py
# Author: #cf
# Date: 2016


"""
Script for search-and-replace, useful when dealing with lots of files.
WARNING! Using regular expressions on large numbers of texts in one go 
may lead to unexpected changes in your files! This script does not have an
undo functionality! You need to make a copy of your data before using this script.
"""


#####################
# Parameters
#####################

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wordlist/txt/" # ends on slash
TextPath = WorkDir+"*.txt"

Find = "–"
Replace = "--"



#####################
# Import statements
#####################

import os
import re
import glob



#####################
# Functions
#####################

def read_file(File):
    """
    # Read a text file and return as string.
    """
    with open(File, "r") as InFile: 
        Text = InFile.read()
        Filename = os.path.basename(File)
    return Text, Filename


def find_and_replace(Find, Replace, Text): 
    Text = re.sub(Find, Replace, Text)
    return Text


def save_text(Text, WorkDir, Filename): 
    """
    Save changed text to file.
    """
    with open(WorkDir+Filename, "w") as OutFile: 
        OutFile.write(Text)


####################
# Main
####################

def main(WorkDir, TextPath, Find, Replace): 
    print("Launched.")
    for File in glob.glob(TextPath): 
        Text, Filename = read_file(File)
        Text = find_and_replace(Find, Replace, Text)
        save_text(Text, WorkDir, Filename)
    print("Done.")

main(WorkDir, TextPath, Find, Replace)






