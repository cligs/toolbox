#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: word2vec.py
# Author: #cf
# Version 0.1.0 (2016-09-24)


"""
Function to compare which words are similar to a target word,
based on data from two word2vec models.

This function assumes there are already two gensim model files,
each representing one of the two comparison corpora. 
"""



##################
# Imports
##################

import os
import gensim 
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import re
import glob
import matplotlib
import matplotlib.pyplot as plt
import sys
from tabulate import tabulate
from sklearn import preprocessing
import itertools
import pygal
from pygal.style import LightenStyle

#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)




#============================================================================
# compare (compare most similar words in two models)
#============================================================================

def get_similar_words(Model, Query):
    """
    Gets the n words which are most similar to the target word.
    Then, filters the n words by a threshold mimimum similarity.
    Returns only those among the n words beyond the threshold.
    """
    #print("--similar_words")
    NWords = Model.similar_by_word(Query[0], Query[1])
    SimilarWords = []
    for Entry in NWords: 
        if Entry[1] > Query[2]:
            SimilarWords.append(Entry)
    #print(Query)
    #print(len(SimilarWords), "words")
    #print(SimilarWords)
    return SimilarWords


def get_targetnodes(Query, ModelLabels): 
    """
    Get the two nominally differentiated target nodes.
    These two nodes will form the center of the graph.
    """
    #print("--get_targetnodes")
    TargetNodes = []
    TargetNodes.append(Query[0]+"_"+ModelLabels[0])
    TargetNodes.append(Query[0]+"_"+ModelLabels[1])
    #print(TargetNodes)
    return TargetNodes


def make_nodes(Query, TargetNode, Results): 
    """
    Extract nodes from similar_words data.
    """
    #print("--make_nodes")
    Nodes = [TargetNode]
    for Item in Results: 
        Nodes.append(Item[0])
    #print(Nodes)
    return Nodes

def get_sharednodes(SimilarNodesOne, SimilarNodesTwo):
    """
    Get the list of nodes which are most similar in both collections.
    """
    #print("--get_sharednodes")
    SharedNodes = []
    for Node1 in SimilarNodesOne: 
        for Node2 in SimilarNodesTwo: 
            if Node1 == Node2: 
                SharedNodes.append(Node1)
    SharedNodes = list(set(SharedNodes))
    #print(SharedNodes)
    return SharedNodes


def make_edges(Query, TargetNode, Results): 
    """
    Extract weighted edges from similar_words data. 
    """
    #print("--make_edges")
    Edges = [] 
    for Item in Results: 
        Edges.append([TargetNode, Item[0], Item[1]])
    #print(Edges)
    return Edges
    
    
def make_graph(NodesOne, NodesTwo, EdgesOne, EdgesTwo, ResultFile): 
    """
    Create word graph using networkx.
    """
    #print("--make_graph")
    MyGraph = nx.Graph(name="pairwise-similarity")
    for Node in NodesOne:
        MyGraph.add_node(Node)
    for Node in NodesTwo:
        MyGraph.add_node(Node)
    for Edge in EdgesOne:
        MyGraph.add_edge(Edge[0], Edge[1], weight=Edge[2], length=1-Edge[2])
    for Edge in EdgesTwo:
        MyGraph.add_edge(Edge[0], Edge[1], weight=Edge[2], length=1-Edge[2])
    nx.write_gexf(MyGraph, ResultFile)
    return MyGraph


def get_edgelabels(MyGraph): 
    EdgeKeys = []
    EdgeValues = []
    for Node1,Node2,Edge in MyGraph.edges(data=True): 
        #print(Node1, Node2, Edge)
        EdgeKeys.append((Node1,Node2))
        EdgeValues.append("{:03.2f}".format(Edge["weight"]))        
    EdgeLabels = dict(zip(EdgeKeys, EdgeValues))
    #print(EdgeLabels)
    return EdgeLabels


