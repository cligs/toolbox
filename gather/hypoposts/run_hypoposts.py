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


wdir = "/media/christof/data/Dropbox/0-Analysen/2017/hypoposts/2015/" 
urlfile = join(wdir, "urls.txt")
htmlfolder = join(wdir, "html", "")
txtfolder = join(wdir, "txt", "")
metadatafile =  join(wdir, "metadata.csv")


# ========================================
# Functions 
# ========================================


hypoposts.get_hypoposts(urlfile, htmlfolder)
# hypoposts.extract_data(htmlfolder, txtfolder)
# hypoposts.analyze_metadata(metadatafile)


















