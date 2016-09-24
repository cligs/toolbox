#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: model-and-coherence.py
# Author: #cf
# Version 0.2.0 (2016-09-24)


"""
Function to perform topic modeling with MALLET and assess topic coherence with Palmetto.
See: https://github.com/AKSW/Palmetto/wiki/How-Palmetto-can-be-used
"""


##################
# Parameters
##################


WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/wissenschaftsfilm/coherence/"

# MALLET general parameters
MalletPath = "/media/christof/data/repos/other/Mallet/bin/mallet"
SegsFolder = WorkDir + "5_segs-N/"
MalletFolder = WorkDir + "6_mallet/" 
MalletCorpus = MalletFolder + "corpus.mallet"
StoplistProject = WorkDir + "extras/en-lemma_stopwords-project.txt"

# Modeling parameters
AllNumTopics = ["10", "50", "100"] # list of strings
AllIterations = ["1000", "1001", "2000", "2001"] # list of strings
OptimizeInterval = "100"
NumTopWords = "12"

# For Topic Scores
TopicsWordsFile = MalletFolder + "topics-with-words.csv"
PalmettoPath = "/home/christof/Programs/palmetto/palmetto-0.1.0-jar-with-dependencies.jar"
IndexFolder = "/home/christof/Programs/palmetto/index-EN/wikipedia_bd"
TopicsFile = WorkDir + "topicsfile.txt"
ScoresFile = WorkDir + "scoresfile.csv"
AllRunsScoresFile = "AllRunsScores.csv"
Coherence = "C_A" # string: C_A|C_P|C_V|_NPMI|UCI|UMass
PalmettoType = "local" # local|webservice

##################
# Imports
##################

import os
import re
import csv
import glob
import pandas as pd
import numpy as np
import requests
import subprocess

##################
# Functions
##################


def mallet_import(MalletPath, SegsFolder, MalletFolder, MalletCorpus, StoplistProject):
    """
    Function to import text data into Mallet.
    Status: OK.
    """
    print("-- mallet_import.")    
    if not os.path.exists(MalletFolder):
        os.makedirs(MalletFolder)    
    TokenRegex = "'\p{L}[\p{L}\p{P}]*\p{L}'"
    command = MalletPath + " import-dir --input " + SegsFolder + " --output " + MalletCorpus + " --keep-sequence --token-regex " + TokenRegex + " --remove-stopwords TRUE --stoplist-file " + StoplistProject
    subprocess.call(command, shell=True)


def mallet_modeling(MalletPath, MalletCorpus, outfolder, NumTopics, OptimizeInterval, NumIterations, NumTopWords):
    """
    Function to perform topic modeling with Mallet.
    Status: OK.
    """
    print("-- mallet_modeling.")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)        
    #NumThreads = "4"
    DocTopicsMax = NumTopics
    word_topics_counts_file = outfolder + "words-by-topics.txt"
    topic_word_weights_file = outfolder + "word-weights.txt"
    output_topic_keys = outfolder + "topics-with-words.csv"
    output_doc_topics = outfolder + "topics-in-texts.csv"
    output_topic_state = outfolder + "topic_state.gz"
    
    command = MalletPath +" train-topics --input "+ MalletCorpus +" --num-topics "+ NumTopics +" --optimize-interval "+ OptimizeInterval +" --num-iterations " + NumIterations +" --num-top-words " + NumTopWords +" --word-topic-counts-file "+ word_topics_counts_file + " --topic-word-weights-file "+ topic_word_weights_file +" --output-state topic-state.gz"+" --output-topic-keys "+ output_topic_keys +" --output-doc-topics "+ output_doc_topics +" --doc-topics-max "+ DocTopicsMax + " --output-state " + output_topic_state
    subprocess.call(command, shell=True)


def make_topicsfile(TopicsWordsFile, TopicsFile):
    """
    Extracts the topic words from Mallet output for further treatment. 
    Status: OK. 
    """
    with open(TopicsWordsFile, "r") as InFile: 
        FileContent = pd.DataFrame.from_csv(InFile, header=None, sep="\t")
        TopicWords = FileContent.iloc[:,1]
        with open(TopicsFile, "w") as OutFile: 
            TopicWords.to_csv(OutFile, index=False)


def local_coherences(TopicsFile, PalmettoPath, IndexFolder, Coherence, ScoresFile): 
    """
    Calculate topic coherence scores using local Java Palmetto. 
    Status: OK.
    """
    print("-- local_coherences")
    PalmettoCall = "java -jar " + PalmettoPath +" "+ IndexFolder +" "+Coherence +" "+ TopicsFile + "> " + ScoresFile
    #print(PalmettoCall)
    subprocess.call(PalmettoCall, shell=True)



