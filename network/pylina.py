#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file: run_pyzeta.py
# author: #cf
# version: 0.0.1


import glob
import os
import re
from lxml import etree
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import itertools


# =========================================
# Extract speech statis from teatroespanol
# =========================================


def read_tei(teifile):
    idno,ext = os.path.basename(teifile).split(".")
    print("current text idno:", idno)
    tei = etree.parse(teifile)
    return idno, tei


def get_speechseq(tei):
    namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
    speechseq = tei.findall("//tei:sp", namespaces=namespaces)
    print("total number of speeches:", len(speechseq))
    return speechseq


def get_speakerid(speech):
    speechtxt = str(etree.tostring(speech))
    speakerid = re.findall("who=\"#(.*?)\"", speechtxt)
    # print(speakerid[0])
    return speakerid[0]


def get_speakername(tei, speakerid):
    namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
    xpath = "//tei:role[@xml:id=\'" + speakerid + "\']/text()"
    speakername = tei.xpath(xpath, namespaces=namespaces)
    if speakername:
        speakername = speakername[0]
    else:
        speakername = "(unknown)"
    # print(speakername)
    return speakername


def get_speechstats(speech):
    namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
    lines = speech.findall("tei:l", namespaces=namespaces)
    numlines = len(lines)
    numwords = 0
    for line in lines:
        line = line.xpath("text()", namespaces=namespaces)
        if line:  # this should not be necessary; check faulty files
            words = re.split("\W", line[0])
            words = [word for word in words if word]
            numwords = numwords + len(words)
    # print("numlines", numlines)
    # print("numwords", numwords)
    return numlines, numwords


def save_listoflists(dataseq, idno, zffolder):
    zffile = os.path.join(zffolder, idno + "-myzf.csv")
    with open(zffile, "w") as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        writer.writerows(dataseq)


def extract(teifile, zffolder):
    """
    Main function for "pylina.extracting".
    Extracts data about the sequence of speeches in a play.
    Status: OK.
    """
    idno, tei = read_tei(teifile)
    speechseq = get_speechseq(tei)
    myzf = [["num", "id", "name", "numlines", "numwords"]]
    speechnum = 1
    for speech in speechseq:
        speakerid = get_speakerid(speech)
        speakername = get_speakername(tei, speakerid)
        numlines, numwords = get_speechstats(speech)
        data = [speechnum, speakerid, speakername, numlines, numwords]
        speechnum +=1
        myzf.append(data)
    save_listoflists(myzf, idno, zffolder)
    return idno, myzf


# =============================================
# Create adjacency matrix based on interactions
# =============================================

def get_interactions(myzf):
    interactions = []
    for i in range(1, len(myzf) - 1):
        nameone = myzf[i][2]
        nametwo = myzf[i + 1][2]
        weight = myzf[i][4]
        interlocutors = [nameone, nametwo]
        interlocutors = sorted(interlocutors)
        interaction = [interlocutors, weight]
        interactions.append(interaction)
    # print(interactions)
    return interactions


def make_df(myzf):
    headers = myzf.pop(0)
    myzfdf = pd.DataFrame(myzf, columns=headers)
    # print(myzfdf.head())
    return(myzfdf)


def get_speakers(myzfdf):
    speakers = list(set(myzfdf.loc[:, "name"]))
    # print(speakers)
    return speakers


def make_matrix(speakers, myzfdf):
    matrix = pd.DataFrame(index=speakers, columns=speakers)
    matrix.fillna(0, inplace=True)
    # print(matrix)
    return matrix


def fill_matrix(matrix, interactions):
    for item in interactions:
        # print(item[0][0], item[0][1], item[1])
        matrix.loc[item[0][0], item[0][1]] = matrix.loc[item[0][0],item[0][1]] + item[1]
        matrix.loc[item[0][1], item[0][0]] = matrix.loc[item[0][1], item[0][0]] + item[1]
    # print(matrix)
    return matrix


def save_matrix(matrix, idno, matrixfolder):
    matrixfile = os.path.join(matrixfolder, idno + "-matrix.csv")
    matrix.to_csv(matrixfile)


def matrix(idno, myzf, matrixfolder):
    """
    Create an adjacency matrix from the speech statistics data.
    """
    interactions = get_interactions(myzf)
    myzfdf = make_df(myzf)
    speakers = get_speakers(myzfdf)
    matrix = make_matrix(speakers, myzfdf)
    matrix = fill_matrix(matrix, interactions)
    save_matrix(matrix, idno, matrixfolder)
    return matrix


# =============================================
# Create graph representation based on matrix
# =============================================

def build_graph(idno, matrix):
    speakers = sorted(matrix.index.values)
    # print(speakers)
    interactions = itertools.permutations(speakers, 2)
    graph = nx.Graph(idno=idno, name=idno)
    for item in interactions:
        weight = matrix.get_value(item[0], item[1])
        if weight > 0:
            #print(item[0], item[1], weight)
            graph.add_edge(item[0], item[1], weight=weight)
    print("number of nodes and edges:", graph.number_of_nodes(), graph.number_of_edges())
    return graph


def save_graph(graph, graphfolder, idno):
    nx.write_gexf(graph, graphfolder + idno + "-graph.xml")
    return graph


def graph(idno, matrix, graphfolder):
    graph = build_graph(idno, matrix)
    save_graph(graph, graphfolder, idno)
    return graph


# =======================================
# Analyzing the graph data
# =======================================


def save_analysis(analysis, analysisfile):
    with open(analysisfile, "a") as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        writer.writerow(analysis)


def calculate_graphanalysis(graph):
    idno = graph.graph["idno"]
    numnodes = graph.number_of_nodes()
    numedges = graph.number_of_edges()
    density = nx.density(graph)
    analysis = [idno, numnodes, numedges, density]
    # print(analysis)
    return analysis


def analyze(graph, analysisfile):
    analysis = calculate_graphanalysis(graph)
    save_analysis(analysis, analysisfile)


# =======================================
# Drawing the graph data
# =======================================


def get_weights(mygraph):
    weights = [d.get("weight") for u, v, d in mygraph.edges(data=True)]
    weights = [weight/100 for weight in weights]
    return weights


def create_edgelabels(mygraph):
    edgelabels = dict([((u,v,),int(d["weight"])) for u,v,d in mygraph.edges(data=True)])
    return edgelabels


def plot_graph(graph, threshold, plotfolder):
    idno = graph.graph["idno"]
    # Filter the full graph by edge weight
    graph = nx.Graph([(u, v, d) for u, v, d in graph.edges(data=True) if d['weight'] > threshold])
    # Derive necessary data
    weights = get_weights(graph)
    edgelabels = create_edgelabels(graph)
    positions = nx.fruchterman_reingold_layout(graph, k=2, scale=2)
    # Perform the actual drawing
    nx.draw_networkx_nodes(graph, positions, node_size=1200, node_color="g", label="label")
    nx.draw_networkx_edges(graph, positions, width=weights)
    nx.draw_networkx_labels(graph, positions, font_size=10)
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=edgelabels, font_size=8)
    # Save the figure
    plt.axis('off')
    plt.title(str(idno))
    plt.savefig(plotfolder + idno + "-plot.png", dpi=300)
    plt.close()


def draw(graph, threshold, plotfolder):
    plot_graph(graph, threshold, plotfolder)
