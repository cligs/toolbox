#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: fw2txm.py
# Authors: #cf
# 2016-05-20

"""
Functions to convert Freeling+WordNet format for import into TXM.
"""

import re
import os
import glob


WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wordnet/"
#WorkDir = "/home/christof/Dropbox/0-Analysen/2016/wordnet/"
InPath = WorkDir+"wn/*.xml"
TXMFolder = WorkDir+"txm/"



def fw2txm(InPath, TXMFolder):
    """
    Transform Freeling+Wordnet output to format suitable for import in TXM.
    Author: #cf.
    """
    print("fw2txm...")
    
    if not os.path.exists(TXMFolder):
        os.makedirs(TXMFolder)


    for File in glob.glob(InPath): 
        with open(File, "r") as InFile: 
            Filename = os.path.basename(File)
            Text = InFile.read()
            TXMText = re.sub("<token","<w", Text)
            TXMText = re.sub("</token>","</w>", TXMText)
            with open(TXMFolder+Filename, "w") as OutFile: 
                OutFile.write(TXMText)
    
    print("Done.")
    

fw2txm(InPath, TXMFolder)
    
    

