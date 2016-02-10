# -*- coding: utf-8 -*-
"""
@author: Ulrike Henny
@filename: qualitychecking.py

Submodule for checking the orthography of a text collection. The expected input are plain text files.

To install further dictionaries: sudo apt-get install myspell-es (etc.)
See http://pythonhosted.org/pyenchant/ for more information about the spellchecking library used
"""

import enchant
from enchant import checker
from enchant.tokenize import get_tokenizer
import collections
import pandas as pd
import os
import glob
import sys
import re
import csv


##########################################################################
def check_collection(inpath, outpath, lang, wordFiles=[]):
    """
    Checks the orthography of the text in a collection. The expected input are plain text files.
    
    Arguments:
    inpath (string): path to the input files, including file name pattern
    outpath (string): path to the output file, including the output file's name
    lang (string): which dictionary to use, e.g. "es", "fr", "de"
    nefile (string): optional; path to file with named entity list (which will not be treated as errors)
    """

    try:
        enchant.dict_exists(lang)
        try:
            tknzr = get_tokenizer(lang)
        except enchant.errors.TokenizerNotFoundError:    
            tknzr = get_tokenizer()
        chk = checker.SpellChecker(lang, tokenize=tknzr)
        
    except enchant.errors.DictNotFoundError:
        print("ERROR: The dictionary " + lang + "doesn't exist. Please choose another dictionary.")
        sys.exit(0)

    all_words = []
    all_num = []
    all_idnos = []

    print("...checking...")
    for file in glob.glob(inpath):
        idno = os.path.basename(file)[-10:-4]
        all_idnos.append(idno)
        
        err_words = []

        with open(file, "r", encoding="UTF-8") as fin:
            intext = fin.read().lower()
            chk.set_text(intext)

        if len(wordFiles) !=0:
            allCorrects = ""
            for file in wordFiles:
                with open(file, "r", encoding="UTF-8") as f:
                     corrects = f.read().lower()
                     allCorrects = allCorrects + corrects

        for err in chk:
            if not wordFiles or err.word not in allCorrects: 
                err_words.append(err.word)
            all_words.append(err_words)

        err_num = collections.Counter(err_words)
        all_num.append(err_num)
        
        print("..." + str(len(err_num)) + " different errors found in " + idno)
        
    df = pd.DataFrame(all_num,index=all_idnos).T
    
    df = df.fillna(0)
    df = df.astype(int)
    
    df["sum"] = df.sum(axis=1)
    df = df.sort("sum", ascending=False)

    df.to_csv(outpath)
    print("done")


########################################################################
def correct_words(errFolder, corrFolder, substFile):
    """
    Corrects misspelled words in TEI files.
    
    Arguments: 
    teiFolder (string): Folder in which the TEI files with errors are.
    outFolder (string): Folder in which the corrected TEI files will be stored.
    substFile (string): CSV file with "error, corrected" word, one per line.
    """
    
    print("correct_words...")
    ## Create a dictionary of errors and correct words from a CSV file.
    with open(substFile, "r") as sf:
        subst = csv.reader(sf)
        substDict = {}
        for row in subst:
            key = row[0]
            if key in substDict:
                pass
            substDict[key] = row[1]
    
    ## Open each TEI file and replace all errors with correct words.
    teiPath = os.path.join(errFolder, "*.xml")
    for teiFile in glob.glob(teiPath):
        with open(teiFile,"r") as tf:
            filename = os.path.basename(teiFile)
            print(filename)
            text = tf.read()
            for err,corr in substDict.items(): 
                text = re.sub(err,corr,text)
        
        ## Save each corrected file to a new location.
        with open(os.path.join(corrFolder, filename),"w") as output:
            output.write(text) 



##########################################################################
def main(inpath, outpath, lang, wordFiles, errFolder, corrFolder, substFile):
    check_collection(inpath, outpath, lang, wordFiles)
    correct_words(errFolder, corrFolder, substFile)
    
if __name__ == "__main__":
    check_collection(int(sys.argv[1]))
    correct_words(int(sys.argv[1]))


