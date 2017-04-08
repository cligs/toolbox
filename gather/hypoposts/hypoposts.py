#!/usr/bin/env python3
# Filename: hypoposts.py


"""
# Function to build corpora from hypotheses.org blog data.
# Bulk download, metadata extraction, plain text extraction.
#
# This is the file containing the actual scripts.
# Run this from run_hypoposts.py.
"""


import os
import glob
import re
import requests as rq
from bs4 import BeautifulSoup as bs
import html
import pandas as pd
from collections import Counter
import numpy as np


# ========================================
# Get a list of URLs for requests
# ========================================


"""
SPARQL query on Isidore

---
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

select ?url where { 

<http://www.rechercheisidore.fr/resource/10670/3.0ardxl> <http://www.openarchives.org/ore/terms/aggregates> ?carnet. 

?carnet <http://www.openarchives.org/ore/terms/aggregates> ?billet.
?billet <http://purl.org/dc/elements/1.1/language> "FR".
?billet <http://purl.org/dc/terms/identifier> ?url.
?billet <http://purl.org/dc/elements/1.1/date> ?date.

FILTER (regex(str(?url), "http" ) && xsd:datetime(?date) > "2017-02-01"^^xsd:dateTime)

} 
LIMIT 1000
---

"""



# ========================================
# Download HTML posts from hypotheses.org
# ========================================


def get_urls(urlfile):
    with open(urlfile, "r") as infile:
        urls = infile.read()
        urls = re.split("\n", urls)
        urls = [url for url in urls if url]
    return urls


def get_html(url): 
    try:
        result = rq.get(url, timeout=1)
        html = result.text
        return html
    except: 
        print("ERROR: download problems ", str(url))


def save_html(html, htmlfolder, url):
    filename = re.sub("http://", "", url)
    filename = re.sub(".hypotheses.org/", "_", filename)
    filepath = htmlfolder+str(filename)+".html"
    with open(filepath, "w") as outfile: 
        outfile.write(html)
    return filename


def get_hypoposts(urlfile, htmlfolder): 
    """
    Function to bulk download blog posts from fr.hypotheses.org.
    """
    if not os.path.exists(htmlfolder): 
        os.makedirs(htmlfolder)
    urls = get_urls(urlfile)
    count = 0
    ok = 0
    for url in urls:
        count +=1
        #print(url)
        html = get_html(url)
        if html:
            filename = save_html(html, htmlfolder, url)
            ok +=1
        print(ok/count, "(", count, ok, ")")
            
        #else:
        #    print("ERROR: no HTML", str(url))


# ================================================
# Extract post data (text and metadata) from HTML
# ================================================


def read_html(htmlfile):
    with open(htmlfile, "r") as infile:
        html = infile.read()
        return html


def get_filename(htmlfile):
    filename, ext = os.path.basename(htmlfile).split(".")
    #print(filename)
    return filename


def get_text(html):
    text = re.findall("<div id=\"content(.*)<hr/>", html, re.S)
    if text:
        #print(len(text[0]))
        return text[0]
    else:
        text = re.findall("<div class=\"content(.*)<hr/>", html, re.S)
        if text:
            #print(len(text[0]))
            return text[0]
        else:
            text = re.findall("<div class=\"entry-inner(.*)<hr/>", html, re.S)
            if text:
                #print(len(text[0]))
                return text[0]
            else:
                text = re.findall("<div class=\"entry-content(.*)<p class", html, re.S)
                if text:
                    #print(len(text[0]))
                    return text[0]
                else:
                    text = re.findall("<div class=\"textwidget(.*)</div>", html, re.S)
                    if text:
                        #print(len(text[0]))
                        return text[0]
                    else:
                        text = "notexthere"
                        return text


def clean_text(text):
    try: 
        text = html.unescape(text)
    except:
        print("error")
    #remove remaining tags
    text = re.sub("\" class=\"site-content", "", text)
    text = re.sub("<.*?>", "", text)
    text = re.sub("\">", "", text)
    text = re.sub("\" role=\"main", "", text)
    
    # remove spaces and tabs
    text = re.sub("\t", " ", text)
    text = re.sub("\n", " ", text)
    text = re.sub("[ ]{2,8}  ", " ", text)
    text = re.sub("^ ", "", text)
    # remove unwanted text
    text = re.sub("Enregistrer", "", text)
    text = re.sub("Navigation des articles", "", text)
    text = re.sub("← Précédent", "", text)
    text = re.sub("Suivant →", "", text)
    text = re.sub("Laisser un commentaire", "", text)
    text = re.sub("🙂", " :-) ", text)
    text = re.sub("😉", " ;-) ", text)
    return text