def get_edgewidths(MyGraph): 
    EdgeWidthsRaw = []
    for Node1,Node2,Edge in MyGraph.edges(data=True): 
        Weight = Edge["weight"]
        Width = (Weight*1)**1
        EdgeWidthsRaw.append(Width)
        #print(Weight, Width)
    #print(EdgeWidthsRaw)
    EdgeWidths = [((float(i)*10)**2)/5 for i in EdgeWidthsRaw]    
    #print(EdgeWidths)
    return EdgeWidths    


    
def draw_graph(MyGraph, TargetNodes, SharedNodes, EdgeLabels, EdgeWidths, ResultsGraph):
    """
    Use the MyGraph data to draw the actual network graph.
    """
    Positions = nx.spring_layout(MyGraph, k=0.15, scale=20, weight="weight")
    nx.draw_networkx_nodes(MyGraph, Positions, node_size=600, node_color="steelblue", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=SharedNodes, node_size=600, node_color="#b30000", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=[TargetNodes[0], TargetNodes[1]], node_size=1000, node_color="seagreen", label="label")
    nx.draw_networkx_labels(MyGraph, Positions, font_size=5)
    nx.draw_networkx_edge_labels(MyGraph, Positions, edge_labels=EdgeLabels, font_size=3)
    nx.draw_networkx_edges(MyGraph, Positions, width=EdgeWidths, alpha=0.6)
    plt.axis('off')
    plt.savefig(ResultsGraph, dpi=400)
    plt.close()


def compare(ModelOneFile,
            ModelTwoFile,
            ModelLabels, 
            CompResultsFile,
            CompResultsGraph,
            Query):
    print("Launched.")
    ModelOne = gensim.models.Word2Vec.load(ModelOneFile)
    ModelTwo = gensim.models.Word2Vec.load(ModelTwoFile)
    if Query[0] in ModelOne.vocab and Query[0] in ModelTwo.vocab: 
        SimilarWordsOne = get_similar_words(ModelOne, Query)
        SimilarWordsTwo = get_similar_words(ModelTwo, Query)
        TargetNodes = get_targetnodes(Query, ModelLabels)
        NodesOne = make_nodes(Query, TargetNodes[0], SimilarWordsOne)
        NodesTwo = make_nodes(Query, TargetNodes[1], SimilarWordsTwo)
        SharedNodes = get_sharednodes(NodesOne, NodesTwo)
        EdgesOne = make_edges(Query, TargetNodes[0], SimilarWordsOne)
        EdgesTwo = make_edges(Query, TargetNodes[1], SimilarWordsTwo)
        MyGraph = make_graph(NodesOne, NodesTwo, EdgesOne, EdgesTwo, CompResultsFile)
        EdgeLabels = get_edgelabels(MyGraph)
        EdgeWidths = get_edgewidths(MyGraph)
        draw_graph(MyGraph, TargetNodes, SharedNodes, EdgeLabels, EdgeWidths, CompResultsGraph)        
    else: 
        print(Query[0], "is missing from one or both models.")
    print("Done.")
    
    
    
    
#============================================================================
# Find potentially interesting words
#============================================================================
    
    
def csv2df(File): 
    with open(File, "r") as InFile: 
        AllData = pd.DataFrame.from_csv(InFile)
        CommonWords = list(AllData.loc[:,"lemma"])
        #print(CommonWords[0:10])
        return CommonWords

def df2csv(AllWordsData, CommonAndSimilarWordsFile): 
    with open(CommonAndSimilarWordsFile, 'w') as OutFile:
        AllWordsData.to_csv(OutFile)


