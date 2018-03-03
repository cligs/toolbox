#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: query_w2v.py
# Author: #cf
# Version 0.2.0 (2017-07-31)


"""
Function to query word2vec models built with gensim.
"""


# =================
# Import statements
# =================

from os.path import join
import re
import glob
import gensim
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

#print("nx", nx.__version__)
#print("gensim", gensim.__version__)
#print("matplotlib", matplotlib.__version__)


# =================
# Parameters
# =================

#wdir = "/media/christof/data/Dropbox/0-Analysen/2017/w2v/"
wdir = "/home/christof/Dropbox/0-Analysen/2017/w2v/"
##modelfile = "models/frwiki17_skgr-400dm-hsoftm-5wn-200mc.gensim"
##modelfile = "models/frwiki17_mdt=skgr-opt=negsam-dim=300-win=6-min=100.gensim"
modelfile = join(wdir, "models", "frwiki17_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=100.gensim")
#modelfile = join(wdir, "models", "roman20_mdt=skgr-opt=negsam-itr=10-dim=300-win=6-min=50.gensim")



mode = ["Calc"]
#mode = ["Similar"]
#mode = ["SeveralSim"]
#mode = ["TopN"]
#mode = ["NWords"]
#mode = ["OddOne"]
#mode = ["Pair"]
#mode = ["Count"]

# =================
# Queries
# =================

# Pair: Calculate (cosine) similarity score (input: two terms)
#PairQuery = ["machine", "outil"]
#PairQuery = ["femme", "fille"]
#PairQuery = ["père", "fils"]
#PairQuery = ["fille", "fils"]
#PairQuery = ["père", "mère"]
#PairQuery = ["père", "papa"]
#PairQuery = ["mère", "maman"]
#PairQuery = ["café", "cigarette"]
#PairQuery = ["cigare", "cigarette"]
#PairQuery = ["pipe", "cigare"]
#PairQuery = ["rue", "avenue"]
#PairQuery = ["rue", "chemin"]
#PairQuery = ["papa", "gamin"]
#PairQuery = ["père", "fils"]
#PairQuery = ["papa", "fils"]
#PairQuery = ["père", "gamin"]
PairQuery = ["prose_nom", "littérature_nom"]
#PairQuery = ["poésie_nom", "littérature_nom"]

# NWords: Calculate similarity between lists of words
NWordsQuery = [["police", "voiture"],["automobile", "flic"]]

# Calc: Calculate the most similar term.
# Input: [[positive terms], [negative terms]]
#CalcQuery = [["femme_nom", "amant_nom"], ["homme_nom"]]
#CalcQuery = [["oncle_nom", "femme_nom"], ["homme_nom"], ["_nom"]] #OK
#CalcQuery = [["roi_nom", "femme_nom"], ["homme_nom"], ["_nom"]] #OK
#CalcQuery = [["oncle_nom", "femme_nom"], ["homme_nom"]]
#CalcQuery = ["ville", "époux", "homme"]
#CalcQuery = [["amant", "femme"], ["homme"], ["_nam"]]
#CalcQuery = ["livre", "histoire", "fiction"], ["théâtre"]
#CalcQuery = ["livre"], ["histoire"]
#CalcQuery = [["paris_nam", "allemagne_nam"], ["france_nam"], ["_nam"]] #OK
#CalcQuery = [["histoire", "fiction"], ["réalité"]]
#CalcQuery = ["orange"], ["choppers"]
#CalcQuery = [["eau_nom"], ["rhum_nom"], ["_nom"]]
#CalcQuery = ["calme_adj"], ["puis_adv"]
#CalcQuery = [["balle_nom"], ["jeu_nom"], ["_nom"], 10]
#CalcQuery = ["balle_nom"], ["puis_adv"], ["_nom", "_adj", "_ver"]
#CalcQuery = ["richesse_nom", "vertu_nom"], ["apprentissage_nom"], "_nom"
#CalcQuery = ["eau_nom"], ["rivière_nom"], "_nom"
#CalcQuery = ["roi_nom", "homme_nom"], ["homme_nom"], "_nom"
#CalcQuery = ["assurance_nom"], ["musique_nom"], "_nom"
#CalcQuery = ["roi_nom", "homme_nom"], ["femme_nom"], "_nom"
#CalcQuery = [["sens_nom"], ["signification_nom"], ["_nom"]]
#CalcQuery = [["sens_nom"], ["musique_nom"], ["_nom"]]
#CalcQuery = [["clarté_nom"], ["luminosité_nom"], ["_nom"]]
#CalcQuery = [["clarté_nom"], ["concision_nom"], ["_nom"]]
#CalcQuery = [["suite_nom"], ["chambre_nom"], ["_nom"]]
#CalcQuery = [["pièce_nom"], ["chambre_nom"], ["_nom"]]
#CalcQuery = [["morceau_nom"], ["chanson_nom"], ["_nom"]]
#CalcQuery = [["roi_nom", "femme_nom"], ["homme_nom"], ["_nom"]]
#CalcQuery = [["bélier_nom", "femelle_nom"], ["mâle_nom"], ["_nom"]]
CalcQuery = [["pommier_nom", "cerise_nom"], ["pomme_nom"], ["_nom"]]


