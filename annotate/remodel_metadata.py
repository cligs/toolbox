# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:29:35 2016

@author: jose
"""

import pandas as pd
import os


def remodel_metadata(input_metadata,input_remodel_keywords, list_metadata, list_numerical_metadata, list_number_frontier):
    """
    This script remodel the metadata from the corpus using the new moedl in a keywords file with column called "new_model". The idea is to simplify into less categories (many times binary values) in order to compare better its capacity to distinguish cluster in a corpus
   
    Example of how to use it:
    
    df_metadata = remodel_metadata(
                                    input_metadata = "/home/jose/cligs/ne/metadata_beta-opt-obl-prueba.csv",
                                    input_remodel_keywords = "/home/jose/cligs/ne/keywords-prueba.csv",
                                    list_metadata = ['narrative-perspective','narrator','protagonist-gender'],
                                    list_numerical_metadata = ['time-span','text-histlit-pages'],
                                    list_number_frontier = ['author-year-change']
                                    )    
    
    """
    # Lets open the csvs for metadata and keywords
    df_metadata = pd.read_csv(input_metadata, encoding="utf-8", sep=",")
    df_keywords = pd.read_csv(input_remodel_keywords, encoding="utf-8", sep="\t")

    # We create multiindex for the columns of the keywords that we need
    df_keywords.set_index(['term_type','term_value'], inplace=True)
    idx = pd.IndexSlice

    # We take the columns that we need form the categorical metadata
    for col in list_metadata:
        df_metadata[col] = df_metadata[col].map(df_keywords.loc[idx[col,:]]['new_model'])

    # Now we take the numerical values
    for col in list_numerical_metadata:
        median = df_metadata[col].median()
        df_metadata.ix[df_metadata[col] < median, col] = 0
        df_metadata.ix[df_metadata[col] >= median, col] = 1

    # And now we to the same with the special catgeory "author-year-change". You probably don't want to use it, so leave the list_number_frontier empty
    for col in list_number_frontier:
        df_metadata.ix[df_metadata[col] < df_metadata['year'], col] = 0
        df_metadata.ix[df_metadata[col] >= df_metadata['year'], col] = 1
    
    output_metadata = os.path.splitext(input_metadata)[0]+"_newmodel.csv"   
    df_metadata.to_csv(output_metadata, sep='\t', encoding='utf-8')    
    #print (df_metadata)