def discover(ModelOneFile, ModelTwoFile, ModelLabels,
             CommonWordsFile, CommonAndSimilarWordsFile):
    """
    This function determines the overlap, in two word2vec models,
    in the most similar words of a given target word.
    The assumption is that words with high overlap are more 
    interpretable for a contrastive analysis. 
    """
    CommonWords = csv2df(CommonWordsFile)
    AllWordsData = []
    ModelOne = gensim.models.Word2Vec.load(ModelOneFile)
    ModelTwo = gensim.models.Word2Vec.load(ModelTwoFile)
    for Word in CommonWords[0:999]:
        if Word in ModelOne.vocab and Word in ModelTwo.vocab: 
            Query = [Word, 30, 0.2]
            SimilarWordsOne = get_similar_words(ModelOne, Query)
            SimilarWordsTwo = get_similar_words(ModelTwo, Query)
            TargetNodes = get_targetnodes(Query, ModelLabels)
            NodesOne = make_nodes(Query, TargetNodes[0], SimilarWordsOne)
            NodesTwo = make_nodes(Query, TargetNodes[1], SimilarWordsTwo)
            SharedWords = get_sharednodes(NodesOne, NodesTwo)
            OneWordData = {"word": Word, "num-shared" : len(SharedWords)}
            AllWordsData.append(OneWordData)
        else: 
            print(Word, "is missing from one or both models.")
    AllWordsData = pd.DataFrame(AllWordsData)
    AllWordsData.sort_values(by=["num-shared", "word"], ascending=False, inplace=True)
    df2csv(AllWordsData, CommonAndSimilarWordsFile) 
    
    
    
    
    
    
#==================================================================
# Query a model
#==================================================================


