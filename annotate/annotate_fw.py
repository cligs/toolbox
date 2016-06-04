#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: annotate_fw.py
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


def use_freeling(FreelingPath, InPath, FreelingFolder, Lang="fr"): 
    """
    Call Freeling "analyze".
    Authors: #cf (#uh).
    """
    print("use_freeling...")
    
    if Lang not in ["fr","es"]:
        raise ValueError("Please indicate one of the following as language: 'fr', 'es'")
        
    if not os.path.exists(FreelingFolder):
        os.makedirs(FreelingFolder)

    for File in glob.glob(InPath): 
        Filename = os.path.basename(File)
        OutPath = FreelingFolder + Filename[:-4] + ".xml" 
        Command = "analyze -f " + Lang + ".cfg --outlv tagged  --sense ukb --output xml < " + File + " > " + OutPath   
        #print(Command)
        subprocess.call(Command, shell=True)

    print("Done.")


def use_wordnet(FreelingFolder, WordnetFolder, Lang):
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
                    SynsetAbbID = ""
                    try:
                        SynsetAbbID = wn._synset_from_pos_and_offset(SynsetPOS, SynsetNumber)
                    except:
                        ""
                        #print("Error when trying to get synset name.")
                    SynsetAbbID = str(SynsetAbbID)
                    SynsetAbbID = SynsetAbbID[8:-2]
                    #print(SynsetAbbID)
                    Lexname = "xxx"
                    try:
                        Lexname = wn.synset(SynsetAbbID).lexname()
                    except:
                        #print("Error when trying to get lexname.")
                        LexErrCounter.update({"LexNameError":1})
                    #print(Lexname)
                    Line = re.sub("wn=(.*) >", "wnsyn="+"\\1 wnlex=\""+Lexname+"\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "wn=" not in Line and "sentence" not in Line:
                    #print(Line)
                    Line = re.sub(" >", " wnsyn=\"xxx\" wnlex=\"xxx\" >", Line)
                    #print(Line)
                    NewText.append(Line)
                elif "sentence" in Line:
                    #print(Line)
                    Line = re.sub(" >", " wnsyn=\"xxx\" wnlex=\"xxx\" >", Line)
                    #print(Line)
                    NewText.append(Line)
            
            if LexErrCounter["LexNameError"] > 0:
                print(str(LexErrCounter["LexNameError"]) + " lexname(s) could not be found in " + str(Filename))

            NewText = ''.join(NewText)
            NewText = NewText + "</sentence>\n</body>"
            NewText = re.sub("<token id","<w n", NewText)
            NewText = re.sub("</token>","</w>", NewText)
            NewText = re.sub("<sentence id","<s n", NewText)
            NewText = re.sub("</sentence>","</s>", NewText)
            NewText = re.sub("<div id","<div xml:id", NewText)




            if Lang == "fr": 
                # Expand tags
                # Nouns
                NewText = re.sub("(tag=\"NCFS.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"NCFP.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"NCFN.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"NCF0.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"NCMS.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"NCMP.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"NCMN.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"NCM0.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"NCCS.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"NCCP.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"NCCN.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"NCC0.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"NCNS.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"NCNP.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"NCNN.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"neuter\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"NCN0.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"NP.*?\")", "\\1 pos=\"noun\" type=\"common\" gen=\"xxx\" num=\"xxx\"", NewText)

                # Verbs                
                NewText = re.sub("(tag=\"VM...SF\")", "\\1 pos=\"verb\" type=\"main\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VM...PF\")", "\\1 pos=\"verb\" type=\"main\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VM...0F\")", "\\1 pos=\"verb\" type=\"main\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VM...SM\")", "\\1 pos=\"verb\" type=\"main\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VM...PM\")", "\\1 pos=\"verb\" type=\"main\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VM...0M\")", "\\1 pos=\"verb\" type=\"main\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VM...SC\")", "\\1 pos=\"verb\" type=\"main\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VM...PC\")", "\\1 pos=\"verb\" type=\"main\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VM...0C\")", "\\1 pos=\"verb\" type=\"main\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VM...SN\")", "\\1 pos=\"verb\" type=\"main\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VM...PN\")", "\\1 pos=\"verb\" type=\"main\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VM...0N\")", "\\1 pos=\"verb\" type=\"main\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VM...S0\")", "\\1 pos=\"verb\" type=\"main\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VM...P0\")", "\\1 pos=\"verb\" type=\"main\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VM...00\")", "\\1 pos=\"verb\" type=\"main\" gen=\"xxx\" num=\"xxx\"", NewText)

                NewText = re.sub("(tag=\"VA...SF\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VA...PF\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VA...0F\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VA...SM\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VA...PM\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VA...0M\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VA...SC\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VA...PC\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VA...0C\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VA...SN\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VA...PN\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VA...0N\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VA...00\")", "\\1 pos=\"verb\" type=\"auxiliary\" gen=\"xxx\" num=\"xxx\"", NewText)

                NewText = re.sub("(tag=\"VS...SF\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VS...PF\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VS...0F\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VS...SM\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VS...PM\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VS...0M\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VS...SC\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VS...PC\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VS...0C\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VS...SN\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"VS...PN\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"VS...0N\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"VS...00\")", "\\1 pos=\"verb\" type=\"semiaux\" gen=\"xxx\" num=\"xxx\"", NewText)

                NewText = re.sub("(tag=\"V0...SF\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"V0...PF\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"V0...0F\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"V0...SM\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"V0...PM\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"V0...0M\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"V0...SC\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"V0...PC\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"V0...0C\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"V0...SN\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"V0...PN\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"V0...0N\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"V0...00\")", "\\1 pos=\"verb\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)

                # Adjectives
                NewText = re.sub("(tag=\"AO.FS.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AO.FP.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AO.FN.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AO.F0.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AO.MS.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AO.MP.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AO.MN.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AO.M0.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AO.CS.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AO.CP.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AO.CN.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AO.C0.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AO.0S.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AO.0P.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AO.0N.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AO.00.*?\")", "\\1 pos=\"adj\" type=\"ordinal\" gen=\"xxx\" num=\"xxx\"", NewText)
                
                NewText = re.sub("(tag=\"AQ.FS.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AQ.FP.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AQ.FN.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AQ.F0.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AQ.MS.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AQ.MP.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AQ.MN.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AQ.M0.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AQ.CS.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AQ.CP.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AQ.CN.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AQ.C0.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AQ.0S.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AQ.0P.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AQ.0N.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AQ.00.*?\")", "\\1 pos=\"adj\" type=\"qualif\" gen=\"xxx\" num=\"xxx\"", NewText)

                NewText = re.sub("(tag=\"AP.FS.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AP.FP.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AP.FN.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AP.F0.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AP.MS.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AP.MP.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AP.MN.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AP.M0.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AP.CS.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AP.CP.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AP.CN.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AP.C0.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"AP.0S.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"AP.0P.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"AP.0N.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"AP.00.*?\")", "\\1 pos=\"adj\" type=\"poss\" gen=\"xxx\" num=\"xxx\"", NewText)

                NewText = re.sub("(tag=\"A0.FS.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"A0.FP.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"A0.FN.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"A0.F0.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"A0.MS.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"A0.MP.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"A0.MN.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"A0.M0.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"A0.CS.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"A0.CP.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"A0.CN.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"A0.C0.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"A0.0S.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"A0.0P.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"A0.0N.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"A0.00.*?\")", "\\1 pos=\"adj\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)

                # Pronouns
                NewText = re.sub("(tag=\"P..FS.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"P..FP.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"P..FN.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"P..F0.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"P..MS.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"P..MP.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"P..MN.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"P..M0.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"P..CS.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"P..CP.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"P..CN.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"P..C0.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"P..NS.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"P..NP.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"P..NN.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"P..N0.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"P..0S.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"P..0P.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"P..0N.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"P..00.*?\")", "\\1 pos=\"pron\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)

                # Determiner
                NewText = re.sub("(tag=\"D..FS.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"feminine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"D..FP.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"feminine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"D..FN.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"feminine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"D..F0.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"feminine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"D..MS.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"masculine\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"D..MP.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"masculine\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"D..MN.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"masculine\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"D..M0.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"masculine\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"D..CS.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"common\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"D..CP.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"common\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"D..CN.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"common\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"D..C0.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"common\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"D..NS.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"neuter\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"D..NP.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"neuter\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"D..NN.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"neuter\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"D..N0.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"neuter\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"D..0S.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"xxx\" num=\"singular\"", NewText)
                NewText = re.sub("(tag=\"D..0P.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"xxx\" num=\"plural\"", NewText)
                NewText = re.sub("(tag=\"D..0N.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"xxx\" num=\"neuter\"", NewText)
                NewText = re.sub("(tag=\"D..00.\")", "\\1 pos=\"det\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)

                # Others
                NewText = re.sub("(tag=\"CC\")", "\\1 pos=\"conj\" type=\"coord\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"CS\")", "\\1 pos=\"conj\" type=\"subord\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"RG.*?\")", "\\1 pos=\"adverb\" type=\"general\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"RN.*?\")", "\\1 pos=\"adverb\" type=\"negative\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"SP.*?\")", "\\1 pos=\"prep\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"F.*?\")", "\\1 pos=\"punc\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"Z.*?\")", "\\1 pos=\"number\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"W.*?\")", "\\1 pos=\"date\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                NewText = re.sub("(tag=\"I.*?\")", "\\1 pos=\"interj\" type=\"xxx\" gen=\"xxx\" num=\"xxx\"", NewText)
                #NewText = re.sub("", "", NewText)
            
                # Transform entities            
                NewText = re.sub("&apos;", "'", NewText)

                # Contractions 
                # Not sure how to deal with them           
            
            with open(WordnetFolder+Filename[:-4]+"_a.xml", "w") as OutFile: 
                OutFile.write(NewText)
                
    print("Done.")
    


def annotate_fw(FreelingPath, InPath, FreelingFolder, WordnetFolder, Lang):
    #use_freeling(FreelingPath, InPath, FreelingFolder, Lang)
    use_wordnet(FreelingFolder, WordnetFolder, Lang)



if __name__ == "__main__":
    annotate_fw(int(sys.argv[1]))
