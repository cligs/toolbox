#!/usr/bin/env python3
# Filename: sentencelength.py

"""
# Analyse complexity data through visualisation and statistical tests. 
"""


# Import statements

import pandas as pd
import numpy as np
import scipy.stats as stats
import itertools as itt
import pygal
import csv


# Directories and file names for input
WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/simenon/analyses/"
ComplexityFile = WorkDir+"data_RandomWindow-5000.csv"
EntropyFile = WorkDir+"data_entropy.csv"
MetadataFile = WorkDir+"data_metadata.csv"

# Data selection: filter (0,1); splitting (2,3), filter (4,5)
SelectionType = "filtered-two" 
OneFilter = ["genre", "novel", "subcorpus", "contemporains", "creation", list(range(1925, 1975))]
TwoFilter = ["genre", "novel", "subcorpus", "simenon", "creation", list(range(1925, 1975))]
Dimensions = ["creation", "SLMean"]

# Graph style
my_style = pygal.style.Style(
  background='white',
  plot_background='white',
  foreground='#282828',
  foreground_strong='#000000',
  foreground_subtle='#282828',
  opacity='.6',
  opacity_hover='.9',
  transition='100ms ease-in',
  font_family = "FreeSans",
  title_font_size = 20,
  legend_font_size = 16,
  label_font_size = 12,
  #colors=('#000000', '#707070', '#E0E0E0') # bw
  colors=('#002699', '#006600', '#b30000') # blue-green-red
  )

# GraphTitles
MainTitle = OneFilter[1]+": "+OneFilter[3]+" vs "+ TwoFilter[3]
XTitle = Dimensions[0]
YTitle = Dimensions[1]

# Base filenames for output
GraphFile = OneFilter[1]+"-"+OneFilter[3]+"-vs-"+ TwoFilter[3]+"_"+Dimensions[0]+"-"+Dimensions[1]+"_scatterplot.svg"
CorrelationsFile = OneFilter[1]+"-"+OneFilter[3]+"-vs-"+ TwoFilter[3]+"_correlations.csv"
SignificanceFile = OneFilter[1]+"-"+OneFilter[3]+"-vs-"+ TwoFilter[3]+"_"+Dimensions[0]+"-"+Dimensions[1]+"_significances.csv"



# Functions

def read_data(File):
    with open(File,"r") as InFile:
        Data = pd.DataFrame.from_csv(InFile)
        return Data

def merge_data(ComplexityFile, EntropyFile, MetadataFile):
    ComplexityData = read_data(ComplexityFile)
    EntropyData = read_data(EntropyFile)
    Metadata = read_data(MetadataFile)
    AllData = pd.merge(ComplexityData, EntropyData, on="idno")
    AllData = pd.merge(AllData, Metadata, on="idno")
    #print(AllData.head())
    with open("data_mastermatrix.csv", "w") as OutFile:
        print("Saving:", "data_mastermatrix.csv")
        AllData.to_csv(OutFile)
    return AllData 

def save_data(Results, File): 
    print("Saving:", File)
    with open(File, "w") as OutFile:
        writer = csv.writer(OutFile)
        writer.writerows(Results)


def filter_two_data(AllData, OneFilter, TwoFilter): 
    """
    # Filter out two series of subsets from all of the data for visualisation and tests. 
    # Status: ok, but redundant code could be simplified. 
    """
    print(list(AllData.columns.values))
    OneData = AllData
    OneData = OneData[OneData[OneFilter[0]].isin([OneFilter[1]])]
    OneData = OneData[OneData[OneFilter[2]].isin([OneFilter[3]])]
    OneData = OneData[OneData[OneFilter[4]].isin(OneFilter[5])]
    print("OneData:", len(OneData), "items.")
    #print(OneData)
    TwoData = AllData
    TwoData = TwoData[TwoData[TwoFilter[0]].isin([TwoFilter[1]])]
    TwoData = TwoData[TwoData[TwoFilter[2]].isin([TwoFilter[3]])]
    TwoData = TwoData[TwoData[TwoFilter[4]].isin(TwoFilter[5])]
    print("TwoData:", len(TwoData), "items.")
    #print(TwoData)
    return OneData, TwoData


def make_two_points(OneData, TwoData, Dimensions):
    """
    From the filtered data, make a dictionary of data points for pygal scatterplot.
    Status: ok; redundant code could be simplified.
    """
    OnePoints = []
    Xiloc = OneData.columns.get_loc(Dimensions[0])
    Yiloc = OneData.columns.get_loc(Dimensions[1])
    Label1iloc = OneData.columns.get_loc("author")
    Label2iloc = OneData.columns.get_loc("title")
    Label3iloc = OneData.columns.get_loc("creation")
    for i in range(0,len(OneData)): 
        XY = (OneData.iloc[i,Xiloc], OneData.iloc[i,Yiloc])  
        Label = OneData.iloc[i,Label1iloc]+": "+OneData.iloc[i,Label2iloc]+" ("+str(OneData.iloc[i,Label3iloc])+")" # author_title_year
        OnePoint = {"value" : XY, "label" : Label}
        OnePoints.append(OnePoint)
    TwoPoints = []    
    for i in range(0,len(TwoData)): 
        XY = (TwoData.iloc[i,Xiloc], TwoData.iloc[i,Yiloc])
        Label = TwoData.iloc[i,Label1iloc]+": "+TwoData.iloc[i,Label2iloc]+" ("+str(TwoData.iloc[i,Label3iloc])+")"
        TwoPoint = {"value" : XY, "label" : Label}
        TwoPoints.append(TwoPoint)
    return OnePoints, TwoPoints


