#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: get_lexnames.py
# Authors: #cf
# 2016-05-20

"""
Functions to annotate French text with Freeling, add lexnames, prepare for TXM.
"""

import re
import os
import glob
#import pandas as pd
import subprocess
from nltk.corpus import wordnet as wn


FreelingPath = "/home/christof/Programs/FreeLing4/"
WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wordnet/"
#WorkDir = "/home/christof/Dropbox/0-Analysen/2016/wordnet/"
InPath = WorkDir+"txt/*.txt"
DataFolder = WorkDir+"data/" 
TXMFolder = WorkDir+"txm/"


def use_freeling(FreelingPath, InPath, DataFolder): 
    """
    Call Freeling "analyze".
    Author: #cf.
    """
    print("use_freeling...")

    for File in glob.glob(InPath): 
        Filename = os.path.basename(File)
        OutPath = DataFolder + Filename[:-4] + "_fl.xml" 
        Command = "analyze -f fr.cfg --outlv tagged  --sense ukb --output xml < " + File + " > " + OutPath   
        #print(Command)
        subprocess.call(Command, shell=True)

    print("Done.")


def find_lexnames(DataFolder, TXMFolder):
    """
    Call Wordnet using NLTK to get the lexnames.
    Author: #cf.
    """
    print("find_lexnames...")

    InPath = DataFolder+"*.xml"
    for File in glob.glob(InPath): 
        with open(File, "r") as InFile: 
            Filename = os.path.basename(File)
            Text = InFile.read()
            Text = re.split("</token>", Text)
            NewText = ["<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<body>"]
            for Line in Text[0:-1]:
                Line = Line + "</token>"
                #print(Line)
                Word = re.findall("form=\"(.*?)\" ", Line)[0]
                #print(Word)
                Line = re.sub("</token>", Word+" </token>", Line)
                #print(Line) 
                if "wn=" in Line: 
                    #print(Line)
                    SynsetID = re.findall("wn=.*\"", Line)[0]
                    SynsetNumber = int(SynsetID[4:-3])
                    SynsetPOS = SynsetID[-2:-1]
                    #print(SynsetID, SynsetPOS, SynsetNumber)
                    SynsetAbbID = wn._synset_from_pos_and_offset(SynsetPOS, SynsetNumber)
                    SynsetAbbID = str(SynsetAbbID)
                    SynsetAbbID = SynsetAbbID[8:-2]
                    #print(SynsetAbbID)
                    Lexname = wn.synset(SynsetAbbID).lexname()
                    #print(Lexname)
                    Line = re.sub("(wn=.*) >", "\\1 lxn=\""+Lexname+"\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "wn=" not in Line and "sentence" not in Line:
                    #print(Line)
                    Line = re.sub(" >", " wn=\"XXX\" lxn=\"XXX\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "sentence" in Line:
                    #print(Line)
                    Line = re.sub(" >", " wn=\"XXX\" lxn=\"XXX\" >", Line)
                    #print(Line)
                    NewText.append(Line)

            NewText.append("</sentence>\n</body>")                
            NewNewText = ''.join(NewText)
                
            # Prepare for TXM
            NewNewText = re.sub("<token","<w", NewNewText)
            NewNewText = re.sub("</token>","</w>", NewNewText)
            #print(NewNewText)
            with open(TXMFolder+Filename[:-7]+".xml", "w") as OutFile: 
                OutFile.write(NewNewText)
                
                
                

    print("Done.")
    


def get_lexnames(FreelingPath, InPath, DataFolder, TXMFolder):
    #use_freeling(FreelingPath, InPath, DataFolder)
    find_lexnames(DataFolder, TXMFolder)

get_lexnames(FreelingPath, InPath, DataFolder, TXMFolder)
    
    

