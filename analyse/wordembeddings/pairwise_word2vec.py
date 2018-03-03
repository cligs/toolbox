#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: my-word-to-vec.py
# Author: #cf
# Version 0.1.0 (2016-09-24)


"""
Function to compare which words are similar to a target word,
based on data from two word2vec models.

This function assumes there are already two gensim model files,
each representing one of the two comparison corpora. 
"""

##################
# Parameters
##################

WorkDir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
ModelOneFile = WorkDir + "models/frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim"
ModelTwoFile = WorkDir + "models/roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim"
ModelLabels = ["WIKI", "ROMAN"] 
Query = ["morceau_nom", 100]  # target word, number of most similar words 
ResultsFile = WorkDir + "gexf/"+ModelLabels[0]+"-"+ModelLabels[1]+"_"+Query[0]+"-"+str(Query[1])+".gexf"
ResultsGraph = WorkDir + "network/"+ModelLabels[0]+"-"+ModelLabels[1]+"_"+Query[0]+"-"+str(Query[1])+".png"



##################
# Imports
##################

import gensim 
import networkx as nx
import matplotlib.pyplot as plt


#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)



##################
# Functions
##################

def get_similar_words(ModelFile, Query):
    """
    Returns the n words which are most similar to the target word.
    """
    #print("--similar_words")
    Model = gensim.models.Word2Vec.load(ModelFile)
    Result = Model.similar_by_word(Query[0], Query[1])
    Result = [item for item in Result if "_nom" in item[0] or "_adj" in item[0]]
    print(Query, Result)
    return Result

def get_targetnodes(Query, ModelLabels): 
    """
    Get the two nominally differentiated target nodes.
    """
    #print("--get_targetnodes")
    TargetNodes = []
    TargetNodes.append(Query[0][:-4]+"_"+ModelLabels[0])
    TargetNodes.append(Query[0][:-4]+"_"+ModelLabels[1])
    #print(TargetNodes)
    return TargetNodes

def make_nodes(Query, TargetNode, Results): 
    """
    Extract nodes from similar_words data.
    """
    #print("--make_nodes")
    Nodes = [TargetNode]
    for Item in Results: 
        Nodes.append(Item[0][:-4])
    #print(Nodes)
    return Nodes

def get_sharednodes(NodesOne, NodesTwo):
    """
    Get the list of nodes which are most similar in both collections.
    """
    #print("--get_sharednodes")
    SharedNodes = []
    for Node1 in NodesOne: 
        for Node2 in NodesTwo: 
            if Node1 == Node2: 
                SharedNodes.append(Node1)
    SharedNodes = set(SharedNodes)
    SharedNodes = [node for node in SharedNodes if node]
    #print(SharedNodes)
    return SharedNodes

def make_edges(Query, TargetNode, Results): 
    """
    Extract weighted edges from similar_words data. 
    """
    #print("--make_edges")
    Edges = [] 
    for Item in Results: 
        Edges.append([TargetNode, Item[0][:-4], Item[1]])
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
        MyGraph.add_edge(Edge[0], Edge[1], weight=Edge[2])
    for Edge in EdgesTwo:
        MyGraph.add_edge(Edge[0], Edge[1], weight=Edge[2])
    nx.write_gexf(MyGraph, ResultFile)
    return MyGraph


def visualize_graph(MyGraph, TargetNodes, SharedNodes, ResultsGraph):
    """
    Use the MyGraph data to draw the actual graph.
    """
    #print("--visualize_graph")
    Positions = nx.spring_layout(MyGraph, k=0.13, scale=1)
    #pos=nx.circular_layout(MyGraph, center=[0,0])
    EdgesAndWeights=dict([((u,v,),int(d["weight"])) for u,v,d in MyGraph.edges(data=True)])
    JustWeights = [d.get("weight") for u,v,d in MyGraph.edges(data=True)]
    #JustWeights = [(weight*weight*weight)*15 for weight in JustWeights]
    JustWeights = [4 for weight in JustWeights]
    nx.draw_networkx_nodes(MyGraph, Positions, node_size=1200, node_color="c", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=SharedNodes, node_size=1200, node_color="r", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=[TargetNodes[0], TargetNodes[1]], node_size=1800, node_color="y", label="label")
    nx.draw_networkx_labels(MyGraph, Positions, font_size=6)
    #nx.draw_networkx_edge_labels(MyGraph, Positions, edge_labels=EdgesAndWeights, font_size=12)
    nx.draw_networkx_edges(MyGraph, Positions, width=JustWeights, edge_color="#888888")

    plt.axis('off')
    plt.savefig(ResultsGraph, dpi=400)
    


################
# Main function
################

def main(ModelOneFile,
         ModelTwoFile,
         Query,
         ResultsFile,
         ResultsGraph):
    print("Launched.")
    ResultsOne = get_similar_words(ModelOneFile, Query)
    ResultsTwo = get_similar_words(ModelTwoFile, Query)
    TargetNodes = get_targetnodes(Query, ModelLabels)
    NodesOne = make_nodes(Query, TargetNodes[0], ResultsOne)
    NodesTwo = make_nodes(Query, TargetNodes[1], ResultsTwo)
    SharedNodes = get_sharednodes(NodesOne, NodesTwo)
    EdgesOne = make_edges(Query, TargetNodes[0], ResultsOne)
    EdgesTwo = make_edges(Query, TargetNodes[1], ResultsTwo)
    MyGraph = make_graph(NodesOne, NodesTwo, EdgesOne, EdgesTwo, ResultsFile)
    visualize_graph(MyGraph, TargetNodes, SharedNodes, ResultsGraph)        
    print("Info. Models:", ModelLabels[0], "vs.", ModelLabels[1], "; query:", Query[0], "; words:", Query[1], "; shared:", len(SharedNodes), "words.")
    print("Done.")
    
main(ModelOneFile,
     ModelTwoFile,
     Query,
     ResultsFile,
     ResultsGraph)
