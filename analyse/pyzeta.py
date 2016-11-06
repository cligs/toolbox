#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyzeta.py
# #cf



#=================================
# Import statements
#=================================

import os
import re
import glob
import pandas as pd
from collections import Counter
import itertools
import shutil
import pygal


#=================================
# Functions
#=================================

def merge_text(Path, File): 
    """
    Merge all texts from one group into one large text file.
    Creates less loss when splitting.
    """
    with open(File, 'wb') as OutFile:
        for File in glob.glob(Path):
            with open(File, 'rb') as ReadFile:
                shutil.copyfileobj(ReadFile, OutFile)


def read_file(File):
    """
    Read one text file per partition.
    """
    FileName,Ext = os.path.basename(File).split(".")
    with open(File, "r") as InFile: 
        Text = InFile.read()
    #print(Text)
    return Text, FileName


def prepare_text(Text):
    """
    Takes a text in string format and transforms and filters it. 
    Makes it lowercase, splits into tokens, discards tokens of length 1.
    Returns a list. 
    """
    Prepared = Text.lower()
    Prepared = re.split("\W", Prepared)
    Prepared = [Token for Token in Prepared if len(Token) > 1]
    #print(Prepared)
    return Prepared 


def save_seg(Seg, SegFile, SegsFolder): 
    """
    Function to save one segment to disk for sequential reading.
    """
    with open(SegsFolder+SegFile, "w") as OutFile: 
        OutFile.write(Seg)


def segment_text(Prepared, SegLength, Filename, SegsFolder):
    """
    Splits the whole text document into segments of fixed length; discards rest. 
    Also, reduces each segment to the set of different words in the segment. 
    """
    NumSegs = int(len(Prepared)/SegLength)
    #print("text length (prepared)", len(Prepared))
    #print("number of segments", NumSegs)
    for i in range(0,NumSegs): 
        Seg = Prepared[i*SegLength:(i+1)*SegLength]
        #print(len(Seg))
        Seg = list(set(Seg))
        #print(len(Seg))
        Seg = "\t".join(Seg)
        SegFile = Filename+"{:04d}".format(i)+".txt"
        save_seg(Seg, SegFile, SegsFolder)
    return NumSegs


def get_types(OnePrepared, TwoPrepared, Threshold):
    """
    Merges all prepared text and extracts the types with their frequency (Counter). 
    Filters the list of types based on their frequency and length in chars.
    A high frequency threshold may speed things up but information is lost. 
    """
    Types = Counter()
    Types.update(OnePrepared)
    Types.update(TwoPrepared)
    Types = {k:v for (k,v) in Types.items() if v > Threshold and len(k) > 1}
    #Set all values to zero.
    Types = dict.fromkeys(Types, 0)
    #print("number of types in collection (filtered)", len(list(Types.keys())))
    #print(list(itertools.islice(Types.items(), 0, 5)))
    return Types
    
       
def check_types(SegsPath, Types, NumSegs):
    """
    For each text segment in one group: 
    1. Read the file and split on the tab
    2. For each Type in the list of all Types, check whether it exists in the file.
    3. If it does, increase the value in the dict for this type by one.
    At the end, divide all dict values by the number of segments. 
    """
    Types = dict.fromkeys(Types, 0)
    for SegFile in glob.glob(SegsPath):
        with open(SegFile, "r") as InFile: 
            Seg = InFile.read()
            Seg = re.split("\t", Seg)
            for Type in Types:       ### TODO: this part is really slow ###
                if Type in Seg:
                    Types[Type] = Types[Type]+1
    Props = {k: v / NumSegs for k, v in Types.items()}
    return Props
                    

def get_zetas(Types, OneProps, TwoProps, ZetaFile):
    """
    Perform the actual Zeta calculation.
    Zeta = Proportion in Group One + (1-Proportion in Group 2) -1
    """
    AllResults = []
    for Type in Types:
        try:
            OneProp = OneProps[Type]
        except: 
            OneProp = 0
        try:
            TwoProp = TwoProps[Type]
        except: 
            TwoProp = 0
        Zeta = OneProp + (1-TwoProp) -1
        Result = {"type":Type, "one-prop":OneProp, "two-prop":TwoProp, "zeta":Zeta}
        AllResults.append(Result)
    AllResults = pd.DataFrame(AllResults)
    AllResults = AllResults[["type", "one-prop", "two-prop", "zeta"]]
    AllResults = AllResults.sort_values("zeta", ascending=False)
    print(AllResults.head(5))
    print(AllResults.tail(5))
    with open(ZetaFile, "w") as OutFile: 
        AllResults.to_csv(OutFile)