def get_numwords(text):
    text = re.split(" ", text)
    text = [word for word in text if word]
    numwords = len(text)
    return numwords


def check_language(text):
    from langdetect import detect_langs
    from langdetect import detect
    #result = detect_langs(text)
    #language = str(result[0])[0:2]
    try:
        language = detect(text)
    except:
        language = "xx"
    return language


def save_text(text, txtfolder, filename, language):
    filepath = txtfolder+str(language) + "_" + str(filename)+".txt"
    with open(filepath, "w") as outfile: 
        outfile.write(text)


def get_metadata(html, filename):
    blog,post = filename.split("_")
    url = "http://" + blog + ".hypotheses.org/" + str(post)
    metadata = [filename, url, blog, post]
    author = re.findall("rel=\"author\">(.*?)</a>", html)
    if author:
        metadata.append(author[0])
    else:
        metadata.append("N/A")
    date = re.findall("dcterms:created\" content=\"(.*?)\"", html)
    if date:
        date = date[0]
        metadata.append(date)
        month = date[0:7]
        metadata.append(month)
    else:
        metadata.append("N/A")
        metadata.append("N/A")
    return metadata
    

def save_metadata(allmetadata):
    columns = ["id", "url", "blog", "post", "author", "date", "month", "lang", "numwords"]
    allmetadata = pd.DataFrame(allmetadata, columns=columns)
    #print(allmetadata)
    allmetadata.to_csv("metadata.csv", sep=";")


def extract_data(htmlfolder, txtfolder):
    if not os.path.exists(txtfolder): 
        os.makedirs(txtfolder)
    allmetadata = []
    for htmlfile in glob.glob(htmlfolder+"*.html"):
        # Extract and save the text
        html = read_html(htmlfile)
        filename = get_filename(htmlfile)
        text = get_text(html)
        text = clean_text(text)
        language = check_language(text)
        numwords = get_numwords(text)
        save_text(text, txtfolder, filename, language)
        # Extract and save the metadata
        metadata = get_metadata(html, filename)
        metadata.append(language)
        numwords = get_numwords(text)
        metadata.append(numwords)
        allmetadata.append(metadata)
    save_metadata(allmetadata)


# =====================================
# Analyze the metadata
# =====================================


def open_metadatafile(metadatafile):
    with open(metadatafile, "r") as infile:
        metadata = pd.DataFrame.from_csv(infile, sep=";")
        #print(metadata.head())
        return metadata


def check_authordata(metadata):
    authordata = metadata.loc[:,"author"]
    numentries = len(authordata)
    numauthors = len(set(authordata))
    print("number of authors", numauthors)
    entries = Counter(list(authordata))
    #print(entries)
    entries = dict(entries)
    entries = list(entries.values())
    #print(entries)
    sum = np.sum(entries)
    mean = np.mean(entries)
    median = np.median(entries)
    std = np.std(entries)
    print("sum, mean, median post per author:", sum, mean, median, std)
    return authordata


def check_postdata(metadata):
    postdata = metadata.loc[:,"numwords"]
    numentries = len(postdata)
    #print(sorted(list(postdata)))
    sum = np.sum(postdata)
    mean = np.mean(postdata)
    median = np.median(postdata)
    std = np.std(postdata)
    print("sum, mean, median std words per post:", sum, mean, median, std)
    return postdata


def check_langdata(metadata):
    langdata = metadata.loc[:,"lang"]
    langcount = Counter(list(langdata))
    print(langcount)


def plot_data(postdata):
    import matplotlib.pyplot as plt
    import seaborn as sns
    plot = sns.distplot(postdata, bins=3, rug=False, hist=True, kde=True)
    plt.savefig("post-length-histogram.png")
    plot = sns.violinplot(postdata)
    plt.savefig("post-length-violinplot.png")
    plot = sns.boxplot(postdata)
    plt.savefig("post-length-boxplot.png")


def find_cases(metadata):
    metadata = metadata.groupby("author")
    count = 0
    for name, group in metadata:
        langs = list(group.loc[:,"lang"])
        lang = Counter(langs).most_common()[0][0]
        numwords = sorted(list(group.loc[:,"numwords"]), reverse=True)
        if lang == "fr" and len(numwords) > 12 and numwords[2] > 2000 and numwords[11] > 200:
            count +=1
            print(count, lang, name, numwords[0:12])
    

def analyze_metadata(metadatafile):
    metadata = open_metadatafile(metadatafile)
    authordata = check_authordata(metadata)
    postdata = check_postdata(metadata)
    langdata = check_langdata(metadata)
    plot_data(postdata)
    find_cases(metadata)




























