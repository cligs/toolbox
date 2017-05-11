# -*- coding: utf-8 -*-
"""
Created on Mon May  8 11:39:12 2017

@author: #jct


"""
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import re
import os
import glob
from collections import Counter
import time
start_time = time.time()

def open_file(doc):
    """
    """
    file_name  = os.path.splitext(os.path.split(doc)[1])[0]
    print(file_name)
    with open(doc, "r", errors="replace", encoding="utf-8") as fin:
        text = fin.read()
        fin.close()
    return file_name, text

def preprocess_text(text, case_sensitive, keep_puntuaction):
    """
    """
    text = re.sub(r"[\n\t]+", " ", text)
    if case_sensitive == False:
        text = text.lower()
    if keep_puntuaction == True:
        substitue = re.compile(r"[\w]+|[¶\(»\]\?\.\–\!’•\|“\>\)\-\—\:\}\*\&…¿\/=¡_\"\'·+\{\#\[;­,«~]")
    else:
        substitue = re.compile(r"[\w]+")
    text = re.findall(substitue, text)
    return text

def corpus2dict(wdir, corpus_dir, text_format, case_sensitive, keep_puntuaction):
    """
    """
    corpus = {}
    for doc in glob.glob(wdir+corpus_dir+"*." + text_format):
        file_name, text = open_file(doc)
        text = preprocess_text(text, case_sensitive, keep_puntuaction)
        corpus[file_name] = text
    return corpus

def make_wordlist(corpus):
    """
    """
    list_tokens = [token for text in list(corpus.values()) for token in text]
    print("Total amount of features", len(list_tokens))
    wordlist = sorted(list(set(list_tokens)))
    return wordlist

def corpus2df(corpus, wordlist, wdir, save_files, print_freq_list_raw=True):
    """
    """
    df_corpus = pd.DataFrame(0, columns = wordlist, index = corpus.keys())

    for file, text in corpus.items():
        for token, frequency in Counter(text).items():
            df_corpus.set_value(file, token, frequency)

    if print_freq_list_raw == True:
        df_corpus = df_corpus.T
        df_corpus["sum"]=df_corpus.sum(axis="columns")
        df_corpus = df_corpus.sort_values(by="sum", ascending=False)
        df_corpus.to_csv(wdir+"freq_table_raw.csv", sep='\t', encoding='utf-8', index=True)
        del df_corpus['sum']
        df_corpus = df_corpus.T
    
    return df_corpus

def process_frequencies(df_corpus, wdir, min_MFF, max_MFF):
    """
    This script normalise and cut the ammount of words that we are analysing.
    """
    # Normalization of the frequencies by the sum of the text
    df_corpus = df_corpus.loc[:].div(df_corpus.sum(axis='columns'), axis="index")

    # The dataframe gets a new summatory column that we use to order the df    
    df_corpus = df_corpus.T
    df_corpus["sum"]=df_corpus.sum(axis="columns")
    df_corpus = df_corpus.sort_values(by="sum", ascending=False)
    
    # Only a given amount of words is taken
    df_corpus = df_corpus[min_MFF:max_MFF]
    # Summatory column is deleted and the df goes back to its normal format
    del df_corpus['sum']
    df_corpus = df_corpus.T
    # The table is saved as csv
    df_corpus.to_csv(wdir+"freq_table.csv", sep='\t', encoding='utf-8', index=True)

    return df_corpus

def main(wdir, corpus_dir = "corpus/", text_format = "txt", case_sensitive = False, keep_puntuaction = True, analyse_corpus = False, save_files = True, min_MFF=0, max_MFF=5000):
    """
    The main function of this script. It takes the takes from a folder and creates a dataframe with the texts as rows and each feature (normally tokens) as columns:
    
    Parameters:
    + wdir: (string) (mandatory!) working directory; it should end with "/"
    * corpus_dir: (string) subfolder in wdir. corpus/ as default
    * text_format: (string) ending of the files: txt (default), xml
    * case_sensitive: (boolean) it defines if it should be case sensitive or not (defatul False)
    * keep_puntuaction: (boolean) it defines if the punctuation should be kept or not (default True) 
    * analyse_corpus: (boolean)  it defines if you want a txt file with an analyse of the corpus (it can take a while!) (default False)
    * save_files: (boolean) it defines if files like freq_list or wordlist should be saved (default True)
    * min_MFF: (int) minimum number of Most Frequent Features (F because not always are words!) (default 0)
    * max_MFF: (int) maximum number of Most Frequent Features (default 5000)


    Simple example of how to use it:
    
        from toolbox.extract import corpus2table
        corpus2table.main("/home/jose/cligs/experiments/20170508 starting_ml/")

    More complicated example of how to use it:

        from toolbox.extract import corpus2table
        corpus2table.main(
            wdir, corpus_dir = "elotrocorpus/", 
            text_format = "xml", 
            case_sensitive = True, 
            keep_puntuaction = False, 
            analyse_corpus = True,
            save_files = False,
            max_MFW=1000     
        )
        
    """
    corpus = corpus2dict(wdir, corpus_dir, text_format, case_sensitive, keep_puntuaction)
    
    wordlist = make_wordlist(corpus)
    
    df_corpus = corpus2df(corpus, wordlist, wdir, save_files)
    print("Original corpus' shape: ",df_corpus.shape)

    df_corpus = process_frequencies(df_corpus, wdir, min_MFF, max_MFF)

    print("Processed corpus' shape: ",df_corpus.shape)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    return df_corpus

