# ./bin/env python3
# copy_subset.py
# author: #cf, #jct
# v0.5, 2017-05-03. 

"""
# Select a subset of text files from a larger text collection. The main function is copy_subset.

"""

import glob
import pandas as pd
import os
import shutil

def categorical_filtering(metadata, filter_feature = "genre", filter_value=["novel"]):

    ## USER: For categorical criteria, set filter category (column) and list of values to be selected.
    filter_feature = filter_feature # author_short, genre, subgenre, availability, decade, etc.
    values_list = filter_value # See metadata file for possible values
    metadata = metadata[metadata[filter_feature].isin(values_list)]
    print("categorical filter: ",metadata.shape)
    return metadata

def numerical_filtering(metadata, filter_feature = "year", lower_bound="1799", upper_bound="1900"):
    # jct: I am not sure if this is still working...
    ## USER: And/or, for numeric criteria, set a filter category and upper and lower bound.
    filter_feature = filter_feature
    lower_bound = lower_bound
    upper_bound = upper_bound
    myquery = lower_bound + "<" + filter_feature + "<" + upper_bound 
    metadata = metadata.query(myquery)
    print(metadata.shape)
    return metadata

def categorical_sampling(metadata, sampling_feature, value, identifier):

    # We creeate a groupby element using the sampling feature and using the first column (iloc[:,0]) to sum it; the result is a series
    grouped = metadata.groupby(sampling_feature).count().iloc[:,0]
    # We filter this using the value that we have given and get a list of the values that are represented with more than the given value
    approved_features = list(grouped[grouped >= value].index)
    # We use this information to delete all the features (authors) that don't have more than 3 texts
    metadata = categorical_filtering(metadata, filter_feature = sampling_feature, filter_value = approved_features)

    #TODO: We could build here more steps, like for example select works of the same author with the maximal distance in years...
    
    # We make a nice list comprehension where we use the sample function of pandas for each feature (author) to choose the texts randomly. We get a list of the ids
    #TODO: There is an option of use a seed to the sampling thing. Should we use it?
    id_texts = [item for feature in approved_features for item in list(metadata[metadata[sampling_feature] == feature].sample(n = value)[identifier]) ]

    # We filter again the metadata using the list of the ids
    metadata = categorical_filtering(metadata, filter_feature = identifier, filter_value = id_texts)
    print("sample filter: ",metadata.shape)
    return metadata

def copy_subset(wdir, fullset, metadata, outfolder, categorical_filters = [{"genre":["novel"]}], numerical_filters = [], categorical_sample_filters = [["author-name",3]], identifier = "idno"):
    """ Select a subset of text files from a larger text collection.

    Parameters:
        * wdir : (string) the basic path
        * fullset: (string) the subpath where the texts actually are
        * metadata: (string) name of the file for metadata
        * outfolder: (string) name of the subpath where you want the subcorpus
         categorical_filters: (list of dictionaries) the different categories that we want to filter by; for example, if we want to filter by genre taking only novel and essay, we would use: [{"genre":["novel","essay"]}]
         numerical_filters: (list of dictionaries) the different ranges that we want to filter by (does it work?)
         categorical_sample_filters: (list of lists) the different categories that we want to sample by, with the minimum value. For example: categorical_sample_filters = [["author-name",3]] means that we want to sample taking 3 texts from each author (if an author does not have so many texts, none of his texts will be used for the subcorpus)
         identifier: (string) name of the column with the identifier

    Example of how to use it:
    copy_subset("/home/jose/cligs/ne/", "master/*.xml", "metadata_obl.csv", "subset_df/")

    """
    
    ## Read metadata from file
    metadata = pd.read_csv(wdir+metadata, delimiter=',', index_col=0)
    #print(metadata.head())

    ## Filter the metadata table by one or several criteria
    for categorical_filter in categorical_filters:
        for key, values in categorical_filter.items():
            metadata = categorical_filtering(metadata, filter_feature = key, filter_value = values)

    for numerical_filter in numerical_filters:
        for key, values in numerical_filter.items():
            metadata = numerical_filtering(metadata, key, values[0], values[1])

    ## Sample the metadata using a category and a fixed value
    for categorical_sample_filter in categorical_sample_filters:
        metadata = categorical_sampling(metadata, sampling_feature = categorical_sample_filter[0], value = categorical_sample_filter[1], identifier = identifier)

    ## Create a list of filenames corresponding to the filter criteria.
    subset = []
    for item in metadata.index:
        subset.append(item)
    #print(subset)
    
    ## Copy the right files to a new folder.    
    if not os.path.exists(wdir+outfolder):
        os.makedirs(wdir+outfolder)
    source = wdir+fullset
    destination = wdir+outfolder
    counter = 0
    for file in glob.glob(source):
        basename = os.path.basename(file)
        idno = basename[0:6]
        #print(file)
        #print(idno, basename)
        #print(wdir+outfolder+basename)
        if idno in subset:
            counter +=1
            shutil.copy(file, destination)
            
    print("Files selected and copied: "+ str(len(subset)) +","+ str(counter))


#main("/home/christof/Repos/cligs/romanfrancais/", "master/*.xml", "metadata.csv", "subset_df/")
#copy_subset("/home/jose/cligs/ne/", "master/*.xml", "metadata_obl.csv", "subset_df/")