#=================================
# Main coordinating function
#=================================

def zeta(DataFolder,InputFolder,
         OnePath, TwoPath, 
         OneFile, TwoFile, 
         SegLength, SegsFolder, 
         Threshold, ZetaFile):
    """
    Python implementation of Craig's Zeta. 
    Status: proof-of-concept quality.
    """
    # Create necessary folders
    if not os.path.exists(InputFolder):
        os.makedirs(InputFolder)
    if not os.path.exists(SegsFolder):
        os.makedirs(SegsFolder)
    # Merge text files into two input files
    print("--merge_text (one and two)")
    merge_text(OnePath, OneFile)
    merge_text(TwoPath, TwoFile)
    # Load both text files       
    print("--read_file (one and two)")
    OneText, OneFileName = read_file(OneFile)
    TwoText, TwoFileName = read_file(TwoFile)
    # Prepare both text files           
    print("--prepare_text (one and two)")
    OnePrepared = prepare_text(OneText)
    TwoPrepared = prepare_text(TwoText)
    # Segment both text files
    print("--segment_text (one and two)")
    NumSegsOne = segment_text(OnePrepared, SegLength, OneFileName, SegsFolder)
    NumSegsTwo = segment_text(TwoPrepared, SegLength, TwoFileName, SegsFolder)
    print("  Number of segments (one, two)", NumSegsOne, NumSegsTwo)
    # Extract the list of selected types 
    print("--get_types (one)")
    Types = get_types(OnePrepared, TwoPrepared, Threshold)
    print("  Number of types", len(list(Types.keys())))
    # Check in how many segs each type is (one)
    print("--check_types (one)")
    OneProps = check_types(SegsFolder+"rm*.txt", Types, NumSegsOne)
    # Extract the list of selected types (repeat)
    print("--get_types (two)")
    Types = get_types(OnePrepared, TwoPrepared, Threshold)
    # Check in how many segs each type is (two)
    print("--check_types (two)")
    TwoProps = check_types(SegsFolder+"wk*.txt", Types, NumSegsTwo)
    # Calculate zeta for each type
    print("--get_zetas")
    get_zetas(Types, OneProps, TwoProps, ZetaFile)






#=================================
# Visualize zeta data
#=================================

zeta_style = pygal.style.Style(
  background='white',
  plot_background='white',
  font_family = "FreeSans",
  title_font_size = 20,
  legend_font_size = 16,
  label_font_size = 12,
  colors=["#1d91c0","#225ea8","#253494","#081d58", "#071746"])



def get_zetadata(ZetaFile, NumWords): 
    with open(ZetaFile, "r") as InFile: 
        ZetaData = pd.DataFrame.from_csv(InFile)
        #print(ZetaData.head())
        ZetaData.drop(["one-prop", "two-prop"], axis=1, inplace=True)
        ZetaData.sort_values("zeta", ascending=False, inplace=True)
        ZetaDataHead = ZetaData.head(NumWords)
        ZetaDataTail = ZetaData.tail(NumWords)
        ZetaData = ZetaDataHead.append(ZetaDataTail)
        ZetaData = ZetaData.reset_index(drop=True)
        #print(ZetaData)
        return ZetaData


def plot_zetadata(ZetaData, PlotFile, NumWords): 
    plot = pygal.HorizontalBar(style=zeta_style,
                               print_values=False,
                               print_labels=True,
                               show_legend=False,
                               range=(-1,1),
                               title="Kontrastive Analyse (Wikipedia vs. Romane)",
                               x_title="Craig's Zeta",
                               y_title="Je "+str(NumWords)+" Worte pro Sammlung"
                               )
    for i in range(len(ZetaData)):
        if ZetaData.iloc[i,1] > 0.8: 
            Color = "#4d9900"
        elif ZetaData.iloc[i,1] > 0.7: 
            Color = "#4d6f2a"
        elif ZetaData.iloc[i,1] > 0: 
            Color = "#4d5c3d"
        elif ZetaData.iloc[i,1] < -0.8: 
            Color = "#0044cc"
        elif ZetaData.iloc[i,1] < -0.7: 
            Color = "#1f4ead"
        elif ZetaData.iloc[i,1] < 0: 
            Color = "#3d588f"
        plot.add(ZetaData.iloc[i,0], [{"value":ZetaData.iloc[i,1], "label":ZetaData.iloc[i,0], "color":Color}])
    plot.render_to_file(PlotFile)


def plot_zeta(ZetaFile,
              NumWords,
              PlotFile): 
    print("--plot_zeta")
    ZetaData = get_zetadata(ZetaFile, NumWords)
    plot_zetadata(ZetaData, PlotFile, NumWords)

















