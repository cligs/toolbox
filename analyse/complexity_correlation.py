#!/usr/bin/env python3
# Filename: sentencelength.py

"""
# Create scatterplot from vocabulary richness data.
"""


# Import statements

import pandas as pd
import scipy.stats.stats as stats
import itertools as itt
import csv


# Parameter definitions

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/simenon/complexity/"
DataFile = WorkDir+"results_RandomWindow-5000.csv"
MetadataFile = WorkDir+"metadata.csv"
ResultFile = WorkDir+"correlations.csv"

# Functions

def read_data(File):
    with open(File,"r") as InFile:
        Data = pd.DataFrame.from_csv(InFile)
        return Data

def merge_data(Data, Metadata):
    AllData = pd.merge(Data, Metadata, on="idno")
    #print(AllData.head(3))
    return AllData 

def check_correlations(AllData):
    AllCorrs = [["vector1", "vector2", "correlation", "p-value"]]
    AllHeads = ["NumWords", "NumSents", "SLMean", "SLMedian", "SLStdev", "TTR-mean", "TTR-stdev", "BVR-mean", "BVR-stdev", "DirectPerc", "pub-year", "crt-year"]
    Combinations = list(itt.combinations(AllHeads, 2))
    print(Combinations[0])
    for Heads in Combinations: 
        Corr = stats.pearsonr(AllData.loc[:,Heads[0]], AllData.loc[:,Heads[1]])
        Result = [Heads[0], Heads[1], Corr[0], Corr[1]]
        print(Result)
        AllCorrs.append(Result)

#    for Head1 in AllHeads:        
#        Vector1 = AllData.loc[:,Head1]
#        for Head2 in AllHeads: 
#            Vector2 = AllData.loc[:,Head2]
#            Result = [Head1, Head2, Corr[0], Corr[1]]
            #print(Result)
#            AllCorrs.append(Result)
    return AllCorrs
    
def save_data(AllCorrs, ResultFile): 
    with open(ResultFile, "w") as OutFile:
        writer = csv.writer(OutFile)
        writer.writerows(AllCorrs)

# Coordination function
def test_correlation(DataFile, MetadataFile, ResultFile):
    File = MetadataFile
    Data = read_data(File)
    Metadata = Data 
    File = DataFile
    Data = read_data(File)
    AllData = merge_data(Data, Metadata)
    AllCorrs = check_correlations(AllData)
    save_data(AllCorrs, ResultFile)
    
test_correlation(DataFile, MetadataFile, ResultFile)






























