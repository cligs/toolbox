#!/usr/bin/env python3
# Filename: run_hypoposts.py


"""
# Function to build corpora from hypotheses.org blog data.
# Bulk download, metadata extraction, plain text extraction.
#
# This is the parameter and control script.
"""


import hypoposts
from os.path import join


# ========================================
# Parameters
# ========================================


wdir = "/media/christof/data/Dropbox/0-Analysen/2017/hypoposts/all/" 
urlfile = join(wdir, "urls-missing.txt")
htmlfolder = join(wdir, "html", "")
txtfolder = join(wdir, "txt", "")
minlength = 50
metadatafile =  join(wdir, "metadata.csv")
collfolder = join(wdir, "coll", "")
languages = ["de"]
numposts = 3
textlengths = [5000, 4000, 3000, 2000, 1500, 1000, 500, 250]
variability = 0.2


# ========================================
# Functions 
# ========================================


# hypoposts.get_hypoposts(urlfile, htmlfolder)
# hypoposts.extract_data(htmlfolder, txtfolder, minlength)
# hypoposts.analyze_metadata(metadatafile)
hypoposts.build_collection(metadatafile, languages, numposts, textlengths, variability)


















