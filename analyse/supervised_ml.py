# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:27:31 2017

@author: jose
"""

from toolbox.extract import corpus2table
import pandas as pd
from sklearn.model_selection import train_test_split



def load_data(wdir, mode, max_MFF, wsdir="", freq_table="freq_table.csv", metadata_table="metadata_opt-obl.csv", corpus_table=False, names_MFF=[]):
    """
    It loads the texts and the metadata
    """
    wsdir = mode+"-set/"
    if corpus_table == True:
        print("\nloading", wsdir," from table")        
        data = pd.read_csv(wdir+wsdir+freq_table, encoding="utf-8", sep="\t", index_col=0)
    else:
        print("\nloading", wsdir," from files")        
        data = corpus2table.main(wdir+wsdir, mode = mode, corpus_dir = "corpus/", names_MFF = names_MFF)
    
    # Important!
    data = data.sort_index()
    labels = pd.read_csv(wdir+wsdir+metadata_table, encoding="utf-8", sep=",", index_col=0)
    
    print(mode, data.shape, labels.shape)
    # TODO: Confirmation if everything is ok
    return data, labels


def main(wdir, labels, corpus_table=False, spliting=False, max_MFF=5000, methods=["KNN"], n_neighbors=5):
    """
    Main function of this script. It evaluates different labels and different methods for a a train-set and eval-set.
    
    Parameters:
    *  wdir: (string) working directory. This directory should contain two subfolders: train-set and eval-set. Each of this subfolders should contain the metadata and another subfolder called corpus with the texts (in theory with the ids as file names and in txt)
    *  labels: (list) list of the names of the columns of the metadata that you want to evaluate. If you want to use regression models, the columns should contain only numbers (like the year of publication)
    *  corpus_table: (boolean) if you already have the sets in a table called freq_table.csv in the subfolders train-set and eval-set. Default = False
    *  spliting: (boolean) if you don't have a train-set and eval-set but only a train-set that you want to split authomatically. This function is currently not workind. Default= False
    *  max_MFF: (int) amount of maximum Most Frequent Features. Defaul=5000
    *  methods: (list) names of the methods that should be implemented. Regression methods: ["KNR","LR","RR"]; classification methods: ["KNN", "GNB", "BNB", "MNB", "SVC", "DT", "RF","LSVC", "LG"]. Default=["KNN"]
    *  n_neighbors: (int) number of neighbors that knn should use. Default=5

    Simple example for subgenre and authorship loading the texts from the txt files:
from toolbox.analyse import supervised_ml
supervised_ml.main(
 wdir = "/home/jose/cligs/experiments/20170508 starting_ml/",
 labels=["subgenre","author-name"],
 methods = ["KNN"]
 )
     
    Example of how to use it for classification:
from toolbox.analyse import supervised_ml
supervised_ml.main(
 wdir = "/home/jose/cligs/experiments/20170508 starting_ml/",
 labels=["subgenre","author-name", "decade","author-gender","availability", "subgenre",	"genre-label",	"narrative-perspective",	"narrator",	"protagonist-gender",	"setting",	"subsubgenre",	"form",	"decade"],
 corpus_table = True,
 max_MFF=5000,
 n_neighbors=3,
 methods = ["KNN", "GNB", "BNB", "MNB", "SVC", "DT", "RF","LSVC", "LG"]
 )

    Example of how to use it for regression:
from toolbox.analyse import supervised_ml
supervised_ml.main(
 wdir = "/home/jose/cligs/experiments/20170508 starting_ml/",
 labels=["year"],
 corpus_table = True,
 max_MFF=5000,
 methods = ["KNR","LR","RR"]
 )

     """
    if spliting == False:
        print(corpus_table)
        # Load train data
        data_train, labels_train = load_data(wdir=wdir, max_MFF=max_MFF, mode="train", corpus_table=corpus_table)
        print(data_train.columns[-1])
        
        # Load eval data
        data_eval, labels_eval = load_data(wdir=wdir, max_MFF=max_MFF, mode="eval", corpus_table=corpus_table, names_MFF=data_train.columns)
        print(data_eval.columns[-1])
        
    else:
        # This part is not working
        data_train, data_eval, labels_train, labels_eval = train_test_split(X_labeled, y_labeled, random_state=2)

    for method in methods:
        print("\n", method)
        results = {}
           
        for label in labels:
            # TODO: Confirmation if everything is ok
            label_train = labels_train[label]
            label_eval = labels_eval[label]

            if method == "KNN":
                from sklearn.neighbors import KNeighborsClassifier
                # Application to the test-set
                model = KNeighborsClassifier(n_neighbors=n_neighbors, p=2)
            elif method== "GNB":
                from sklearn.naive_bayes import GaussianNB
                model = GaussianNB()
            elif method== "BNB":
                from sklearn.naive_bayes import BernoulliNB
                model = BernoulliNB()
            elif method== "MNB":
                from sklearn.naive_bayes import MultinomialNB
                model = MultinomialNB()
            elif method== "SVC":
                from sklearn.svm import SVC
                model = SVC(kernel="linear",C=1E10)
            elif method=="DT":
                from sklearn.tree import DecisionTreeClassifier
                model = DecisionTreeClassifier()
            elif method=="RF":
                from sklearn.ensemble import BaggingClassifier
                from sklearn.tree import DecisionTreeClassifier
                tree = DecisionTreeClassifier()
                model = BaggingClassifier(tree)
            elif method== "LSVC":
                from sklearn.svm import LinearSVC
                model = LinearSVC()
            elif method== "LG":
                from sklearn.linear_model import LogisticRegression
                model = LogisticRegression()
                
                
            elif method=="KNR":
                from sklearn.neighbors import KNeighborsRegressor
                model = KNeighborsRegressor(n_neighbors=n_neighbors)
            elif method=="LR":
                from sklearn import linear_model
                model = linear_model.LinearRegression()
            elif method=="RR":
                from sklearn import linear_model
                linear_model.Ridge (alpha = .5)
                
                
            model.fit(data_train, label_train)
            results[label]=model.score(data_eval, label_eval)
            # Visualisation of the results
        print(results)
        print("method's mean for labels: ", sum(list(results.values()))/len(results))

