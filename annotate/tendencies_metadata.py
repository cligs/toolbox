# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:29:35 2016

@author: jose
"""

import pandas as pd
from collections import Counter
import os

def find_tendencies(input_metadata):
    """
    This script finds the mode and the median of numeric values from a table of metadata.
    Example of how to use it:
    
    find_tendencies("/home/jose/cligs/experiments/20160920 modes in Edad de Plata/metadata_beta-opt-obl-structure.csv")
    """
    
    df_metadata = pd.read_csv(input_metadata, encoding="utf-8", sep=",")    

    # The dataframe is created
    df_results = pd.DataFrame([], columns=["metadata","result1-value","result1-ammount","result2-value","result2-ammount"])

    # the columns of the metadata table are iterated
    for column_name, column_series in df_metadata.iteritems():
        #print(column_name, column_series.dtype)
        # if the column is categorical:
        if column_series.dtype == "object" and column_name != "supergenre" and column_name != "genre":
            # we take the two most common values
            contador = Counter(column_series.values).most_common(2)
            if len(contador) > 1:                
                # and place them in the dataframe
                df_results = df_results.append({"metadata": column_name, 'result1-value': str(contador[0][0]), 'result1-ammount': str(contador[0][1]/df_metadata.shape[0]), 'result2-value': str(contador[1][0]), 'result2-ammount': str(contador[1][1]/df_metadata.shape[0]),}, ignore_index=True)

        # if the column is numerical
        elif column_series.dtype == "int64" or column_series.dtype == "float64":
            # we calculate the median
            median = column_series.median()
            # and place it in the table
            df_results = df_results.append({"metadata": column_name, 'result1-value': median}, ignore_index=True)

    # And print the table as csv file
    output_metadata = os.path.splitext(input_metadata)[0]+"_results_tendencies.csv"
    df_results.to_csv(output_metadata, sep='\t', encoding='utf-8')   
    # And that's it!