def wordpair_similarity(ModelFile, PairQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.similarity(PairQuery[0], PairQuery[1])
    print("Query:", PairQuery)
    print("Result:", Result)



def nword_similarity(ModelFile, NWordsQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.n_similarity(NWordsQuery[0], NWordsQuery[1])
    print("Query:", NWordsQuery)
    print("Result:", Result)


def calc_similar(ModelFile, CalcQuery):
    """
    Returns the most similar term for a set of positive and negative terms.
    """
    print("--fourth_term")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.most_similar(positive=[Word for Word in CalcQuery[0]], 
                                negative=[Word for Word in CalcQuery[1]], 
                                topn=5) #??
    print("Query:", CalcQuery)
    print("Result:", Result)


def find_oddone(ModelFile, DoesntMatch):
    """
    Returns the term that does not belong to the list.
    """
    print("--doesnt_match")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.doesnt_match([Word for Word in DoesntMatch])
    print("Query:", DoesntMatch)
    print("Result:", Result)


def similar_words(ModelFile, SimilarQuery):
    """
    Returns the n words which are most similar in the data.
    """
    print("--similar_words")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.similar_by_word(SimilarQuery[0], SimilarQuery[1])
    print("Query:", SimilarQuery)
    print(tabulate(Result))
    return Result


def similar_to_networkx(SimilarQuery, Result): 
    """
    Transform output from similar_words into a structure for networkx.
    """
    TargetWord = SimilarQuery[0]
    AllLinks = []
    for Item in Result: 
        Word = Item[0]
        Weight = Item[1]
        #print(Word, Weight)
        Link = [TargetWord, Word, Weight]
        AllLinks.append(Link)    
    return AllLinks


def make_double_graph(AllLinks): 
    """
    Create word graph using networkx.
    """
    MyGraph = nx.Graph(name="word-graph")
    for Link in AllLinks:
        Node1 = Link[0]
        Node2 = Link[1]
        Weight = Link[2]
        #print(Node1, Node2, Weight)
        MyGraph.add_node(Node1, label=Node1)
        MyGraph.add_edge(Node1, Node2, weight=Weight)
    nx.write_gexf(MyGraph,"mygraph_contemps.gexf")
    return MyGraph


def visualize_graph(ModelFile, MyGraph, SimilarQuery):
    ModelName,Ext = os.path.basename(ModelFile).split(".")
    #Positions = nx.spring_layout(MyGraph, k=1, scale=4)
    Positions = nx.circular_layout(MyGraph, scale=10, center=[0,0])
    EdgeLabels = get_edgelabels(MyGraph)
    #print(EdgeLabels)
    EdgeWidths = get_edgewidths(MyGraph)
    #print(EdgeWidths)
    nx.draw_networkx_nodes(MyGraph, Positions, node_size=1500, node_color="steelblue", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=[SimilarQuery[0]], node_size=2500, node_color="seagreen", label="label")
    nx.draw_networkx_labels(MyGraph, Positions, font_size=8)
    nx.draw_networkx_edge_labels(MyGraph, Positions, edge_labels=EdgeLabels, font_size=5)
    nx.draw_networkx_edges(MyGraph, Positions, width=EdgeWidths, alpha=0.6)
    plt.axis('off')
    plt.savefig("sim-network/"+str(ModelName)+"_"+str(SimilarQuery[0])+"-"+str(SimilarQuery[1])+".png", dpi=300)
    plt.close()
    

def query(Mode, ModelFile, 
         PairQuery, NWordsQuery, OddOneQuery, CalcQuery, SimilarQuery):
    print("Launched.")
    print("Model used:", ModelFile)
    if "Pair" in Mode:
        wordpair_similarity(ModelFile, PairQuery)
    if "NWords" in Mode:
        nword_similarity(ModelFile, NWordsQuery)
    if "Calc" in Mode: 
        calc_similar(ModelFile, CalcQuery)
    if "OddOne" in Mode: 
        find_oddone(ModelFile, OddOneQuery)
    if "Similar" in Mode: 
        Result = similar_words(ModelFile, SimilarQuery)
        AllLinks = similar_to_networkx(SimilarQuery, Result)
        MyGraph = make_double_graph(AllLinks)
        visualize_graph(ModelFile, MyGraph, SimilarQuery)
    print("Done.")
    

    


 
#==================================================================
# cumsim
#==================================================================


def get_mean_sim(SimilarWords):
    MeanSim = np.mean([Item[1] for Item in SimilarWords])
    return MeanSim


def meansim(ModelOneFile, ModelTwoFile, ModelLabels, 
           CommonWordsFile, MeanSimilarityFile):
    """
    Compare the cumulated / average similarity score levels of two models.
    Checks the similarity scores for the n words around each word listed in CommonWordsFile.
    (Uses mostly functions defined in other parts of this module.)
    """
    ModelOne = gensim.models.Word2Vec.load(ModelOneFile)
    ModelTwo = gensim.models.Word2Vec.load(ModelTwoFile)
    CommonWords = csv2df(CommonWordsFile)
    AllWordsData = []
    for Word in CommonWords[0:1015]:
        if Word in ModelOne.vocab and Word in ModelTwo.vocab: 
            Query = [Word, 10, 0.0]
            SimilarWordsOne = get_similar_words(ModelOne, Query)
            SimilarWordsTwo = get_similar_words(ModelTwo, Query)
            MeanSimOne = get_mean_sim(SimilarWordsOne)
            MeanSimTwo = get_mean_sim(SimilarWordsTwo)
            MeanSimDiff = MeanSimOne-MeanSimTwo
            OneWordData = {"word":Word , 
                           "mean-"+ModelLabels[0]:MeanSimOne, 
                           "mean-"+ModelLabels[1]:MeanSimTwo,
                           "delta":MeanSimDiff}
            AllWordsData.append(OneWordData)
        else: 
            print(Word, ": missing from one or both models.")
    AllWordsData = pd.DataFrame(AllWordsData)
    AllWordsData.sort_values(by=["word"], ascending=True, inplace=True)
    df2csv(AllWordsData, MeanSimilarityFile) 


    
    
    
    
#==================================================================
# eval
#==================================================================

from itertools import combinations as cb
    
    
def eval(EvalFile, ModelFile): 
    # Load the list of pairs and build a list of grouped quadrupels from it.
    with open(EvalFile, "r") as InFile: 
        AllItems = pd.read_csv(InFile,
                            index_col=0,
                            header=0,
                            sep=",")
        #print(AllItems)
        Types = list(set(list(AllItems.index.values)))
        #print(Types)
        AllQuads = []
        for Type in Types:
            Pairs = []
            Items = AllItems.loc[Type,:]
            #print(Items)
            #print(len(Items))
            for i in range(0,len(Items)): 
                Pairs.append([Items.iloc[i,0], Items.iloc[i,1]])
            #print(Pairs)
            Quads = cb(Pairs, r=2)
            #print(Quads)
            AllQuads.append(Quads)
        ListAllQuads = []
        for Type in AllQuads:
            for Quad in Type:
                ListAllQuads.append([Quad[0][0], Quad[0][1], Quad[1][0], Quad[1][1]])
        #print(ListAllQuads)
    # Evaluate the model performance on the quadrupels                   
    Model = gensim.models.Word2Vec.load(ModelFile)
    Correct = 0
    Items = 0
    for Quad in ListAllQuads: 
        try: 
            Actual = Model.most_similar(positive=[Quad[1], Quad[2]], 
                                        negative=[Quad[0]], 
                                        topn=1)
        except: 
            print("Oh-ooh! (Probably a missing vocabulary item)")
        if Quad[3] == Actual[0][0]: 
            Correct +=1
            print("OK!", Quad[1]+"+"+Quad[2]+"-"+Quad[0]+"\t= "+Quad[3]+" : "+Actual[0][0])
        else: 
            print("ERREUR!", Quad[1]+"+"+Quad[2]+"-"+Quad[0]+"\t= "+Quad[3]+" : "+Actual[0][0])
        Items+=1
    print(str(Correct)+"/"+str(Items)+"="+str(Correct/Items))
      

    
    
    
    

#========================
# word2vec.build_model
#========================

def build_model(TextDir, Type, Window, Iterations, Size, MinCount, ModelFile): 
    """
    Builds a word vector model of the text files given as input.
    This should be used for very large collections of text, as it is very memory-friendly.
    """
    print("Launched build_model.")
    
    class MySentences(object):
        def __init__(self, dirname):
            self.dirname = dirname
        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for Para in open(os.path.join(self.dirname, fname)):
                    if "<doc id" not in Para and "</doc>" not in Para:
                        Sentences = re.split("[.!?]", Para)
                        for Sent in Sentences:
                            Sent = re.split("\W", Sent)
                            Sent = [Token.lower() for Token in Sent if Token]
                            Sent = [Token for Token in Sent if len(Token) > 2]
                            if len(Sent) > 1: 
                                yield Sent
 
    Sentences = MySentences(TextDir) # a memory-friendly iterator
    Model = gensim.models.Word2Vec(Sentences,
                                   sg=Type,
                                   window=Window,
                                   iter=Iterations,
                                   min_count=MinCount, 
                                   size=Size, 
                                   workers=6)
    Model.save(ModelFile)    
    

    
#========================
# word2vec.persist
#========================
    

def persist(ModelFile, Replace):
    ModelName,Ext = os.path.basename(ModelFile).split(".")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Model.init_sims(replace=Replace)
    Model.save(ModelName+"-ro.gensim")    
    
    
    


#========================
# word2vec.coherence
#========================
    

def get_topicwords(TopicWordsFile): 
    """
    Load the Mallet output file with n top words per topic.
    """
    with open(TopicWordsFile, "r") as InFile: 
        Headers = ["topic", "score", "words"]
        TopicWords = pd.read_csv(TopicWordsFile, sep="\t", header=None, names=Headers)
        #print(TopicWords.head())
        return TopicWords


def get_firstwords(TopicWords, TopicNum, TopWords):
    """
    Get the first four words for a given topic (for display).
    """
    FirstWords = TopicWords.iloc[TopicNum,:][2].split(" ")[0:TopWords]
    FirstWords = "-".join(FirstWords)
    #print(FirstWords)
    return(FirstWords)


def create_wordpairs(TopicWords, TopicNum, TopWords): 
    """
    Select the right topic and extract just the first n words.
    Combine each of the top n words with each other in pairs.    
    """
    Words = TopicWords.iloc[TopicNum,:][2].split(" ")[0:TopWords]
    WordPairs = itertools.combinations(Words, 2)
    return WordPairs


def get_distances(ModelFile, WordPairs): 
    """
    For each word pair in a topic, get its word2vec distance.
    """
    Model = gensim.models.Word2Vec.load(ModelFile)
    Distances = []
    for Item in WordPairs:   
        Distance = Model.similarity(Item[0], Item[1])
        Distances.append(Distance)
    #print(Distances)
    return Distances


def get_coherence(Distances):
    """
    Combine the distances for the words in one topic into one score.
    Here, the coherence score is simply the unweighted mean of the distances.
    """
    Coherence = np.mean(Distances)
    #print(Coherence)
    return Coherence


def save_coherences(AllCoherences, CoherencesFile): 
    """
    Save coherence score data to file. 
    Includes topic number, top-words used, and coherence score.
    """
    with open(CoherencesFile, "w") as OutFile: 
        AllCoherences.to_csv(OutFile, index=True, sep='\t', header=True)


co_style = pygal.style.Style(
  background='white',
  plot_background='white',
  font_family = "FreeSans",
  title_font_size = 20,
  legend_font_size = 16,
  label_font_size = 12)

def plot_coherences(AllCoherences, TopicWords, TopWords, CoherencesFile): 
    """
    Make a bar chart with topic coherence scores, including top words used.
    """
    AllCoherences.sort_values(by=["coherence"], axis=0, ascending=False, inplace=True)
    CoherencesPlotFile = CoherencesFile[:-4]+".svg"
    plot = pygal.Bar(show_legend=False,
                     y_title = "Kohärenz-Score ("+str(TopWords)+" Wörter)",
                     x_title = "Topics (absteigend nach Kohärenz sortiert)",
                     title = "word2vec-basierte Topic-Kohärenz",
                     style = co_style)
    #for i in range(0,5): # for testing
    for i in range(0,len(AllCoherences)): 
        plot.add("Topic "+str(int(AllCoherences.iloc[i,1])), 
                 [{"value":AllCoherences.iloc[i,0],
                   "color":"steelblue",
                   "label":str(AllCoherences.iloc[i,2])}])
    plot.render_to_file(CoherencesPlotFile)
    


def coherence(ModelFile, TopicWordsFile, TopWords, CoherencesFile):
    """
    Function to evaluate the coherence of topics.
    Status: Ok, but mechanism to deal with words missing in model is tbd.
    """
    TopicWords = get_topicwords(TopicWordsFile)
    AllCoherences = []
    AllFirstWords = []
    #for TopicNum in range(0,5): # for testing
    for TopicNum in range(0,len(TopicWords)):
        FirstWords = get_firstwords(TopicWords, TopicNum, TopWords)
        AllFirstWords.append(FirstWords)
        WordPairs = create_wordpairs(TopicWords, TopicNum, TopWords)
        Distances = get_distances(ModelFile, WordPairs)
        Coherence = get_coherence(Distances)
        AllCoherences.append(Coherence)
    AllCoherences = pd.Series(AllCoherences, name="coherence")
    AllCoherences = pd.DataFrame(AllCoherences)
    AllCoherences["topic"] = AllCoherences.index
    AllCoherences["topwords"] = AllFirstWords
    #print(AllCoherences)
    save_coherences(AllCoherences, CoherencesFile)
    plot_coherences(AllCoherences, TopicWords, TopWords, CoherencesFile)
    print("Done.")
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 