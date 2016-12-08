# -*- coding: utf-8 -*-
"""
This script separates the delta values from those text from the same author in order to see the next strongest signal (presumably genre)
Created on Thu Jan 14 11:06:25 2016
@author: José Calvo Tello
"""


import pandas as pd
import os
import numpy as np
from scipy.cluster.hierarchy import linkage
import scipy.cluster.hierarchy  as sch
import scipy.stats  as stats
from sklearn import metrics
from matplotlib import pyplot as plt



def calculate_central_tendency(dataframe, neutralise_categories, category1, metadata, mode, zeros, with_authors, print_ = True):
    """
    Calculates central tendencies of a table
    """
    if print_ == True:
        print("central tendency:",mode,zeros,with_authors)

    if with_authors == "with authors":
        dataframe_values = dataframe.values
        dataframe_values = np.reshape(dataframe_values,-1)

        if zeros == "without zeros":
            dataframe_values = np.trim_zeros(np.sort(dataframe_values))

        if mode == "median":
            tendency = dataframe.stack().median()
        elif mode == "mean":
            tendency = dataframe.stack().mean()
        elif mode == "trimming mean":
            tendency = (stats.trim_mean(dataframe, proportiontocut = 0.1))
            

    elif with_authors == "without authors":
        dataframe_without_category = np.empty([0, ])

        #TODO: a better way for that without roating it?
        dataframe = dataframe.rename(lambda x: x +"_"+ metadata.loc[x,category1])
        dataframe = dataframe.T         
        dataframe = dataframe.rename(lambda x: x +"_"+ metadata.loc[x,category1])
        dataframe = dataframe.T
        
        # For each author
        for neutralise_category1 in neutralise_categories:
            # For each author
            for neutralise_category2 in neutralise_categories:
                # If they are not equal
                if neutralise_category1 == neutralise_category2:
                    pass
                else:
                    # Creamos índices para sacar los dataframes de cada autor
                    category_columns = dataframe.columns.to_series().str.endswith("_"+neutralise_category1)
                    category_rows = dataframe.index.to_series().str.endswith("_"+neutralise_category2)

                    # We take the values
                    values_without_category = dataframe.loc[category_rows,category_columns].values
                    # Numbers are 
                    values_without_category = np.reshape(values_without_category,-1)
                    dataframe_without_category = np.concatenate((dataframe_without_category,values_without_category),axis=0)

            if mode == "median":
                tendency = (np.median(dataframe_without_category))
            elif mode == "mean":
                tendency = (np.mean(dataframe_without_category))
            elif mode == "trimming mean":
                tendency = (stats.trim_mean(dataframe_without_category, proportiontocut = 0.1))
                

    #print("\n\n",tendency)    
    return tendency



def add_cluster_2_metadata(clusters, metadata, name):
    """
    It adds the ids of the cluster to the metadata file
    """
    # We add to the metadata the cluster information
    metadata[name] = clusters

    # We get the numbers of clusters    
    ids_clusters = set(clusters)
    print("number of clusters: ",len(ids_clusters))

    return ids_clusters, metadata
    



def add_metada_2_index_columns(dataframe,metadata,category1,category2, step):
    """
     This function puts in the columns' names and index the category of the metadata, normally author-name
    """
    if step == 1:
        dataframe = dataframe.rename(lambda x: x +"_"+ metadata.loc[x,category1])
        dataframe = dataframe.T         
        dataframe = dataframe.rename(lambda x: x +"_"+ metadata.loc[x,category1])
        dataframe = dataframe.T
    
    elif step == "rendering":
        dataframe = dataframe.rename(lambda x: metadata.loc[x[0:6],category1]+"_"+ metadata.loc[x[0:6],category2]+"_"+x[0:6])
        dataframe = dataframe.T         
        dataframe = dataframe.rename(lambda x: metadata.loc[x[0:6],category1]+"_"+ metadata.loc[x[0:6],category2]+"_"+x[0:6])
        dataframe = dataframe.T         
        
    else:
        dataframe = dataframe.rename(lambda x: x[0:6]+"_"+ metadata.loc[x[0:6],category1]+"_"+ metadata.loc[x[0:6],category2])
        dataframe = dataframe.T         
        dataframe = dataframe.rename(lambda x: x[0:6]+"_"+ metadata.loc[x[0:6],category1]+"_"+ metadata.loc[x[0:6],category2])
        dataframe = dataframe.T         

    return dataframe
    
    
    