# OddOne: Find the term that does not belong in the list
#OddOneQuery = ["argent", "billet", "monnaie", "musée"]
#OddOneQuery = ["femme", "oncle", "fille", "soeur"]
OddOneQuery = ["roman", "poème", "drame", "essai"]
#OddOneQuery = ["baudelaire", "flaubert", "zola", "maupassant"]
#OddOneQuery = ["baudelaire", "flaubert", "verlaine", "mallarmé"]
#OddOneQuery = ["baudelaire", "flaubert", "verlaine", "mallarmé"]

# Similar: find similar words
# Query: word, pos-filter, number of results
#SimilarQuery = ["bière_nom", 20]
#SimilarQuery = ["poésie", 8]
#SimilarQuery = ["roman", 8]
#SimilarQuery = ["policier", 5]
#SimilarQuery = ["orange", 5]
#SimilarQuery = ["bleu", 5]
#SimilarQuery = ["blues", 10]
#SimilarQuery = ["jazz_nam", 10]
#SimilarQuery = ["mozart", 10]
#SimilarQuery = ["voltaire_nam", 10]
#SimilarQuery = ["mallarmé", 10]
#SimilarQuery = ["fleur", 10]
#SimilarQuery = ["vérité_nom", 20]
#SimilarQuery = ["mensonge_nom", 20]
#SimilarQuery = ["orange_nam", 20]
#SimilarQuery = ["orange_adj", 20]
#SimilarQuery = ["baudelaire_nam", 20]
#SimilarQuery = ["eau", 20]
#SimilarQuery = ["corps_nom", 50]
#SimilarQuery = ["learning_nom", 50]
#SimilarQuery = ["poésie_nom", 10]
#SimilarQuery = ["assurance_nom", 10]
#SimilarQuery = ["mouvement_nom", "_nom", 10]
#SimilarQuery = ["génie_nom", ["_nom", "_adj"], 20]
#SimilarQuery = ["conduite_nom", ["_nom"], 20]
#SimilarQuery = ["sens_nom", ["_nom"], 20]
#SimilarQuery = ["clarté_nom", ["_nom"], 20]
#SimilarQuery = ["pièce_nom", ["_nom"], 20]
SimilarQuery = ["morceau_nom", ["_nom"], 20]


