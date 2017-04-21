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
from bs4 import BeautifulSoup as soup
import html
import pandas as pd
from collections import Counter
import numpy as np
import shutil
import csv


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
        result = rq.get(url, timeout=2)
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
    """
    Reads the HTML file to a string.
    Removes some potential trouble makers.
    """
    with open(htmlfile, "r") as infile:
        html = infile.read()
        html = re.sub("<div class=\"wp-about-author.*?</div>", "", html, re.S)
        html = re.sub("<em>", "", html)
        html = re.sub("</em>", "", html)
        html = re.sub("<i>", "", html)
        html = re.sub("</i>", "", html)
        return html


def get_filename(htmlfile):
    filename, ext = os.path.basename(htmlfile).split(".")
    #print(filename)
    return filename


def get_title(html, filename): 
    """
    Looks for the title of the blog post. 
    """
    html = soup(html, "html.parser")
    title = html.find_all("h1", ["post-title entry-title", "entry-title"])
    if title:
        title = title[0].string
        try:
            title = re.sub(";", "_", title)
        except:
            print("WARNING: problem with title", filename)
            title = "N/A"
    #print(title)
    #print(type(title))
    return title


def clean_text(text):
    """
    Removes some remaining stuff from the text.
    """
    # Removes any links
    #text = re.sub("http.*?[ \n]", " ", text)
    # Removes some special signs which disturb processing
    text = re.sub("🙂", " :-) ", text)
    text = re.sub("😉", " ;-) ", text)
    text = re.sub("More Posts  - Website Follow Me:", "", text)
    text = re.sub("Website Follow Me:", "", text)
    # Removes unnecessary whitespace
    text = re.sub("\t", " ", text)
    text = re.sub("\n", " ", text)
    text = re.sub("[ ]{2,8}  ", " ", text)
    text = re.sub("^ ", "", text)
    return text


def get_text(html, filename):
    """
    Does the actual extraction of the text from the HTML.
    Uses Beautiful Soup to do so.
    """
    html = soup(html, "html.parser")
    text = ""
    divs = html.find_all("div", ["entry-inner", "entry-content", "content"])
    if divs: 
        for div in divs: 
            div = div.get_text()
            text = text + str(div) + "\n"
    else: 
        print("ERROR: no text found.", filename)
        text = "N/A"
    text =  clean_text(text)
    return text


def get_category(text, title): 
    """
    Makes a guess at the type of blog post.
    Particularly tries to identify conference programms and CfPs.
    """
    try: 
        text = text.lower()
        title = title.lower()
    except:
        print("WARNING: problem with category")
    # Evidence for conference programme
    conf = 0
    if "programm" in title or "programme" in title or "program" in title: 
        conf +=2
    if "programm" in text or "programme" in text or "program" in text: 
        conf +=1
    if "accueil" in text or "Begrüßung" in text or "welcome" in text: 
        conf +=1
    # Evidence for call for papers
    call = 0    
    if "call for papers" in title or "appel à contributions" in title or "tagungsausschreibung" in title: 
        call +=2
    if "call for papers" in title or "appel à contributions" in title or "tagungsausschreibung" in text: 
        call +=1
    if "deadline" in text or "date limite" in text or "frist" in text: 
        call +=1
    if call > 1:
        category = "call"
    elif conf > 1: 
        category = "conf"
    else: 
        category = "N/A"
    return category
        

def get_numwords(text):
    """
    Estimates the length of the plain text in number of words.
    """
    text = re.split(" ", text)
    text = [word for word in text if word]
    numwords = len(text)
    return numwords


def check_language(text):
    """
    Detects the language of the post from the full text.
    (The metadata with regard to language are often unreliable.)
    """
    from langdetect import detect
    try:
        language = detect(text)
    except:
        language = "xx"
    return language


def get_licence(html):
    """
    Searches the HTML content for a mention of a CC licence.
    """
    if "creative-commons" in html or "Creative Commons" in html: 
        licence = "CC"
    else: 
        licence = "N/A"
    return licence


def save_text(text, txtfolder, filename):
    """
    Saves the extracted text to a TXT file.
    """
    filepath = txtfolder + str(filename) + ".txt"
    with open(filepath, "w") as outfile: 
        outfile.write(text)


def get_author(html):
    author = re.findall("rel=\"author\">(.*?)</a>", html)
    if author:
        author = author[0]
        author = re.sub(";", "_", author)
    else:
        author = "N/A"
    return author


def get_date(html):
    date = re.findall("dcterms:created\" content=\"(.*?)\"", html)
    if date:
        date = date[0]
    else:
        date = "N/A"
    return date
    