def create_flat_cluster(dataframe, t, delta_type):
    """
    It creates a flat cluster and a dendrogram from a dataframe
    """
    
    # We create clusters of the original delta matrix to compare the neutralised delta matrix
    cluster = linkage(dataframe, method = 'ward')

    plt.figure(figsize=(6, 12))
    plt.title('Hierarchical Clustering Dendrogram (Ward)')
    plt.xlabel('sample index')
    plt.ylabel(delta_type+' (5000 MFW)')

    dendrogram = sch.dendrogram(Z = cluster, labels = dataframe.index, orientation = 'right') #, color_threshold=1.5
    flat_cluster = sch.fcluster(cluster, t = t)
    # maxcluster
    plt.show()


    return flat_cluster



def calculate_cluster_homogeneity(categories, ids_clusters, metadata, source_clusters, folder):
    """
    Observes if a cluster is homogenous about author or subgenre (normally)
    """
    
    # We create a dataframe to compare the results of Cosine Delta and Neutralized Delta
    print("homogeneity")
    #print(metadata)

    ground_truth_category1 = list(metadata.loc[:,categories[0]])
    ground_truth_category2 = list(metadata.loc[:,categories[1]])
    
    ground_truth_2categories = []
    for i in range(len(ground_truth_category2)):
        combination = ground_truth_category1[i] + "-" + ground_truth_category2[i]
        ground_truth_2categories.append(combination)


    test_values = list(metadata.loc[:,source_clusters])
    
    homogeneity_category1 = metrics.homogeneity_score(ground_truth_category1,test_values)
    homogeneity_category2 = metrics.homogeneity_score(ground_truth_category2,test_values)
    
    return [homogeneity_category1, homogeneity_category2] 

def index_author(author,delta_matrix):
    """
    It creates index for the dataframe of the author
    """
    author_columns = delta_matrix.columns.to_series().str.endswith("_"+author)
    author_rows = delta_matrix.index.to_series().str.endswith("_"+author)

    return author_columns, author_rows




def calculate_author_delta(author,delta_matrix, mode, zeros, corpus_tendency,author_columns, author_rows):
    """
    It calculates the author difference and tendency
    """
    # We create a delta for the author
    delta_author = delta_matrix.loc[author_rows,author_columns]
    # And put in a numpy array its values
    #values_author = delta_author.values
    #print(values_author)
    
    author_tendecy = calculate_central_tendency(
        dataframe = delta_author,
        neutralise_categories = None,
        category1 = None,
        metadata = None,
        mode = mode,
        zeros = zeros,
        with_authors = "with authors",
        print_ = False)
    
    # We calculate the difference between the corpus and the author tendency
    author_difference = corpus_tendency - author_tendecy       

    #print(author, author_tendecy, author_difference)

    return author_tendecy, author_difference



def neutralise_delta(delta_matrix_neutralised, author_columns, author_rows, author_difference, corpus_tendency, modification ="difference"):
    """
    it modifies a dalta matrix based on the difference between the author central tendency and the corpus central tendecy
    """
    if modification == "difference":
        # Condicional sobre 
        delta_matrix_neutralised.loc[author_rows,author_columns] = delta_matrix_neutralised.loc[author_rows,author_columns] + author_difference
    elif modification == "total_median":
        delta_matrix_neutralised.loc[author_rows,author_columns] = corpus_tendency
    # We put to cero again the values from the same texts
    for column in delta_matrix_neutralised.columns:
        delta_matrix_neutralised.loc[column,column] = 0

    return delta_matrix_neutralised



