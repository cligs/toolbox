#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: run_word2vec.py
# Author: #cf
# Version 0.2.0 (2016-10-29)

"""
This is the parameter file for word2vec.py. 
It bundles several functions related to querying word2vec models using gensim.
"""

import word2vec

#========================
# General Parameters
#========================

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/pdb/3-word2vec/"
ModelOneFile = WorkDir + "models/frwiki5-ro.gensim"
ModelTwoFile = WorkDir + "models/roman5-ro.gensim"
ModelLabels = ["wk5", "rm5"] 
CommonWordsFile = WorkDir + "CommonWords.csv"


#========================
# word2vec.compare
#========================

Query = ["train", 20, 0.42]  # target word, number of most similar words, similarity threshold

CompResultsFile = WorkDir + "comp-gexf/"+ModelLabels[0]+"-"+ModelLabels[1]+"_"+Query[0]+"-"+str(Query[1])+".gexf"
CompResultsGraph = WorkDir + "comp-network/"+ModelLabels[0]+"-"+ModelLabels[1]+"_"+Query[0]+"-"+str(Query[1])+".png"

word2vec.compare(ModelOneFile, ModelTwoFile, ModelLabels,
                 CompResultsFile, CompResultsGraph, Query)



#========================
# word2vec.discover
#========================

CommonAndSimilarWordsFile = WorkDir + "CommonAndSimilarWords.csv"
#word2vec.discover(ModelOneFile, ModelTwoFile, ModelLabels,
#                 CommonWordsFile, CommonAndSimilarWordsFile)



#========================
# word2vec.query
#========================

#ModelFile = "models/frwiki5-ro.gensim"
ModelFile = "models/roman5-ro.gensim"
Mode = ["Similar"]  #Pair|NWords|Calc|OddOne|Similar

### Queries ###

# Pair: Calculate (cosine) similarity score (input: two terms)
#PairQuery = ["machine", "outil"] 
#PairQuery = ["femme", "fille"] 
#PairQuery = ["père", "fils"] 
#PairQuery = ["café", "cigarette"] 
#PairQuery = ["cigare", "cigarette"] 
#PairQuery = ["pipe", "cigare"] 
PairQuery = ["tomate", "mangue"] 

# NWords: Calculate similarity between lists of words
NWordsQuery = [["police", "voiture"],["automobile", "flic"]]

# Calc: Calculate the most similar term.
# Input: [[positive terms], [negative terms]]
#CalcQuery = [["femme", "amant"], ["homme"]]
#CalcQuery = [["oncle", "femme"], ["homme"]] 
#CalcQuery = ["ville", "époux", "homme"] 
#CalcQuery = ["amant", "femme"], ["homme"] 
#CalcQuery = ["livre", "histoire", "fiction"], ["théâtre"] 
#CalcQuery = ["capitale", "allemagne"], ["france"] 
#CalcQuery = [["histoire", "livre"], ["réalité"]]
CalcQuery = [["femme", "roi"], ["homme"]]  # funktioniert perfekt
#CalcQuery = [["roman", "télévision"], ["histoire"]]  # fast, "film, téléfilm"
#CalcQuery = [["roman", "télévision"], ["histoire"]]  # fast, "film, téléfilm"
#CalcQuery = [["récit", "roman"], ["histoire"]]  # conte? => poème, conte, livre
#CalcQuery = [["paris", "grenoble"], ["ville"]]  # conte? => poème, conte, livre

# OddOne: Find the term that does not belong in the list
#OddOneQuery = ["argent", "billet", "monnaie", "musée"]
OddOneQuery = ["femme", "oncle", "fille", "soeur"]
OddOneQuery = ["roman", "histoire", "récit", "livre", "poème"]

# Similar: find similar words
SimilarQuery = ["train", 12]

#word2vec.query(Mode, ModelFile, PairQuery, NWordsQuery, 
#               OddOneQuery, CalcQuery, SimilarQuery)








#========================
# word2vec.coherence
#========================

#TopWords = 5
#WorkDir = "/media/christof/data/Dropbox/0-Analysen/2016/pdb/"
#ModelFile = WorkDir + "3-word2vec/models/frwiki5.gensim"
#TopicWordsFile = WorkDir + "2-topicmodeling/7_model/topics-with-words_080tp-6000it-7000in.csv"
#CoherencesFile = WorkDir + "3-word2vec/topics/topic-coherence-scores_"+str(TopWords)+"-words.csv"


#word2vec.coherence(ModelFile, TopicWordsFile, TopWords, CoherencesFile)














#========================
# word2vec.build_model
#========================

#ModelFile = WorkDir + "models/frwiki5.gensim"
#TextDir = WorkDir + "data/frwiki/"
#Size = 500       # dimensions of the model
#MinCount = 30    # minimum count of each type
#Type = 0         # 0=CBOW, 1=skip-gram; default=0
#Window = 4       # Words before and after target word
#Iterations = 10  # default=5
#word2vec.build_model(TextDir, Type, Window, Iterations, Size, MinCount, ModelFile)



#========================
# word2vec.persist
#========================

#ModelFile = WorkDir + "models/frwiki5.gensim"
#Replace = True
#word2vec.persist(ModelFile, Replace)


#========================
# word2vec.cumsim
#========================

#MeanSimilarityFile = WorkDir + "compared-mean-similarities_"+ModelLabels[0]+"-"+ModelLabels[1]+".csv"
#word2vec.meansim(ModelOneFile, ModelTwoFile, ModelLabels, 
#                 CommonWordsFile, MeanSimilarityFile)


#========================
# word2vec.eval
#========================

#ModelFile = WorkDir + "models/roman5-ro.gensim"
#EvalFile = WorkDir + "testpairs.csv"
#word2vec.eval(EvalFile, ModelFile)













