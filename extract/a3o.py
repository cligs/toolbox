#!/usr/bin/env python3


"""
# Script to scrape texts from a3o (Archive of Our Own)
"""

# ========================================
# Parameters
# ========================================

# Generic imports
from os.path import join
import os
import glob
import pandas as pd
import numpy as np

# Specific imports
import re
import requests as rq
import html
from collections import Counter
import shutil
import csv


# ========================================
# Parameters
# ========================================

wdir = "/home/christof/Dropbox/2-Aktionen/1-Aktuell/Newcastle/a3o/" 
htmlfolder = join(wdir, "html", "")
txtfolder = join(wdir, "txt", "")
a3o_base = "https://archiveofourown.org/"
query_base = "https://archiveofourown.org/works/search?commit=Search&page="
query_body =  "&utf8=%E2%9C%93&work_search%5Bbookmarks_count%5D=&work_search%5Bcharacter_names%5D=&work_search%5Bcomments_count%5D=&work_search%5Bcomplete%5D=1&work_search%5Bcreator%5D=&work_search%5Bfandom_names%5D=Harry+Potter+-+J.+K.+Rowling&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bquery%5D=&work_search%5Brating_ids%5D=&work_search%5Brelationship_names%5D=&work_search%5Brevised_at%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsort_column%5D=word_count&work_search%5Bsort_direction%5D=desc&work_search%5Btitle%5D=&work_search%5Bword_count%5D=%3E100000"


# ========================================
# Functions 
# ========================================


def get_ids(query_base, query_body): 
    """
    Based on a specific search query encoded in the query body,
    finds the text identifiers for all matching texts.
    Returns them as a list and saves the list to a text file.    
    """
    all_ids = []
    for page in range(1,67): 
        print(page)
        query = query_base + str(page) + query_body
        try:
            queryresult = rq.get(query, timeout=4)
            queryhtml = queryresult.text
            #print(queryhtml)
        except:
            print("Error receiving HTML")
        try: 
            ids = re.findall("<a href=\"/works/(\d*?)\">", queryhtml)
            all_ids.extend(ids)
            #print(len(all_ids))
        except: 
            print("Error extracting IDs")
    print(len(all_ids), "ids collected")
    for item in all_ids: 
        with open("ids.txt", "a") as output:
            output.write(str(item)+"\n")
    return all_ids


def load_ids():
    """
    Loads the saved text file with text identifiers relevant to the query. 
    Gives them back as a list.
    """
    all_ids = []
    with open("ids.txt", "r") as infile: 
        all_ids = infile.read()
        all_ids = re.split("\n", all_ids)
        all_ids = [item for item in all_ids if item]
        #print(all_ids)
        return all_ids


def get_html(a3o_base, all_ids, htmlfolder): 
    """
    For each work in the list of work identifiers, downloads the
    complete HTML file with the metadata and full HTML text.
    Saves this file to disk.
    """
    for item in all_ids[700:801]: 
        url = a3o_base + "works/" + str(item) + "?view_full_work=true"
        filename = join(htmlfolder, "a3o-"+str(item)+".html")
        #print(filename)
        try: 
            html = rq.get(url, timeout=4)
            html = html.text
            with open(filename, "w") as outfile: 
                outfile.write(html)
            print("OK") 
        except: 
            print("ERROR when downloading file; URL:", url)


def get_tags(htmlfolder): 
    """
    From each downloaded text, extract the tags it is tagged with.
    Saves the list of tags to CSV, one row for each text.
    """
    all_tags = []
    all_titles = []
    all_authors = []
    all_identifiers = []
    for file in glob.glob("html/*.html"): 
        identifier, ext = os.path.basename(file).split(".")
        all_identifiers.append(identifier)
        with open(file, "r") as infile: 
            content = infile.read()
            tags = re.findall("<a class=\"tag\" href=\"/tags/(.*?)/works\">", content)
            tags = [re.sub("%20", "_", tag) for tag in tags]
            title = re.findall("class=\"title heading\">\n(.*?)\n", content)
            title = re.sub("[ ]{3,6}", "", title[0])
            all_titles.append(title)
            author = re.findall("<a rel=\"author\" href=\".*?\">(.*?)</a>", content)[0]
            all_authors.append(author)
            all_tags.append(tags)
    from collections import Counter
    all_tagdicts = []
    for item in all_tags: 
        tagdict = Counter(item)
        all_tagdicts.append(tagdict)
    all_tags = pd.DataFrame(all_tagdicts)
    all_tags.drop([col for col, val in all_tags.sum().iteritems() if val < 30], axis=1, inplace=True)
    all_tags = all_tags.fillna(0)
    all_tags = all_tags.astype(int)
    all_tags["title"] = pd.Series(all_titles)
    all_tags["author"] = pd.Series(all_authors)
    all_tags["identifier"] = pd.Series(all_identifiers)
    #print(all_tags.head())
    all_tags.to_csv("metadata.csv", index=False, header=True)


def get_text(htmlfolder, txtfolder): 
    """
    From each HTML file, extract the text content. 
    Save the text content to a plain text file. 
    """
    for file in glob.glob(join(htmlfolder, "*.html")): 
        identifier, ext = os.path.basename(file).split(".")
        with open(file, "r") as infile: 
            content = infile.read()
            content = re.findall("<!--main content-->(.*?)<!--/main-->", content, re.DOTALL)
            content = ("\n").join(content)
            content = re.sub("</p>", "\n", content)
            content = re.sub("<br/>", "\n", content)
            content = re.sub("<[^>]*?>", "", content)
            content = re.sub("”", "\"", content)
            content = re.sub("“", "\"", content)
            content = re.sub("’", "\'", content)
            content = re.sub("\n\n", "\n", content)
            content = re.sub("\n\n", "\n", content)
            content = re.sub("\n  ", "\n", content)
            filename = join(txtfolder, str(identifier)+".txt")
            with open(filename, "w") as outfile: 
                outfile.write(content)
                


# ========================================
# Main function 
# ========================================

def main(wdir, a3o_base, query_base, query_body, htmlfolder, txtfolder): 
    #all_ids = get_ids(query_base, query_body)
    #all_ids = load_ids()
    #html = get_html(a3o_base, all_ids, htmlfolder) 
    #tags = get_tags(htmlfolder)
    text = get_text(htmlfolder, txtfolder)
    
    

main(wdir, a3o_base, query_base, query_body, htmlfolder, txtfolder)