def neutralising_authorship_delta(corpora, folder, file_matrix, file_metadata, t, category1, category2, mode = "mean", zeros = "without zeros", with_authors = "without authors", modification = "difference"):
    """
    Main function of the script. It receives the following arguments:
    * corpora: name of the corpus
    * folder: place where he finds the rest of the files
    * file_matrix: distance table outputed from Stylo
    * file_metadata: csv file with id, author-name and subgenre at least
    * category1: name of the category that we want to neutralise (normally author-name)
    * category2: name of the category that we expect to get clearer (normally subgenre)
    * mode: kind of central tendency that we want to use. Normally mean, also possible median or trimming mean
    * zeros: we specify if we want to filter the zeros from the delta matrix
    * with_authors: we specify if we want to filter the authors for the central tendecy of the corpus (normally without authors)
    * modification: specify
    * t: value of the argument for making the cluster flat. Defaulf: 1.
    
    
    Example of how to use this function:
    
    neutralised_delta = neutralising_authorship_delta(
            corpora = "Spanish American hist-non hist",
            folder = "data/hispan/",
            file_matrix = "distance_table_5000mfw_0c.txt",
            file_metadata = "metadata_opt-obl.csv",
            category1 = "author-name",
            category2 = "subgenre",
            mode = "mean",
            zeros = "without zeros",
            with_authors = "without authors",
            modification = "difference",
            t = 1,
            )
    """
    print(corpora)
    # Load the delta_matrix
    delta_matrix = pd.DataFrame.from_csv(folder+file_matrix,sep=" ")
    #print(delta_matrix)

    #Cargo los metadatos
    metadata = pd.DataFrame.from_csv(folder+"/"+file_metadata,sep=",")
    amount_texts = metadata.shape[0]
    print("cantidad de textos:", metadata.shape[0])

    # We get a list of the authors from the metadata table
    authors = list(set(metadata.loc[:,category1].values))
    #print(authors)

    # We calculate the central tendency of the copus
    corpus_tendency = calculate_central_tendency(
        dataframe = delta_matrix,
        neutralise_categories = authors,
        category1 = category1,
        metadata = metadata,
        mode = mode,
        zeros = "without zeros",
        with_authors = "without authors"
        )
    print("tendency of different authors: ",corpus_tendency)


    # We add the information to index and columns
    delta_matrix = add_metada_2_index_columns(delta_matrix, metadata, category1, category2, step=1)
    #delta_matrix = delta_matrix.sort_index(axis=1, ascending=True)
    #delta_matrix = delta_matrix.sort_index(axis=0, ascending=True)
    #delta_matrix.to_csv(path_or_buf =folder+"/"+os.path.splitext(file_matrix)[0]+"_names.csv", sep=" ", decimal='.')

    # We create a flat cluster
    flat_cluster_delta = create_flat_cluster(delta_matrix, t, delta_type="Cosine Delta")
    
    source_clusters = "clusters Delta"
    # We add the information about the clusters to the metadata
    ids_clusters, metadata = add_cluster_2_metadata(flat_cluster_delta, metadata, source_clusters)
    

    # We create a list of categories
    # TODO: pass it as list already in the definition of the function?
    categories = [category1,category2]

    # We use the function that calculates the homogeneity of the cluster
    homogeneities_cosine = calculate_cluster_homogeneity(categories = categories, ids_clusters = ids_clusters, metadata = metadata, source_clusters = source_clusters, folder = folder)
    #print(homogeneities_cosine)

    # We add the information about the corpus to the author report
    report_author = "type of tendency for corpus: " + str(mode) +"\n"+"different authors tendency: " + str(corpus_tendency) +"\n"+ "author\tauthor_tendency\tauthor_difference"
    # We calculate the central tendency of the subcorpus of each author
    
    # We make a copy of the matrix
    delta_matrix_neutralised = delta_matrix
    #print(delta_matrix_neutralised)

    # For each author
    for author in authors:
        
        # We get the index to create a submatrix
        author_columns, author_rows = index_author(author,delta_matrix)
        
        # We use the function to calculate delta, central tendency and difference of each author
        author_tendecy, author_difference = calculate_author_delta(author, delta_matrix, mode, zeros, corpus_tendency, author_columns, author_rows)

        # We add it to the report        
        report_author = report_author + "\n"+author+"\t"+str(author_tendecy)+"\t"+str(author_difference)

        # We use the function to neutralise 
        delta_matrix_neutralised = neutralise_delta(delta_matrix_neutralised, author_columns, author_rows, author_difference, corpus_tendency, modification ="difference")        
    #print(delta_matrix_neutralised)
    # We print the report about authors:
    with open (os.path.join(folder, "delta_about_authors.csv"), "w", encoding="utf-8") as fout:
        fout.write(report_author)
    
    # We put the information about the second category (normally the subgenre) in the columns names and index
    delta_matrix_neutralised = add_metada_2_index_columns(delta_matrix_neutralised, metadata, category2, category1, step=2)

    delta_matrix_neutralised_printing = add_metada_2_index_columns(delta_matrix_neutralised, metadata, category1, category2, step="rendering")
    delta_matrix_neutralised_printing = delta_matrix_neutralised_printing.sort_index(axis=1, ascending=True)
    delta_matrix_neutralised_printing = delta_matrix_neutralised_printing.sort_index(axis=0, ascending=True)

    # We save the netrualized Delta Matrix as file
    delta_matrix_neutralised_printing.to_csv(path_or_buf =folder+"/"+os.path.splitext(file_matrix)[0]+"_netrualized.csv", sep=" ", decimal='.')
    #print(delta_matrix_neutralised)
    
    # We make a flat cluster
    flat_cluster_neutralised = create_flat_cluster(delta_matrix_neutralised, t, delta_type="Neutralized Delta based on Cosine Delta")

    # We add the info about the cluster to the metadata
    neutralised_ids_clusters, metadata = add_cluster_2_metadata(flat_cluster_neutralised, metadata, "neutralised clusters")
    #print(metadata)

    homogeneities_neutralised = calculate_cluster_homogeneity(categories = categories, ids_clusters = neutralised_ids_clusters, metadata = metadata, source_clusters = "neutralised clusters", folder = folder)

    # We create a table to summarize it
    homogeneity_total = pd.DataFrame(homogeneities_cosine, index=["author","subgenre"],columns=["Cosine"])
    homogeneity_total["Neutralized"] = homogeneities_neutralised

    #print(homogeneity_total)
    homogeneity_total.to_csv(folder+"evaluation-homogeneity.csv", sep='\t', encoding='utf-8')
    
    homogeneity_total.Cosine = homogeneity_total.Cosine.round(2)
    homogeneity_total.Neutralized = homogeneity_total.Neutralized.round(2)

    fig = homogeneity_total.plot(kind="bar", colormap= "summer",
                         figsize= ([7,6]), title = "Homogeneity of "+corpora+" (texts: "+str(amount_texts)+")", table=True,
                        use_index=False, ylim =[0,1]).get_figure()
    fig.axes[0].get_xaxis().set_visible(False)
    fig.savefig(folder+"homogeneity_"+corpora+".png")
    
    homogeneity_total["diference"] = homogeneity_total["Neutralized"] - homogeneity_total["Cosine"]
    print("\n\n\n",homogeneity_total)



def analyse_multiple_corpora(basic_folder, subfolders):
    """
    This function calls the neutralising_category_delta with the same parameters for different corpora.
    Example of how to use it:

    analyse_multiple_corpora("", ["historical-bildungsroman","historical-erotic","historical-adventure","erotic-adventure","bildungsroman-erotic","bildungsroman-adventure"])


    """
    for subfolder in subfolders:

        neutralised_delta = neutralising_authorship_delta(
            corpora = subfolder,
            folder = basic_folder+"data/"+subfolder+"/",
            file_matrix = "distance_table_5000mfw_0c.txt",
            file_metadata = "metadata_opt-obl.csv",
            category1 = "author-name",
            category2 = "subgenre",
            mode = "mean",
            zeros = "without zeros",
            with_authors = "without authors",
            modification = "difference",
            t = 1,
            )
        
    return neutralised_delta