def compare_results(WorkDir): 
    """
    Function to read coherence scores from several runs and calculate the mean scores for each.
    Status: OK (but not very elegant)
    """
    AllScoresPath = WorkDir + "palmetto-scores*.csv" 
    AllRunsScores = [["parameters", "mean-score"]]
    for File in glob.glob(AllScoresPath): 
        Parameter = os.path.basename(File)[16:-4]
        OneRunScore = [Parameter]
        print(Parameter)
        with open(File, "r") as InFile:
            AllLines = InFile.read()
            AllLines = re.split("\n", AllLines)
            SingleScores = []
            for Line in AllLines[1:-1]:
                Line = re.split("[\t]", Line)
                print(Line)
                if Line[1]: 
                    OneScore = float(Line[1])
                    SingleScores.append(OneScore)
            print(SingleScores)
            MeanScore = np.mean(SingleScores)            
            OneRunScore.append(MeanScore)
        AllRunsScores.append(OneRunScore)
    print(AllRunsScores)
    return AllRunsScores
            
        
def web_coherences(TopicsFile, Coherence): 
    """
    Query the Palmetto webservice for topic coherence scores.
    Status: Kind of works, but unmaintained right now.
    """
    BaseURL = "http://palmetto.aksw.org/palmetto-webapp/service/"
    Connector = "?words="
    with open(TopicsFile, "r") as InFile: 
        AllTopicsWords = InFile.read()
        AllTopicsWords = re.split("\n", AllTopicsWords)
        AllScores = []
        for Words in AllTopicsWords[:-1]: 
            FullURL = BaseURL + Coherence + Connector + Words
            #print(FullURL)
            try:
                Result = requests.get(FullURL)
                Score = Result.text
                Score = float(Score)
                AllScores.append(Score)
            except Exception as exc:
                print(exc, "error")
        print(AllScores)
        return AllScores


def save_csv(AllScores, File): 
    """
    Save Palmetto webservice output to file.
    """
    with open(File, "a", newline="", encoding="utf8") as OutFile: 
        writer = csv.writer(OutFile, delimiter="\t")
        writer.writerow(AllScores)


def save_allrunsscores(AllRunsScores, AllRunsScoresFile): 
    """
    Save the parameters and mean coherence scores to file.
    Status: OK.
    """
    for Item in AllRunsScores: 
        with open(File, "w") as OutFile:       
            writer = csv.writer(OutFile)
            for Item in AllRunsScores: 
                writer.writerow(Item)
    

################
# Main function
################

def main(WorkDir, 
         MalletPath, 
         SegsFolder, 
         MalletFolder, 
         MalletCorpus, 
         StoplistProject,
         AllNumTopics, 
         OptimizeInterval, 
         AllIterations, 
         NumTopWords, 
         TopicsWordsFile,
         TopicsFile,
         PalmettoPath,
         IndexFolder,
         Coherence,
         PalmettoType,
         AllRunsScoresFile):
    """
    Main / coordinating function for "model-and-coherence".
    Status: OK.
    """
    print("Launched.")
    #mallet_import(MalletPath, SegsFolder, MalletFolder, MalletCorpus, StoplistProject)
    for NumTopics in AllNumTopics:
        for NumIterations in AllIterations: 
            print("Running with", NumTopics, "topics and",  NumIterations, "iterations.")
            mallet_modeling(MalletPath, MalletCorpus, MalletFolder, NumTopics, OptimizeInterval, NumIterations, NumTopWords)
            make_topicsfile(TopicsWordsFile, TopicsFile)
            if PalmettoType == "local":
                ScoresFile = "palmetto-scores_"+NumTopics+"tp-"+NumIterations+"it.csv"
                local_coherences(TopicsFile, PalmettoPath, IndexFolder, Coherence, ScoresFile)
            elif PalmettoType == "webservice": 
                AllScores = web_coherences(NumTopics, TopicsFile, Coherence)
                save_csv(AllScores, ScoresFile)
    AllRunsScores = compare_results(WorkDir)
    save_allrunsscores(AllRunsScores, AllRunsScoresFile)

    print("Done.")
    

main(WorkDir, 
     MalletPath, 
     SegsFolder, 
     MalletFolder, 
     MalletCorpus, 
     StoplistProject, 
     AllNumTopics, 
     OptimizeInterval, 
     AllIterations, 
     NumTopWords, 
     TopicsWordsFile,
     TopicsFile,
     PalmettoPath, 
     IndexFolder, 
     Coherence,
     PalmettoType,
     AllRunsScoresFile)
