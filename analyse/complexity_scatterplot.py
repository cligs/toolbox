#!/usr/bin/env python3
# Filename: sentencelength.py

"""
# Create scatterplot from vocabulary richness data.
"""


# Import statements

import pandas as pd
import pygal
from pygal.style import Style
from pygal.style import BlueStyle
from pygal.style import TurquoiseStyle
from pygal.style import LightSolarizedStyle
from pygal.style import CleanStyle
from pygal.style import RedBlueStyle


# Parameter definitions

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/simenon/complexity/"
DataFile = WorkDir+"results_RandomWindow-5000.csv"
MetadataFile = WorkDir+"metadata.csv"
Analysis = "tout" # sim|tout
GraphFile = WorkDir+Analysis+"_"+"YEARxDirect.svg"


# Functions

def read_data(File):
    with open(File,"r") as InFile:
        Data = pd.DataFrame.from_csv(InFile)
        #print(Data.head(6))
        return Data

def merge_data(Data, Metadata):
    AllData = pd.merge(Data, Metadata, on="idno")
    #print(AllData.head(3))
    return AllData 


def make_tout_xydata(AllData): 
    #print(AllData)
    GroupedData = AllData.groupby("corpus")
    SimData = GroupedData.get_group("simenon")
    ContData = GroupedData.get_group("contemporains")
    SimPoints = []  
    #print(ContData)
    for i in range(0,len(SimData)): 
        XY = (SimData.iloc[i,14], SimData.iloc[i,8])  
        Label = SimData.iloc[i,11]+": "+SimData.iloc[i,13]+" ("+str(SimData.iloc[i,14])+")" # author_title_year
        SimPoint = {"value" : XY, "label" : Label}
        SimPoints.append(SimPoint)
    ContPoints = []    
    for i in range(0,len(ContData)): 
        XY = (ContData.iloc[i,14], ContData.iloc[i,8])
        Label = ContData.iloc[i,11]+": "+ContData.iloc[i,13]+" ("+str(ContData.iloc[i,14])+")"
        ContPoint = {"value" : XY, "label" : Label}
        ContPoints.append(ContPoint)
    return SimPoints, ContPoints

def make_sim_xydata(AllData): 
    #print(AllData)
    GroupedData = AllData.groupby("cf-class")
    MaigData = GroupedData.get_group("maigr")
    DursData = GroupedData.get_group("romans")
    AutoData = GroupedData.get_group("autob")
    #print(MaigData)
    MaigPoints = []  
    for i in range(0,len(MaigData)): 
        XY = (MaigData.iloc[i,14], MaigData.iloc[i,8])  
        Label = MaigData.iloc[i,11]+": "+MaigData.iloc[i,13]+" ("+str(MaigData.iloc[i,14])+")" # author_title_year
        MaigPoint = {"value" : XY, "label" : Label}
        MaigPoints.append(MaigPoint)
    DursPoints = []    
    for i in range(0,len(DursData)): 
        XY = (DursData.iloc[i,14], DursData.iloc[i,8])
        Label = DursData.iloc[i,11]+": "+DursData.iloc[i,13]+" ("+str(DursData.iloc[i,14])+")"
        DursPoint = {"value" : XY, "label" : Label}
        DursPoints.append(DursPoint)
    AutoPoints = []    
    for i in range(0,len(AutoData)): 
        XY = (AutoData.iloc[i,14], AutoData.iloc[i,8])
        Label = AutoData.iloc[i,11]+": "+AutoData.iloc[i,13]+" ("+str(AutoData.iloc[i,14])+")"
        AutoPoint = {"value" : XY, "label" : Label}
        AutoPoints.append(AutoPoint)
    return MaigPoints, DursPoints, AutoPoints

my_style = Style(
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
  colors=('#002699', '#006600', '#007acc') # blue-green
  )


def make_tout_xyplot(SimPoints, ContPoints, GraphFile): 
    chart = pygal.XY(x_label_rotation=300,
                     stroke=False,
                     #range = (0.36, 0.56),
                     #xrange=(1900, 2000),
                     title="Simenon und Zeitgenossen (n=554)",
                     x_title="Erscheinungsjahr",
                     y_title="Anteil direkter Rede",
                     show_x_guides=True,
                     show_y_guides=True,
                     legend_at_bottom=True,
                     pretty_print=True,
                     style=my_style)                
    chart.add("Contemporains", ContPoints, dots_size=4)
    chart.add("Simenon", SimPoints, dots_size=4)
    chart.render_to_file(GraphFile)



def make_sim_xyplot(MaigPoints, DursPoints, AutoPoints, GraphFile): 
    chart = pygal.XY(x_label_rotation=300,
                     stroke=False,
                     #range = (0.36, 0.56),
                     #xrange=(1920, 1990),
                     title="Georges Simenon (n=127)",
                     x_title="Erscheinungsjahr",
                     y_title="Anteil direkter Rede",
                     show_x_guides=True,
                     show_y_guides=True,
                     legend_at_bottom=True,
                     pretty_print=True,
                     style=my_style)
    chart.add("Maigret", MaigPoints, dots_size=4)
    chart.add("Durs", DursPoints, dots_size=4)
    chart.add("Autob.", AutoPoints, dots_size=4)
    chart.render_to_file(GraphFile)


# Coordination function
def scatter_time(DataFile, MetadataFile, GraphFile, Analysis):
    File = MetadataFile
    Data = read_data(File)
    Metadata = Data 
    File = DataFile
    Data = read_data(File)
    AllData = merge_data(Data, Metadata)
    if Analysis == "tout": 
        SimPoints, ContPoints = make_tout_xydata(AllData)
        make_tout_xyplot(SimPoints, ContPoints, GraphFile)
    elif Analysis == "sim": 
        MaigPoints, DursPoints, AutoPoints = make_sim_xydata(AllData)
        make_sim_xyplot(MaigPoints, DursPoints, AutoPoints, GraphFile)
    
scatter_time(DataFile, MetadataFile, GraphFile, Analysis)






























