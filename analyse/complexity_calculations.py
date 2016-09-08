# ./bin/env python3
# calculate_ttr.py
# author: #cf

"""
# Calculate various measures of textual complexity in a collection of texts.
#
# Currently implemented: 
# * type-token-ration (based on multiple samples; mean, standard deviation); 
# * basic vocabulary ratio (based on multiple samples; mean, standard deviation);
# * sentence length (based on full text; mean, median, standard deviation).
# * Proportion of direct speech (very simple approximation for French text)
# * Data from FJ's JSD and entropy script can be added.
#
# For all of these, you can use several sampling methods: 
# * a moving window of fixed length
# * drawing words at random to build samples
# * drawing random starting points for windows of fixed length
#
# Requirements
# * Python 3.4 (or higher I guess) and TreeTagger installed
# Collection of text in plain text format
# Some metadata, like author or year for each text, in a CSV file.
# Filenames are identifiers in the metadata table
# For the BVR score: the file "liste-brunet.csv" for French, containing the 1500 most frequent words in French.
"""

import re
import os
import glob
import pandas as pd
import numpy as np
from collections import Counter
import random
import sys

#=======================
# Parameters / Settings
#=======================

WorkDir = "/"
InPath = WorkDir+"txt/*.txt"
TestType = "RandomWindow" # MovingWindow|RandomSample|RandomWindow
UnitLength = 5000
BasicVocab = WorkDir+"data_1500motsFR.csv"
ResultsFile = WorkDir+"data_"+TestType+"-"+str(UnitLength)+".csv"


#====================
# Functions
#====================

def read_text(File): 
    with open(File, "r") as InFile: 
        Text = InFile.read()
        return Text

def prepare_text(Text): 
    Text = Text.lower()
    Text = re.sub("[,\.;:!?«»]","", Text)   
    Text = re.sub("-- ","", Text)   
    Text = re.split("\W", Text)
    Text = [x for x in Text if x]
    return Text

def get_lengths(Text):
    Paras = re.split("\n", Text)
    LengthsWords = []
    for Para in Paras:
        #print(Para,"\n")
        if len(Para) > 2: 
            Sents = re.split("[\.?!]", Para)
            for Sent in Sents:
                if len(Sent) > 2:
                    Sent = re.sub("[\.,!?:;«»]"," ", Sent)
                    Sent = re.sub("[-]{2,4}"," ", Sent)
                    Sent = re.sub("[ ]{2,4}"," ", Sent)
                    Sent = re.sub("\t"," ", Sent)
                    Sent = Sent.strip()
                    #print(Sent)
                    Words = re.split("[\W'-]", Sent)
                    #print(Words)
                    LengthWords = len(Words)
                    LengthsWords.append(LengthWords)
    #print(LengthsWords)
    return LengthsWords

def get_sent_stats(LengthsWords, Idno): 
    """
    # Calculates some basic sentence length statistics. 
    # Status: Ok, but add IQR and 25-percentile, 75-percentile
    """
    NumWords = sum(LengthsWords)
    NumSents = len(LengthsWords)
    SentLenMean = np.mean(LengthsWords)
    SentLenMedian = np.median(LengthsWords)
    SentLenStdev = np.std(LengthsWords)
    SentLenVarc = SentLenStdev / SentLenMean
    SentStats = [Idno, NumWords, NumSents, SentLenMean, SentLenMedian, SentLenStdev, SentLenVarc]
    #SentStats = pd.Series(Stats, name=Idno)
    return SentStats

def get_direct_prop(Text):
    Paras = re.split("\n", Text)
    OtherWords = 0
    DirectWords = 0
    for Para in Paras:
        if "--" in Para[0:2]:
            Words = re.split("\W", Para)
            NumWords = len(Words)
            DirectWords = DirectWords+NumWords 
        else:
            Words = re.split("\W", Para)
            NumWords = len(Words)
            Words = re.split("\W", Para)
            NumWords = len(Words)
            OtherWords = OtherWords+NumWords 
    DirectPerc = DirectWords / (DirectWords + OtherWords)
    DirectPerc = [DirectPerc]
    return DirectPerc

def make_moving_unit(Text, Start, UnitLength):
    End = Start+UnitLength
    Unit = Text[Start:End]
    return(Unit)

def make_sampled_unit(Text, UnitLength):
    Unit = random.sample(Text, UnitLength)    
    return Unit

def get_tokens(Unit): 
    Tokens = len(Unit)
    return Tokens

def get_types(Unit):
    Types = len(Counter(Unit))
    return Types

def get_ttr(Unit): 
    Tokens = get_tokens(Unit)
    Types = get_types(Unit)
    TTR = Types / Tokens
    return TTR

def read_csv(BasicVocab):
    with open(BasicVocab, "r") as InFile: 
        Common = pd.DataFrame.from_csv(InFile, sep=',', index_col=None)
        return Common

