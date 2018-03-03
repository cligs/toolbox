# -*- coding: utf-8 -*-
"""
Created on Wed May  3 07:28:41 2017

@author: #jct,

This script uses different other scripts to create a corpus in txt for different use cases. All the parameters are used later by the rest of the scripts.

Description of the parameters (the ones with an asterik are mandatory, the rest have default values):
        * basic_wdir : (string) path of the very basic folder
        * master_wdir : (string)  subpath with the master folgers
        * subset_wdir : (string) the path where you want the subcorpus
        converted_wdir : (string) the path where you want the converted subcorpus.
        metadata_name : (string) name of the metadata that you want to extract and read
        metadata_mode : (string) the mode of the extraction of metadata
        categorical_filters : (list of dictionaries) the categories you want to filter the corpus, given as a list of dictionaries where the keys are the columns and the values are a list of possible values (ex: [{"genre":["novel"]}])
        numerical_filters : (list of dictionaries) (not sure if this option works) the ranges you want to filter the corpus, given as a list of dictionaries where the keys are the columns and the two values are the maximum and possible value (ex [{"year":[1799,1900]}], )
        categorical_sample_filters : (list of lists) the categories that you want to sample your corpus, given as a list of lists with the first value for the category and the second value the minimum number (ex: [["author-name",3]])
        identifier :  (string) name of the column for identifier
        converting : (boolean) do you want to convert?
        convert_format : format to convert it, normally "txt"
        xpath : (string) value of the modes of xpath (): "alltext", "bodytext, "seg" or "said"
        renaming :  (boolean) do you want to convert?
        rename_columns : (list with two elements) 
        
        
Simple and minimal example of how to use it:

from toolbox.extract import prepare_subcorpus
prepare_subcorpus.prepare_subcorpus(
    basic_wdir = "/home/jose/cligs/ne/",
    master_wdir = "master/",
    subset_wdir = "subset/"
    )

More complexed example of how to use it with all the parameters:

from toolbox.extract import prepare_subcorpus
prepare_subcorpus.prepare_subcorpus(
        basic_wdir = "/home/jose/cligs/ne/",
        master_wdir = "master/",
        subset_wdir = "subset/",
        converted_wdir = "texto/", 
        metadata_name = "metadata", 
        metadata_mode = "beta-opt-obl-subgenre-structure", 
        categorical_filters = [{"genre":["novel"]}], 
        numerical_filters = [], 
        categorical_sample_filters = [["author-name",3]], 
        identifier = "idno",
        converting = True, 
        convert_format = "txt", 
        xpath = "bodytext", 
        renaming = True, 
        rename_columns = ["author-name","title"],
    )

Another example for copying only a list of files:

files = ["ne0026","ne0027","ne0033","ne0037","ne0041","ne0044","ne0072","ne0084","ne0107","ne0121","ne0161","ne0192","ne0194","ne0226","ne0228","ne0235","ne0246","ne0253","ne0257","ne0285","ne0292","ne0298","ne0309","ne0036","ne0124","ne0167","ne0274","ne0295"]

from toolbox.extract import prepare_subcorpus
prepare_subcorpus.prepare_subcorpus(
        basic_wdir = "/home/jose/cligs/ne/",
        master_wdir = "master/",
        subset_wdir = "subset/",
        converted_wdir = "texto/", 
        metadata_name = "metadata", 
        metadata_mode = "beta-opt-obl-subgenre-structure", 
        categorical_filters = [{"idno":files}], 
        numerical_filters = [], 
        categorical_sample_filters = [], 
        identifier = "idno",
        converting = True, 
        convert_format = "txt", 
        xpath = "bodytext", 
        renaming = True, 
        rename_columns = ["author-name","title"],
    )
    

"""
from toolbox.extract import get_metadata
from toolbox.extract import copy_subset
from toolbox.extract import read_tei
from toolbox.extract import rename_files
import os
import shutil

def prepare_subcorpus(basic_wdir, master_wdir, subset_wdir,  converted_wdir = "txt/", metadata_name = "metadata", metadata_mode = "opt-obl", categorical_filters = [{"genre":["novel"]}], numerical_filters = [], categorical_sample_filters = [["author-name",3]], identifier = "idno", converting = True, convert_format = "txt", xpath = "bodytext", renaming = True, rename_columns = ["author-name","title"]):

    # Name of the tables of metadata
    full_metadata_file = metadata_name+"_"+metadata_mode+".csv"

    
    if os.path.exists(basic_wdir+subset_wdir):
        shutil.rmtree(basic_wdir+subset_wdir)
        print("We have just deleted " + basic_wdir+subset_wdir+" to start your subcorpus clean and fresh.\n")
    
    # I want a table with the metadata
    get_metadata.from_TEIP5(basic_wdir, master_wdir+"*.xml", metadata_name, metadata_mode)
    
    # I want to copy the corpus using filters and random sample
    copy_subset.copy_subset(basic_wdir, master_wdir+"*.xml", full_metadata_file, subset_wdir+master_wdir, categorical_filters, numerical_filters, categorical_sample_filters, identifier)
    
    # I want the metadata of this new subcorpus
    get_metadata.from_TEIP5(basic_wdir+subset_wdir,master_wdir+"*.xml", metadata_name, metadata_mode)
    
    if converting == True:
        # I want to modify the corpus somehow (rip tags, rip paratexts, take only some annotation)
        read_tei.from_TEIP5(basic_wdir+subset_wdir+master_wdir+"*.xml",basic_wdir+subset_wdir+converted_wdir, xpath)

    if renaming == True: 
        # Maybe I want to modify the names of the files using metadata
        rename_files.rename_files(basic_wdir+subset_wdir, converted_wdir+"*"+convert_format, full_metadata_file, rename_columns[0], rename_columns[1])

    print("Corpus done! :)")