#SeveralSimQuery = [["huitres", "poulet", "soupe", "pain", "omelette", "sauce", "oignon", "lard", "potage", "ragoût", "beignet", "vermicelle", "tomate", "aubergine", "courgette"], ["grillé", "braiser", "farcir", "griller"], 5000]
#SeveralSimQuery = [["surprise_nom", "peur_nom", "angoisse_nom", "joie_nom", "bonheur_nom", "malheur_nom", "ennui_nom", "désespoir_nom","tristesse_nom","amour_nom","honte_nom","tendresse_nom","tourment_nom","désarroi_nom","chagrin_nom", "remords_nom", "jalousie_nom", "étonnement_nom", "effroi_nom", "plaisir_nom", "timidité_nom", "amertume_nom", "indifférence_nom", "envie_nom", "fureur_nom", "nostalgie_nom",], ["soif_nom", "éternel_adj"], 2000]
#SeveralSimQuery = [["vérité","destinée","haine","science","sagesse","vie","mémoire","peuple", "saints", "mort", "temps", "courage", "monde"], ["prince", "colonel", "mer", "table", "forêt", "bateau", "prince", "cas", "oiseaux"], 200]
#SeveralSimQuery = [["vérité","destinée","haine","science","sagesse","vie","mémoire","peuple", "saints", "mort", "temps", "courage", "monde"], ["prince", "colonel", "mer", "table", "forêt", "bateau", "prince", "cas", "oiseaux"], 200]
#SeveralSimQuery = [["roman_nom","théâtre_nom","poésie_nom","drame_nom","poème_nom","histoire_nom","fiction_nom","biographie_nom", "lettre_nom", "édition_nom", "livre_nom", "papier_nom", "récit_nom", "préface_nom", "écrit_nom", "prose_nom", "anthologie_nom", "ouvrage_nom", "littérature_nom", "publication_nom", "élégie_nom", "recueil_nom", "poétique_nom", "aphorisme_nom", "pamphlet_nom", "romanesque_nom", "auteur_nom", "poète_nom", "fable_nom", "sonnet_nom", "satire_nom", "mémoires_nom", "folio_nom"], ["musique_nom", "danse_nom", "peinture_nom"], 2000]
SeveralSimQuery = [["apprentissage_nom", "vertu_nom"], ["thé_nom"], 5]

CountQuery = ["balzac_nam", "vian_nam", "verne_nam", "bergson_nam", "beauclair_nam"]
#CountQuery = ["vérité_nom", "courage_nom", "prince_nom"]

topn = 5000

# =================
# Functions
# =================


def get_topn(Model, topn):
    """
    Return the n most frequent tokens in the model.
    """
    print("get_topn")
    counter = 0
    tokens = []
    counts = []
    for token,vocab_obj in Model.wv.vocab.items():
        count = vocab_obj.count
        if "_adj" in token or "_nom" in token or "_ver" in token and count > 1000:
            counter += 1
            #print("==>", token, count)
            tokens.append(token)
            counts.append(count)
        #else:
            #print("rejected", token, count)
        #if counter == 1000:
        #    break
    topn_counts = pd.DataFrame({"token": tokens, "count": counts})
    topn_counts.sort_values(by="count", ascending=False, inplace=True)
    with open("topn-counts.csv", "w") as outfile:
        topn_counts.to_csv(outfile, sep=";")
    return topn_counts




def get_count(Model, CountQuery):
    """
    For any word, returns the word count in the model.
    """
    print("get_count")
    for Word in CountQuery:
        Result = Model.wv.vocab[Word].count
        print(Word, "count:", Result)