def get_lemmatext(Unit):
    import treetaggerwrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
    Tagged = tagger.tag_text(Unit)
    Lemmas = []
    AmbLemmas = []
    for Item in Tagged: 
        Item = re.split("\t", Item)
        Lemma = Item[2]
        if Lemma == "d": 
            Lemma = "de"
        if Lemma == "n": 
            Lemma = "ne"
        if Lemma == "l": 
            Lemma = "le"
        if Lemma == "j": 
            Lemma = "je"
        if Lemma == "t": 
            Lemma = "tu"
        if Lemma == "qu": 
            Lemma = "que"
        if Lemma == "la|le": 
            Lemma = "la"
        if Lemma == "sommer|être": 
            Lemma = "être"
        if Lemma == "suivre|être": 
            Lemma = "être"
        if Lemma == "foi|fois": 
            Lemma = "fois"
        if Lemma == "ouvrer|ouvrir": 
            Lemma = "ouvrir"
        if Lemma == "sen|sens": 
            Lemma = "sens"
        if Lemma == "jacque|jacques": 
            Lemma = "jacques"
        if "|" in Lemma: 
            AmbLemmas.append(Lemma)
            Lemma = re.split("\|", Lemma)[0]
        Lemmas.append(Lemma)
    AmbLemmas = Counter(AmbLemmas)
    #if AmbLemmas: 
    #    print(AmbLemmas)
    return Lemmas

def get_bvr(Unit, UnitLength, BasicVocab):
    Lemmas = get_lemmatext(Unit)
    Common = read_csv(BasicVocab)
    Common = list(Common.loc[:,"mot"])
    CommonCount = 0
    for Item in Lemmas: 
        if Item in Common: 
            CommonCount +=1
    BVR = CommonCount / UnitLength
    return BVR

def get_vocab_stats(TextTTRs, TextBVRs):
    TTRMean = np.mean(TextTTRs)
    TTRStdev = np.std(TextTTRs)
    TTRVarc = TTRStdev / TTRMean
    BVRMean = np.mean(TextBVRs)
    BVRStdev = np.std(TextBVRs)
    BVRVarc = BVRStdev / BVRMean
    TextResults = [TTRMean, TTRStdev, TTRVarc, BVRMean, BVRStdev, BVRVarc]
    #TextResults = pd.Series(TextResults, name=Idno)
    return(TextResults)

def save_results(CollResults, ResultFile, TestType, UnitLength): 
    with open(ResultFile, "w") as OutFile: 
        CollResults.to_csv(OutFile)

# =============================
# Central coordination function
# =============================

def assess_vocabulary(InPath, TestType, UnitLength, ResultsFile, BasicVocab): 
    CollResults = pd.DataFrame()
    FileCounter = 0
    for File in glob.glob(InPath): 
        Idno, Ext = os.path.basename(File).split(".")
        Text = read_text(File)
        LengthsWords = get_lengths(Text)
        SentStats = get_sent_stats(LengthsWords, Idno)
        DirectPerc = get_direct_prop(Text)
        Text = prepare_text(Text)
        TextTTRs = []
        TextBVRs = []
        if TestType == "MovingWindow": 
            for Start in range(0,len(Text)-UnitLength):
                Unit = make_moving_unit(Text, Start, UnitLength)
                TTR = get_ttr(Unit)
                TextTTRs.append(TTR)
                BVR = get_bvr(Unit, UnitLength, BasicVocab)
                TextBVRs.append(BVR)
            VocabStats = get_vocab_stats(TextTTRs, TextBVRs)
            SentStats.extend(VocabStats)
            CombinedResults = pd.Series(SentStats)
        elif TestType == "RandomSample": 
            Counter = 0 
            while Counter < 20: 
                Unit = make_sampled_unit(Text, UnitLength)
                TTR = get_ttr(Unit)
                TextTTRs.append(TTR)
                BVR = get_bvr(Unit, UnitLength, BasicVocab)
                TextBVRs.append(BVR)
                Counter +=1
            VocabStats = get_vocab_stats(TextTTRs, TextBVRs)
            SentStats.extend(VocabStats)
            CombinedResults = pd.Series(SentStats)
        elif TestType == "RandomWindow": 
            Counter = 0 
            while Counter < 20: 
                Counter +=1
                Start = random.choice(list(range(0,len(Text)-UnitLength)))
                Unit = make_moving_unit(Text, Start, UnitLength)
                TTR = get_ttr(Unit)
                TextTTRs.append(TTR)
                BVR = get_bvr(Unit, UnitLength, BasicVocab)
                TextBVRs.append(BVR)
                Counter +=1
            VocabStats = get_vocab_stats(TextTTRs, TextBVRs)
            SentStats.extend(VocabStats)
            SentStats.extend(DirectPerc)
            CombinedResults = pd.Series(SentStats)
        CollResults = CollResults.append(CombinedResults, ignore_index=True)
        FileCounter +=1
        sys.stdout.write("\r"+str(FileCounter)+"/627")
        #print("Files done", FileCounter)
    CollResults.columns = ["idno", "NumWords", "NumSents", "SLMean", "SLMedian", "SLStdev", "SLVarc", "TTR-mean", "TTR-stdev", "TTRVarc", "BVR-mean", "BVR-stdev", "BVRVarc", "DirectPerc"]
    #print(CollResults)
    save_results(CollResults, ResultsFile, TestType, UnitLength)

assess_vocabulary(InPath, TestType, UnitLength, ResultsFile, BasicVocab)

