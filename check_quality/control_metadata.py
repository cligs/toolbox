# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:29:35 2016

@author: jose
"""

import re
import pandas as pd


def check_metadata(input_metadata,input_keywords):
    """
    
    Example of how to use it:
    check_metadata("/home/jose/cligs/ne/metadata_beta-opt-obl.csv","/home/jose/cligs/reference/keywords/keywords.csv")
    """
    # Lets open the csvs for metadata and keywords
    df_metadata = pd.read_csv(input_metadata, encoding="utf-8", sep=",")
    df_keywords = pd.read_csv(input_keywords, encoding="utf-8", sep="\t")
    
    # We manipulate non typical values from the metada table
    df_metadata = df_metadata.replace(["n.av.", "?", "other", "mixed"], ["", "", "other/mixed", "other/mixed"])
    
    # Other metadata besides the keywords and terms
    other_metadata = ["Unnamed: 0", "idno", "author-name", "title", "year", "genre-subtitle", "availability", "keywords-cert", "decade"]
    
    # We check if the columns of the metadata are in the keywords file:
    print("====\nChecking columns of metadata:")
    for metada in df_metadata.columns.values:
        i = 0
        # We check if the columns of the metadata are in the keywords
        if (len(df_keywords.loc[df_keywords['term_type'] == metada]) == 0) and metada not in other_metadata:
            print(metada, "not found")
            i = i+1 
    if i == 0:
        print("All clean :)")
    else:
        print("found ", i, " problematic columns")
    print("====\n")
    
    
    
    print("====\nChecking values of metadata:")
    # We check if the values of each column are right:
    # We iterate over every row (so it is easier to edit the files):
    for index, row in df_metadata.iterrows():
        i = 0
        # We iterate over the columns (so, over the cells)
        for column_name, column_value in row.iteritems():
            # If the data is not part of the other metadata:
            if column_name not in other_metadata:

                # The values of the kind of list and kind of information are saved in variables
                value_list = df_keywords.loc[df_keywords['term_type'] == column_name]['value_list'].values[0]
                type_data = df_keywords.loc[df_keywords['term_type'] == column_name]['type_data'].values[0]
    
                # if the data is numerical, we see if it follows the regex
                if type_data == "number":
                    if len(re.findall("[^\d\.]+",str(column_value))) == 0:
                        pass
                    else:
                        i = i+1
                        print("problem with number in", row[1], column_name)
                
                # if the list is closed
                if value_list == "closed_list" and type_data == "string":

                    # We check if the value is in the keywords
                    if len(column_value) > 0 and column_value not in df_keywords.loc[df_keywords['term_type'] == column_name]['term_value'].values:
                        i = i+1
                        print("problem in", row[1], column_name,":", column_value, "not found in keywords")

        # Amount of problems in each file
        if i > 0:
            print(row[1],  "contains", i, "problems")
    if i == 0:
        print("All clean :)")
    else:
        print("Total problems in corpus",i)
        
    print("====\n")                  
                    

