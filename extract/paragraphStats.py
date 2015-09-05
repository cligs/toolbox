#!/usr/bin/env python3
# Filename: paragraphStats.py
# Author: #cf


##################
### Parameters ###
##################

#wdir = "/home/christof/Dropbox/0-Analysen/2015/hybrid/rf692/"
wdir = "/home/christof/Repos/cligs/romanfrancais/"
outfolder = "./stats/" # optional: prefix wdir 
infolder = "master/rf*.xml"
paragraphStatsFile = outfolder+"paragraphStats.csv"

##################
### Functions  ###
##################

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re
from lxml import etree
from collections import Counter
import itertools

def read_xml(file): 
    #print("- reading xml...")
    with open(file, "r"): 
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        xml = etree.parse(file, parser)
        #namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}teiHeader")
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}front")
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}back")
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}note")
        etree.strip_elements(xml, "{http://www.tei-c.org/ns/1.0}head")
        etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}seg")
        etree.strip_tags(xml, "{http://www.tei-c.org/ns/1.0}said")
        xml = etree.tostring(xml, pretty_print=False, encoding="unicode")
        #print(xml)
        return(xml)

def get_paragraphStats(idno, xml):
    #print("- getting statistics...")
    text_wordsPerParagraph = [] 
    text_paragraphs = re.split("<p>", xml)
    for para_paragraph in text_paragraphs:
        para_paragraph = para_paragraph[0:-4]
        para_words = re.split(" ", para_paragraph)
        #print(para_words)
        para_wordsPerParagraph = len(para_words)
        text_wordsPerParagraph.append(para_wordsPerParagraph)
    text_numberOfParagraphs = len(text_wordsPerParagraph)
    text_wordsPerText = sum(text_wordsPerParagraph)
    text_avgWordsPerParagraph = text_wordsPerText / text_numberOfParagraphs
    text_data = [idno, text_wordsPerText, text_numberOfParagraphs, text_wordsPerParagraph, text_avgWordsPerParagraph]     
    #print(text_data)
    return text_data


def plot_paragraphStats(coll_data, outfolder): 
    print("- plotting data...")
    
    ## Plotting number of paragraphs per text in collection
    noParasData = Counter(coll_data.loc[:,"noParas"])
    #print(noParasData)
    val, weight = zip(*[(k, v) for k,v in noParasData.items()])
    #plt.hist(val, weights=weight) # default
    plt.hist(val,  bins=20, range=[0, 10000], weights=weight)
    plt.title("Verteilung der Anzahl von Absätzen (pro Text in der Sammlung)")
    plt.xlabel("Anzahl der Absätze")
    plt.ylabel("Häufigkeit in der Sammlung")
    figure_filename = outfolder+"paragraphStats_noParas.png"
    plt.savefig(figure_filename, dpi=300)
    #plt.show()
    plt.close()

    ## Plotting length of paragraphs per text in collection
    lenParas = list(itertools.chain(*coll_data.loc[:,"lenParas"]))
    lenParasData = Counter(lenParas)
    #print(lenParasData)
    val, weight = zip(*[(k, v) for k,v in lenParasData.items()])
    #plt.hist(val, weights=weight) # default
    plt.hist(val, bins=20, range=[0, 350], weights=weight)
    plt.title("Verteilung der Länge der Paragraphen (in der Sammlung)")
    plt.xlabel("Länge der Paragraphen (in Wörtern)")
    plt.ylabel("Häufigkeit in der Sammlung")
    figure_filename = outfolder+"paragraphStats_lenParas.png"
    plt.savefig(figure_filename, dpi=300)
    #plt.show()
    plt.close()

    ## Plotting length of texts in words in collection
    noWordsData = Counter(coll_data.loc[:,"noWords"])
    #print(noWordsData)
    #plt.hist(val, weights=weight) # default
    val, weight = zip(*[(k, v) for k,v in noWordsData.items()])
    plt.hist(val, bins=20, range=[14000, 34000], weights=weight)
    plt.title("Verteilung der Länge der Texte (in der Sammlung)")
    plt.xlabel("Länge der Texte (in Wörtern)")
    plt.ylabel("Häufigkeit in der Sammlung")
    figure_filename = outfolder+"paragraphStats_noWords.png"
    plt.savefig(figure_filename, dpi=300)
    #plt.show()
    plt.close()
    
    ## Plotting average paragraph length in texts in collection
    avgWordsPPData = Counter(coll_data.loc[:,"avgWordsPP"])
    #print(avgWordsPPData)
    #plt.hist(val, weights=weight) # default
    val, weight = zip(*[(k, v) for k,v in avgWordsPPData.items()])
    plt.hist(val, bins=20, range=[0, 500], weights=weight)
    plt.title("Verteilung der durchschn. Länge der Absätze (in der Sammlung)")
    plt.xlabel("Durchschnittliche Länge der Absätze (in Wörtern)")
    plt.ylabel("Häufigkeit in der Sammlung")
    figure_filename = outfolder+"paragraphStats_avgWordsPP.png"
    plt.savefig(figure_filename, dpi=300)
    #plt.show()
    plt.close()

def paragraphStats(wdir, infolder, outfolder, paragraphStatsFile):
    """Extract paragraph statistics per text."""
    print("Launched paragraphStats")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)    
    coll_data = []
    for file in glob.glob(wdir+infolder):
        ## Get idno and text content as string
        idno = os.path.basename(file)[:-4]
        xml = read_xml(file)
        ## Calculate paragraph stats for each text            
        text_data = get_paragraphStats(idno, xml)
        ## Add info about each text to collection-level list
        coll_data.append(text_data)
    ## Turn collection-level data into one joint dataframe and save it.
    headers = ["idno", "noWords", "noParas", "lenParas", "avgWordsPP"]
    coll_data = pd.DataFrame(coll_data, columns=headers)
    coll_data.to_csv(paragraphStatsFile, sep=",", encoding="utf-8")
    #print(coll_data)   
    plot_paragraphStats(coll_data, outfolder)
    print("Done.")

paragraphStats(wdir, infolder, outfolder, paragraphStatsFile)