def make_two_plot(OnePoints, TwoPoints, OneFilter, TwoFilter, GraphFile, MainTitle, XTitle, YTitle): 
    """
    # Make a scatterplot with two series of data. 
    # Status: ok, but get correct series label automatically.
    """
    chart = pygal.XY(x_label_rotation=300,
                     stroke=False,
                     logarithmic=False,
                     #range = (0.36, 0.56),
                     #xrange=(1920, 1990),
                     title=MainTitle,
                     x_title=XTitle,
                     y_title=YTitle,
                     show_x_guides=True,
                     show_y_guides=True,
                     legend_at_bottom=True,
                     pretty_print=True,
                     style=my_style)
    chart.add(OneFilter[3], OnePoints, dots_size=4)
    chart.add(TwoFilter[3], TwoPoints, dots_size=4)
    #chart.add("Autob.", AutoPoints, dots_size=4)
    print("Saving:", GraphFile)
    chart.render_to_file(GraphFile)


def test_mannwhitney(OneData, TwoData, OneFilter, TwoFilter, Dimensions):
    """
    # Performs the Mann-Whitney-U-test for two independent samples that may not be normally distributed. 
    # See: http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    # Status: Ok, but not entirely confident all is correct.
    """
    Results = [["feature", "category", "group1", "group2", "mw-statistic", "p-value", "mean1", "mean2", "ratio-1/2"]]
    Significance =  stats.mannwhitneyu(OneData.loc[:,Dimensions[1]], TwoData.loc[:,Dimensions[1]], alternative="two-sided")
    Result = [Dimensions[1], OneFilter[2], OneFilter[3], TwoFilter[3], Significance[0], Significance[1]]
    MeanOne = np.mean(OneData.loc[:,Dimensions[1]])
    MeanTwo = np.mean(TwoData.loc[:,Dimensions[1]])
    Ratio12 = MeanOne/MeanTwo
    Result.extend([MeanOne, MeanTwo, Ratio12])
    Results.append(Result)
    return Results


# Correlation test
def check_correlations(OneData, TwoData):
    """
    # Function that checks for correlations between the various measures implemented in "complexity_calculations.py". 
    # Calculates the correlations on all of the selected data (neither all data, nor each series separately).
    # See: http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html#scipy.stats.pearsonr
    # Status: ok, but solution to check OneData, TwoData, BothData in one go would be nice. 
    """
    BothData = OneData.append(TwoData)
    AllCorrs = [["vector1", "vector2", "correlation", "p-value"]]
    AllHeads = ["NumWords", "NumSents", "SLMean", "SLMedian", "SLStdev", "TTR-mean", "TTR-stdev", "BVR-mean", "BVR-stdev", "DirectPerc", "jsd", "entropy", "publication", "creation"]
    Combinations = list(itt.combinations(AllHeads, 2))
    #print(Combinations[0])
    for Heads in Combinations: 
        Corr = stats.pearsonr(BothData.loc[:,Heads[0]], BothData.loc[:,Heads[1]])
        Result = [Heads[0], Heads[1], Corr[0], Corr[1]]
        #print(Result)
        AllCorrs.append(Result)
        Results = AllCorrs
    return Results



# Coordination function
def complexity_analyses(DataFile, 
                        EntropyFile, 
                        MetadataFile, 
                        SelectionType,
                        OneFilter,
                        TwoFilter,
                        Dimensions,
                        GraphFile,
                        MainTitle,
                        XTitle,
                        YTitle,
                        CorrelationsFile, 
                        SignificanceFile):
    AllData = merge_data(DataFile, EntropyFile, MetadataFile)
    if SelectionType == "filtered-two": 
        OneData, TwoData = filter_two_data(AllData, OneFilter, TwoFilter)
        OnePoints, TwoPoints = make_two_points(OneData, TwoData, Dimensions)
        make_two_plot(OnePoints, TwoPoints, OneFilter, TwoFilter, GraphFile, MainTitle, XTitle, YTitle)
        Significance = test_mannwhitney(OneData, TwoData, OneFilter, TwoFilter, Dimensions)
        save_data(Significance, SignificanceFile)
        Correlations = check_correlations(OneData,TwoData)
        save_data(Correlations, CorrelationsFile)
    
                
    
complexity_analyses(ComplexityFile, 
                    EntropyFile, 
                    MetadataFile, 
                    SelectionType,
                    OneFilter,
                    TwoFilter,
                    Dimensions,
                    GraphFile,
                    MainTitle,
                    XTitle,
                    YTitle,
                    CorrelationsFile, 
                    SignificanceFile)






























