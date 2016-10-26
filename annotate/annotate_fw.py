#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: get_lexnames.py
# Authors: #cf, #uh
# 2016-05-20

"""
Functions to annotate French/Spanish text with Freeling and add WordNet lexnames.
"""

import re
import os
import glob
import subprocess
import collections
from nltk.corpus import wordnet as wn


def use_freeling(InPath, FreelingFolder, Lang="fr"): 
    """
    Call Freeling "analyze".
    Authors: #cf, #uh.
    """
    print("use_freeling...")
    
    if Lang not in ["fr","es", "it", "pt"]:
        raise ValueError("Please indicate one of the following as language: 'fr', 'es', 'it', 'pt'")
        
    if not os.path.exists(FreelingFolder):
        os.makedirs(FreelingFolder)

    for File in glob.glob(InPath): 
        Filename = os.path.basename(File)
        OutPath = FreelingFolder + Filename[:-4] + ".xml" 
        Command = "analyze -f " + Lang + ".cfg --outlv tagged  --sense ukb --output xml < " + File + " > " + OutPath   
        #print(Command)
        subprocess.call(Command, shell=True)

    print("Done.")


def use_wordnet(FreelingFolder, WordnetFolder):
    """
    Call Wordnet using NLTK to get the lexnames.
    Authors: #cf, #uh
    """
    print("use_wordnet...")
    
    if not os.path.exists(WordnetFolder):
        os.makedirs(WordnetFolder)


    InPath = FreelingFolder+"*.xml"
    for File in glob.glob(InPath): 
		
        LexErrCounter = collections.Counter()
		
        with open(File, "r") as InFile: 
            Filename = os.path.basename(File)
            Text = InFile.read()
            Text = re.split(r"\n\s*?</token>", Text)
            NewText = ["<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<wrapper>"]
            for Line in Text[0:-1]:
                Line = re.sub("token", "w", Line)
                Line = re.sub("sentence", "s", Line)
                # Ids löschen
                Line = re.sub(r'\sid=".*?"', "", Line)
                Line = Line + "</w>"
                #print(Line)
                Word = re.findall("form=\"(.*?)\" ", Line)[0]
                #print(Word)
                Line = re.sub("</w>", Word+"</w>", Line)
                #print(Line) 
                if "wn=" in Line: 
                    #print(Line)
                    SynsetID = re.findall("wn=.*\"", Line)[0]
                    SynsetNumber = int(SynsetID[4:-3])
                    SynsetPOS = SynsetID[-2:-1]
                    #print(SynsetID, SynsetPOS, SynsetNumber)
                    SynsetAbbID = ""
                    try:
                        SynsetAbbID = wn._synset_from_pos_and_offset(SynsetPOS, SynsetNumber)
                    except:
                        ""
                        #print("Error when trying to get synset name.")
                    SynsetAbbID = str(SynsetAbbID)
                    SynsetAbbID = SynsetAbbID[8:-2]
                    #print(SynsetAbbID)
                    Lexname = "XXX"
                    try:
                        Lexname = wn.synset(SynsetAbbID).lexname()
                    except:
                        #print("Error when trying to get lexname.")
                        LexErrCounter.update({"LexNameError":1})
                    #print(Lexname)
                    Line = re.sub("wn=(.*) >", "wnsyn=\\1 wnlex=\""+Lexname+"\">", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "wn=" not in Line and "<s" not in Line:
                    #print(Line)
                    Line = re.sub(" >", " wnsyn=\"xxx\" wnlex=\"xxx\">", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "<s" in Line:
                    #print(Line)
                    #Line = re.sub(" >", " wnsyn=\"xxx\" wnlex=\"xxx\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                
            
            if LexErrCounter["LexNameError"] > 0:
                print(str(LexErrCounter["LexNameError"]) + " lexname(s) could not be found in " + str(Filename))
            NewText.append("</s>\n</wrapper>")                
            NewText = ''.join(NewText)
            with open(WordnetFolder+Filename[:-4]+".xml", "w") as OutFile: 
                OutFile.write(NewText)
                
    print("Done.")
    


def annotate_fw(InPath, FreelingFolder, WordnetFolder, Lang):
    use_freeling(InPath, FreelingFolder, Lang)
    use_wordnet(FreelingFolder, WordnetFolder)



if __name__ == "__main__":
    annotate_fw(int(sys.argv[1]))