def get_metadata(html, text, filename):
    """
    Collects the metadata.
    Calls other functions (above) for most elements.
    """
    blog, post = filename.split("_")
    url = "http://" + blog + ".hypotheses.org/" + str(post)
    title = get_title(html, filename)
    author = get_author(html)
    date = get_date(html)
    licence = get_licence(html)
    language = check_language(text)
    category = get_category(text, title)
    numwords = get_numwords(text)
    metadata = [filename, language, author, numwords, category, date, licence, blog, post, url, title]
    return metadata


def create_metadatafile():
    columns = ["filename", "language", "author", "numwords", "category", "date", "licence", "blog", "post", "url", "title"]
    metadata = pd.DataFrame(columns=columns)
    metadata.to_csv("metadata.csv", sep=";", index=False)
    

def save_metadata(metadata):
    """
    Saves the collected metadata to a CSV file.
    Works incrementally.
    """
    with open("metadata.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(metadata)


def extract_data(htmlfolder, txtfolder, minlength):
    """
    Extracts the plain text of the actual blog post body and metadata.
    """
    if not os.path.exists(txtfolder): 
        os.makedirs(txtfolder)
    create_metadatafile()
    for htmlfile in glob.glob(htmlfolder+"*.html"):
        filename = get_filename(htmlfile)
        print("Now working on", filename)
        html = read_html(htmlfile)
        # Extract text and metadata
        text = get_text(html, filename)
        metadata = get_metadata(html, text, filename)
        # Save metadata and text
        numwords = metadata[3]
        if numwords > minlength:
            save_metadata(metadata)
            save_text(text, txtfolder, filename)
            print("====== OK", numwords, filename)
        else:
            print("TOO SHORT", numwords, filename)










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
    #print(langcount)


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
        if lang == "de" and len(numwords) > 12 and numwords[2] > 3000 and numwords[11] > 800:
            count +=1
            print(count, lang, name, numwords[0:12])
    

def analyze_metadata(metadatafile):
    metadata = open_metadatafile(metadatafile)
    authordata = check_authordata(metadata)
    postdata = check_postdata(metadata)
    langdata = check_langdata(metadata)
    plot_data(postdata)
    find_cases(metadata)









# ======================================
# Build a test collection for stylometry
# ======================================


def identify_authors(metadata, collcriteria):
    """
    Identify the authors who correspond to the basic criteria.
    """
    metadata = metadata.groupby("author")
    authors = []
    for name, group in metadata:
        langs = list(group.loc[:,"lang"])
        lang = Counter(langs).most_common()[0][0]
        numwords = sorted(list(group.loc[:,"numwords"]), reverse=True)
        if lang == collcriteria[0]:
            if len(numwords) > 9 and numwords[2] > collcriteria[1] and numwords[5] > collcriteria[2] and numwords[8] > collcriteria[3]:
                authors.append(name)
    print(len(authors), authors)
    return authors


def identify_posts(metadata, collcriteria, authors):
    """
    Identify the posts by selected authors which correspond to more precise criteria.
    """
    metadata = metadata.groupby("author")
    selposts = []
    for name, group in metadata:
        if name in authors:
            filter_category = "numwords"
            lower_bound = collcriteria[1]-501
            upper_bound = collcriteria[1]+501
            myquery = str(lower_bound) + "<" + filter_category + "<" + str(upper_bound)
            filtered = group.query(myquery)
            if len(filtered) > 2:
                posts = filtered.loc[:,"id"]
                selposts.extend(posts)
    print(selposts)
    return selposts
            

def copy_files(selposts, txtfolder, collfolder):
    """
    Copy the right files to a new folder.    
    """
    if not os.path.exists(collfolder):
        os.makedirs(collfolder)
    source = txtfolder
    destination = collfolder
    counter = 0
    for file in glob.glob(source+"*.txt"):
        basename = os.path.basename(file)
        filename,ext = basename.split(".")
        idno = filename[3:]
        #print(idno)
        if idno in selposts:
            counter +=1
            shutil.copy(file, destination)


def rename_files(collfolder, metadata, category1, category2):
    """
    Renames files based on metadata.
    """
    for file in glob.glob(collfolder+"*.txt"):
        ## Get labels from metadatafile for primary and secondary category.
        basename = os.path.basename(file)
        filename, ext = basename.split(".")
        idno = filename[3:]
        metadatax = metadata.set_index("id", drop=True)
        label1 = metadatax.loc[idno, category1]
        label2 = metadatax.loc[idno, category2]
        ## Construct new filename
        newfilename = str(label1) + "_" + str(label2) + "-" + str(basename) 
        newoutputpath = collfolder + newfilename
        os.rename(file, newoutputpath)   


def build_collection(metadatafile, txtfolder, collfolder, collcriteria):
    metadata = open_metadatafile(metadatafile)
    authors = identify_authors(metadata, collcriteria)
    selposts = identify_posts(metadata, collcriteria, authors)
    copy_files(selposts, txtfolder, collfolder)
    rename_files(collfolder, metadata, category1="author", category2="numwords")
    
    
    
























