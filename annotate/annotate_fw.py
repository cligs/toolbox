#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: get_lexnames.py
# Authors: #cf
# 2016-05-20

"""
Functions to annotate French text with Freeling and add WordNet lexnames.
"""

import re
import os
import glob
import subprocess
from nltk.corpus import wordnet as wn


FreelingPath = "/home/christof/Programs/FreeLing4/"
WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wordnet/"
#WorkDir = "/home/christof/Dropbox/0-Analysen/2016/wordnet/"
InPath = WorkDir+"txt/*.txt"
FreelingFolder = WorkDir+"fl/" 
WordnetFolder = WorkDir+"wn/" 


def use_freeling(FreelingPath, InPath, FreelingFolder): 
    """
    Call Freeling "analyze".
    Author: #cf.
    """
    print("use_freeling...")
    
    if not os.path.exists(FreelingFolder):
        os.makedirs(FreelingFolder)

    for File in glob.glob(InPath): 
        Filename = os.path.basename(File)
        OutPath = FreelingFolder + Filename[:-4] + ".xml" 
        Command = "analyze -f fr.cfg --outlv tagged  --sense ukb --output xml < " + File + " > " + OutPath   
        #print(Command)
        subprocess.call(Command, shell=True)

    print("Done.")


def use_wordnet(FreelingFolder, WordnetFolder):
    """
    Call Wordnet using NLTK to get the lexnames.
    Author: #cf.
    """
    print("use_wordnet...")
    
    if not os.path.exists(WordnetFolder):
        os.makedirs(WordnetFolder)


    InPath = FreelingFolder+"*.xml"
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
                    Line = re.sub(" >", " wn=\"xxx\" lxn=\"xxx\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "sentence" in Line:
                    #print(Line)
                    Line = re.sub(" >", " wn=\"xxx\" lxn=\"xxx\" >", Line)
                    #print(Line)
                    NewText.append(Line)

            NewText.append("</sentence>\n</body>")                
            NewText = ''.join(NewText)
            with open(WordnetFolder+Filename, "w") as OutFile: 
                OutFile.write(NewText)
                
    print("Done.")
    


def annotate_fw(FreelingPath, InPath, FreelingFolder, WordnetFolder):
    #use_freeling(FreelingPath, InPath, FreelingFolder)
    use_wordnet(FreelingFolder, WordnetFolder)

annotate_fw(FreelingPath, InPath, FreelingFolder, WordnetFolder)
    
    

