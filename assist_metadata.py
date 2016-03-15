# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob

def get_names(wdir, txtFolder):
    """
    This function gives you a dataframe with the proper names (searched with a regexp) found in a file.
    It should be useful to know who the protagonist is, or where the action of the text takes place.
    The regexps are thought for Spanish. In stead of [a-zá-úñüç] we could be using \w if the English speaking comunity had thought that other languages have other characters and our regexp would be much more elegant...

    wdir is the path of the gile
    txtFolder is the name (without format ending) of the file to be analized

    Example of how to use it at the console:
    
    df = get_names("/home/jose/CLiGS/ne/master/", "ne0002")
    """
    #Lets open the file
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            #We create a list for the names
            names=[]
            # We search for any word that starts with capital letter and that before didn't have anything that looks like an starting of a sentence
            names = re.findall(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+)', content)

            # We delete the duplicated items in the list            
            names=list(set(names))
            #print(names)
            
            # Now we put the list in a data frame
            df=pd.DataFrame(names,columns=["name"])
            #print(df)
            #And we add a new column for the frequency and we fill it with zeros
            df["frequency"]=0
            #print(df)

            # Now, for every row, we take the indexes and the other columns with the real values (names and frequency)            
            for index, row in df.iterrows():
                # For each, we fill the frecuency with the the amount (len) of a times that the name appears in the text with something 
                df.at[index,"frequency"] = len(re.findall(r'[^a-zá-úçñüA-ZÁ-ÚÜÑ\-]'+ re.escape(row["name"]) + r'[^a-zá-úçñüA-ZÁ-ÚÜÑ\-]', content))
            df=df.sort(["frequency"], ascending=True)
            print(df)
            return df