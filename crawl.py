#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: activate_toolbox.py
# Author: Christof Schöch (cf)
# Version: 0.1.0, January 2016


"""
# Scripts for gathering data from a website.
"""


import requests
import codecs
import glob
import os


####################################################################
def crawl_tc(baseURL, itemsFile, encoding, outFolder):
    """
    Gathers XML-TEI files from the Théâtre classique collection.
    Requires a list of the XML files extracted from the HTML page.
    """

    print("\ncrawl_tc...")
    ## Get a list of items to append to the base URL
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)
    with open(itemsFile, "r") as infile:
        items = infile.read().splitlines() 
        #print(items)
    ## For each item, construct the URL of each file to download
    for item in items: 
        itemURL = baseURL + item
        #print(itemURL)
        ## Download and save the text document
        try:
            doc = requests.get(itemURL, timeout=3.1)
            print("Downloaded", item)
            #print("URL:", doc.url)
            #print("Encoding:", doc.encoding)
            doc.encoding = "latin-1"
            #print("Encoding:", doc.encoding)
            #print(doc.text[10000:10500])
            outPath = outFolder + item
            with open(outPath, "w", encoding=encoding) as outFile:
                outFile.write(doc.text)
        ## Exception fangen und überspringen
        except Exception as exc:
            print("Error with", item, exc)


#########################################################################
def convert_encoding(sourceFolder, targetFolder, sourceEnc, targetEnc): 
    """
    Convert files from one character encoding to another.
    """
    print("\nconvert_encoding...")
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    sourcePath = sourceFolder + "*.xml"
    for file in glob.glob(sourcePath): 
        ## Get the input and output file names.
        sourceFileName = file
        #print(sourceFileName)
        targetFileName = targetFolder + os.path.basename(sourceFileName)
        #print(targetFileName)
        ## Read the original file and write it in the target encoding.
        #BLOCKSIZE = 1048576 # or some other, desired size in bytes
        with codecs.open(sourceFileName, "r", sourceEnc) as sourceFile:
            with codecs.open(targetFileName, "w", targetEnc) as targetFile:
                while True:
                    contents = sourceFile.read()
                    if not contents:
                        break
                        print("Error", os.path.basename(sourceFileName))
                    targetFile.write(contents)
                    #print("Converted", os.path.basename(sourceFileName))




def main(baseURL, itemsFile, outFolder):
    crawl_tc(baseURL, itemsFile, outFolder)
    convert_encoding(sourceFolder, targetFolder, sourceEnc, targetEnc) 

if __name__ == "__main__":
    import sys
    crawl_tc(int(sys.argv[1]))
    convert_encoding(int(sys.argv[1]))

