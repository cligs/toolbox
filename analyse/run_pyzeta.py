#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyzeta.py
# #cf

import pyzeta

#=================================
# Zeta Parameters
#=================================

SegLength = 5000
Threshold = 100


#=================================
# Files and folders
#=================================
WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/zeta/"
DataFolder = WorkDir + "data0100MB/"
InputFolder = WorkDir + "input0100MB/"
OnePath = DataFolder + "files1/*.txt"
TwoPath = DataFolder + "files2/*.txt"
OneFile = InputFolder + "rm0100.txt"
TwoFile = InputFolder + "wk0100.txt"
SegsFolder = WorkDir + "segs-of-"+str(SegLength)+"/"
ZetaFile = WorkDir + "zetas-scores_segs-of-"+str(SegLength)+".csv"


#=================================
# Functions
#=================================

# Calculate Zeta for words in two text collections
#pyzeta.zeta(DataFolder, InputFolder,
#            OnePath, TwoPath, 
#            OneFile, TwoFile, 
#            SegLength, SegsFolder, 
#            Threshold, ZetaFile)


# Make a nice plot with some zeta data
PlotFile = WorkDir + "zetas-scores_segs-of-"+str(SegLength)+".svg"
NumWords = 30   
pyzeta.plot_zeta(ZetaFile,
                 NumWords,
                 PlotFile)
















