#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyzeta.py
# #cf

import pyzeta

#=================================
# Zeta Parameters
#=================================

SegLength = 2000
Threshold = 10
Mode = "tag"  # plain|tag|sel|posbigrams
Pos = ["x"] #Nc|Np|Vv|Rg|Ag etc.
Forms = "lemmas" # words|lemmas|pos
Stoplist = ["De", "Et", "...", "qu'", "Qu'", "-là", "-ci", "C'est-à-dire", "c'est-à-dire", "Rome", "aux", "Aux"]
Contrast = ["subgenre", "tragicomedie", "comedie"] # Category, Label1, Label2


#=================================
# Files and folders
#=================================
WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/scientia/"
InputFolder = WorkDir + "txt/"
MetadataFile = WorkDir + "metadata.csv"
DataFolder = WorkDir + "data/"


#=================================
# Functions
#=================================

# Calculate Zeta for words in two text collections
pyzeta.zeta(WorkDir, InputFolder, 
            MetadataFile, Contrast,
            DataFolder,
            SegLength, Threshold,
            Mode, Pos, Forms, Stoplist)


# Make a nice plot with some zeta data
ZetaFile = DataFolder + Contrast[1]+"-"+Contrast[2]+"_zeta-scores_segs-of-"+str(SegLength)+"-"+Mode+"-"+Forms+"-"+str(Pos[0])+".csv"
PlotFile = WorkDir + "zetas-scores_"+ Contrast[1]+"-"+Contrast[2]+"_segs-of-"+str(SegLength)+"-"+Mode+"-"+Forms+"-"+str(Pos[0])+".svg"
NumWords = 25   
pyzeta.plot_zeta(ZetaFile,
                 NumWords,
                 Contrast,
                 PlotFile)
















