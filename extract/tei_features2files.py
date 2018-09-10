# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 11:03:11 2018

@author: jose
"""


def teia_features2files(inputwdir, xpath_filter, xpath_informations, outdir, token_separator = " ", feature_separator = "_", format_= "txt"):
    """
    inputwdir = "/home/jose/cligs/ne/linguistic_annotated/" # "/home/jose/Dropbox/Doktorarbeit/thesis/data/annotated/"
    xpath_filter = "[.]" #"[@cligs:ctag='NC']" 
    xpath_informations = ["@cligs:form","@cligs:ctag","@lemma"] # ["@lemma"] ["@lemma", "@cligs:ctag"]
    outdir = "/home/jose/cligs/ne/"
    token_separator = "\n"
    feature_separator = "\t"
    format_ = "csv"
    
    teia_features2files(inputwdir, xpath_filter, xpath_informations, outdir, token_separator = token_separator,feature_separator=feature_separator, format_ = format_)

    """
    outdirs = xpath_filter + " ".join(xpath_informations)
    outdirs = re.sub(r"[\[\]\.@='':]+", r"_", outdirs)
    outdirs = re.sub(r"cligs", r"", outdirs)
    
    if not os.path.exists(os.path.join(outdir,outdirs)):
        os.makedirs(os.path.join(outdir,outdirs))
    # For every xml file in the folder
    total_length = len(glob.glob(inputwdir+"*.xml"))
    i = 1
    for doc in glob.glob(inputwdir+"*.xml"):
        file_name = os.path.splitext(os.path.split(doc)[1])[0]
        print(i,"th file. Done ", str(i/total_length)[0:3],"%")
    
        # The XML file is parsed as root element
        root_document = etree.parse(doc).getroot()
        
        # Namespaces are defined
        specific_namespaces = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude', 'cligs': 'https://cligs.hypotheses.org/ns/cligs'}

        linguistic_features_lists = []
        for xpath_information in  xpath_informations:
            #print("//tei:w"+xpath_filter+"/"+xpath_information)
            # The xpath is used
            linguistic_features_lists.append(root_document.xpath("//tei:w" + xpath_filter + "/" + xpath_information, namespaces=specific_namespaces))
            
            
        if len(linguistic_features_lists) == 1:
            linguistic_features = linguistic_features_lists[0]

        elif len(linguistic_features_lists[0]) == len(linguistic_features_lists[1]):
            
            if len(linguistic_features_lists) == 2:
                linguistic_features = [feature_separator.join([tuple_[0].lower(),tuple_[1].lower()]) for tuple_ in list(zip(linguistic_features_lists[0],linguistic_features_lists[1]))]
            elif len(linguistic_features_lists) == 3:
                linguistic_features = [feature_separator.join([tuple_[0].lower(),tuple_[1].lower(), tuple_[2].lower()]) for tuple_ in list(zip(linguistic_features_lists[0], linguistic_features_lists[1], linguistic_features_lists[2]))]
        
        else:
            raise ValueError('Not all the elements (' +xpath_filter + ') contain all the features ('+xpath_informations+').')
       
        i += 1
        with open (os.path.join(outdir, outdirs, file_name+ "." + format_), "w", encoding="utf-8") as fout:
            fout.write(token_separator.join(linguistic_features))
"""
inputwdir = "/home/jose/cligs/ne/linguistic_annotated/" # "/home/jose/Dropbox/Doktorarbeit/thesis/data/annotated/"
xpath_filter = "[.]" #"[@cligs:ctag='NC']" 
xpath_informations = ["@cligs:form","@cligs:ctag","@lemma"] # ["@lemma"] ["@lemma", "@cligs:ctag"]
outdir = "/home/jose/cligs/ne/"
token_separator = "\n"
feature_separator = "\t"
format_ = "csv"

tei2text.teia_features2files(inputwdir, xpath_filter, xpath_informations, outdir, token_separator = token_separator,feature_separator=feature_separator, format_ = format_)
"""