def wordpair_similarity(Model, PairQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Result = Model.similarity(PairQuery[0], PairQuery[1])
    print("Query:", PairQuery)
    print("Result:", Result)



def nword_similarity(Model, NWordsQuery):
    """
    Returns the similarity score, between 0 and 1, for two words based on the model.
    """
    print("--word_similarity")
    Result = Model.n_similarity(NWordsQuery[0], NWordsQuery[1])
    print("Query:", NWordsQuery)
    print("Result:", Result)


def calc_similar(Model, CalcQuery):
    """
    Returns the most similar term for a set of positive and negative terms.
    """
    print("--calc_similar")
    Result = Model.most_similar(positive=[Word for Word in CalcQuery[0]],
                                negative=[Word for Word in CalcQuery[1]],
                                topn=20)
    print("Query:", CalcQuery)
    table = []
    for word,value in Result:
        if word[-4:] in CalcQuery[2]:
            table.append([word, value])
    print("\n", tabulate(table))


def several_similarity(Model, SeveralSimQuery):
    """
    Returns the terms most similar to a group of words.
    """
    print("several_similarity")
    Result = Model.wv.most_similar_cosmul(positive=SeveralSimQuery[0], negative=SeveralSimQuery[1], topn=SeveralSimQuery[2])
    print("Query:", SeveralSimQuery)
    for item in SeveralSimQuery[0]:
        print(item)
    for Item in Result:
        print(Item[0])
    #print("Result:", Result)
    wordlist = ""
    for item in SeveralSimQuery[0]:
        wordlist = wordlist + item + "\n"
    for item in Result:
        #print(item[0], "\t", item[1])
        wordlist = wordlist + item[0] + "\n"
    with open("wordlist.txt", "w") as outfile:
        outfile.write(wordlist)




def find_oddone(Model, DoesntMatch):
    """
    Returns the term that does not belong to the list.
    """
    print("--doesnt_match")
    Result = Model.doesnt_match([Word for Word in DoesntMatch])
    print("Query:", DoesntMatch)
    print("Result:", Result)



def similar_words(Model, SimilarQuery):
    """
    Returns the n words which are most similar in the data.
    """
    print("--similar_words")
    Result = Model.similar_by_word(SimilarQuery[0], SimilarQuery[2])
    print("\nQuery:", SimilarQuery)
    wordlist = SimilarQuery[0]+"\n"
    table = []
    for word,value in Result:
        if word[-4:] in SimilarQuery[1]:
            wordlist = wordlist + word + "\t" + str(value) + "\n"
            table.append([word, value])
    print(tabulate(table))
    with open("wordlist.txt", "w") as outfile:
        outfile.write(wordlist)
    return Result



def similar_to_networkx(SimilarQuery, Result):
    """
    Transform output from similar_words into a structure for networkx.
    """
    TargetWord = SimilarQuery[0]
    AllLinks = []
    for Item in Result:
        Word = Item[0]
        Weight = Item[1]
        #print(Word, Weight)
        Link = [TargetWord, Word, Weight]
        AllLinks.append(Link)
    return AllLinks


def make_graph(AllLinks):
    """
    Create word graph using networkx.
    """
    MyGraph = nx.Graph(name="word-graph")
    for Link in AllLinks:
        Node1 = Link[0]
        Node2 = Link[1]
        Weight = Link[2]*100
        print(Node1, Node2, Weight)
        MyGraph.add_node(Node1, label=Node1)
        MyGraph.add_edge(Node1, Node2, weight=Weight)
    nx.write_gexf(MyGraph,"mygraph_contemps.gexf")
    return MyGraph


def visualize_graph(MyGraph, SimilarQuery):
    Positions = nx.spring_layout(MyGraph, k=3, scale=5)
    #Positions = nx.circular_layout(MyGraph, center=[0,0])
    EdgesAndWeights=dict([((u,v,),int(d["weight"])) for u,v,d in MyGraph.edges(data=True)])
    JustWeights = [(d.get("weight")/15) for u,v,d in MyGraph.edges(data=True)]

    nx.draw_networkx_nodes(MyGraph, Positions, node_size=400, node_color="c", label="label")
    nx.draw_networkx_nodes(MyGraph, Positions, nodelist=[SimilarQuery[0]], node_size=1200, node_color="y", label="label")
    nx.draw_networkx_labels(MyGraph, Positions)
    nx.draw_networkx_edge_labels(MyGraph, Positions, edge_labels=EdgesAndWeights, font_size=10)
    nx.draw_networkx_edges(MyGraph, Positions, width=JustWeights)

    plt.axis('off')
    plt.savefig("word-network.png", dpi=300)



# =================
# Main function
# =================

def main(mode, modelfile,
         PairQuery, NWordsQuery, OddOneQuery, CalcQuery, SimilarQuery, SeveralSimQuery):
    print("Launched.")
    Model = gensim.models.Word2Vec.load(modelfile)
    print("Model used:", modelfile)
    if "TopN" in mode:
        Result = get_topn(Model, topn)
    if "Count" in mode:
        Result = get_count(Model, CountQuery)
    if "SeveralSim" in mode:
        several_similarity(Model, SeveralSimQuery)
    if "Pair" in mode:
        wordpair_similarity(Model, PairQuery)
    if "NWords" in mode:
        nword_similarity(Model, NWordsQuery)
    if "Calc" in mode:
        calc_similar(Model, CalcQuery)
    if "OddOne" in mode:
        find_oddone(Model, OddOneQuery)
    if "Similar" in mode:
        Result = similar_words(Model, SimilarQuery)
    #    AllLinks = similar_to_networkx(SimilarQuery, Result)
    #    MyGraph = make_graph(AllLinks)
    #    visualize_graph(MyGraph, SimilarQuery)

main(mode, modelfile,
     PairQuery, NWordsQuery, OddOneQuery, CalcQuery, SimilarQuery, SeveralSimQuery)
