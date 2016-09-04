#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dramavis by frank fischer (@umblaetterer) & christopher kittel (@chris_kittel)

__author__ = "Christopher Kittel <web at christopherkittel.eu>, Frank Fischer <frank.fischer at sub.uni-goettingen.de>"
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "0.2"
__maintainer__ = "Frank Fischer <frank.fischer at sub.uni-goettingen.de>"
__status__ = "Development" # 'Development', 'Production' or 'Prototype'



from lxml import etree
import os
import glob
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
from itertools import chain
import math
#import argparse


ZFDir = "/media/christof/data/Dropbox/0-Analysen/2016/dramenanalyse/dlina/zf_test/"
DataDir = "/media/christof/data/Dropbox/0-Analysen/2016/dramenanalyse/dlina/data/"
GraphDir = "/media/christof/data/Dropbox/0-Analysen/2016/dramenanalyse/dlina/viz/"
action = "dramavis"
debug = False
random = False
 

def parse_drama(tree, filename):
    """
    Parses a single drama,
    runs extractors for metadata, personae, speakers and scenes,
    adds filename and scene count to metadata.
    returns dictionary:
    {ID:
        {
        "metadata":metadata,
        "personae":personae,
        "speakers":speakers
        }
    }
    """
    root = tree.getroot()
    ID = root.attrib.get("id")
    header = root.find("{*}header")
    persons = root.find("{*}personae")
    text = root.find("{*}text")
    metadata = extract_metadata(header)
    metadata["filename"] = filename
    personae = extract_personae(persons)
    speakers, scene_count = extract_speakers(text)
    metadata["scenecount"] = scene_count
    parsed_drama = (ID, {"metadata": metadata, "personae":personae, "speakers":speakers})
    return parsed_drama

def extract_metadata(header):
    """
    Extracts metadata from the header-tag of a lina-xml,
    returns dictionary:

    metadata = {
        "title":title,
        "subtitle":subtitle,
        "genretitle":genretitle,
        "author":author,
        "pnd":pnd,
        "date_print":date_print,
        "date_written":date_written,
        "date_premiere":date_premiere,
        "date_definite":date_definite,
        "source_textgrid":source_textgrid
    }
    """
    title = header.find("{*}title").text
    try:
        subtitle = header.find("{*}subtitle").text
    except AttributeError:
        subtitle = ""
    try:
        genretitle = header.find("{*}genretitle").text
    except AttributeError:
        genretitle = ""
    author = header.find("{*}author").text
    pnd = header.find("{*}title").text
    try:
        date_print = int(header.find("{*}date[@type='print']").attrib.get("when"))
    except:
        date_print = None
    try:
        date_written = int(header.find("{*}date[@type='written']").attrib.get("when"))
    except:
        date_written = None
    try:
        date_premiere = int(header.find("{*}date[@type='premiere']").attrib.get("when"))
    except:
        date_premiere = None

    if date_print and date_premiere:
        date_definite = min(date_print, date_premiere)
    elif date_premiere:
        date_definite = date_premiere
    else:
        date_definite = date_print

    ## date is a string hotfix
    if type(date_print) != int:
        date_print = 9999
    if type(date_written) != int:
        date_print = 9999
    if type(date_premiere) != int:
        date_print = 9999

    if date_written and date_definite:
        if date_definite - date_written > 10:
            date_definite = date_written
    elif date_written and not date_definite:
        date_definite = date_written

    source_textgrid = header.find("{*}source").text
    
    metadata = {
        "title":title,
        "subtitle":subtitle,
        "genretitle":genretitle,
        "author":author,
        "pnd":pnd,
        "date_print":date_print,
        "date_written":date_written,
        "date_premiere":date_premiere,
        "date_definite":date_definite,
        "source_textgrid":source_textgrid
    }
    return metadata

def extract_personae(persons):
    """
    Extracts persons and aliases from the personae-tag of a lina-xml,
    returns list of dictionaries:
    personae = [
        {"charactername":["list", "of", "aliases"]},
        {"charactername2":["list", "of", "aliases"]}
    ]
    """
    personae = []
    for char in persons.getchildren():
        name = char.find("{*}name").text
        aliases = [alias.attrib.get('{http://www.w3.org/XML/1998/namespace}id') for alias in char.findall("{*}alias")]
        if debug:
            print(aliases)
        if name:
            personae.append({name:aliases})
        else:
            personae.append({aliases[0]:aliases})
    if debug:
        print(personae)
    return personae

def extract_speakers(text):
    """
    Extracts speakers that appear in the same scene,
    returns a dict of dict of lists, and the overall scene count:
    acts =
    {"act1":
        {"scene1":["speaker1", "speaker2"],
        "scene2":["speaker2", "speaker3"]},
     "act2":
        {"scene1":["speaker3", "speaker2"],
        "scene2":["speaker2", "speaker1"]}
        }
    }
    scene_count = 4

    """
    acts = {}
    scene_count = 0
    for act in text.getchildren():
        try:
            actname = act.find("{*}head").text
        except:
            actname = str(scene_count)
        if not actname:
            actname = str(scene_count)
            scene_count += 1
        acts[actname] = {}

        for scene in act.getchildren():
            try:
                scenename = scene.find("{*}head").text
            except:
                scenename = str(scene_count)
            if not scenename:
                scenename = str(scene_count)
            speakers = [speaker.attrib.get("who").replace("#","").split() for speaker in scene.findall(".//{*}sp")]
            speakers = list(chain.from_iterable(speakers))
            if speakers:
                acts[actname][scenename] = speakers
            scene_count += 1
    return acts, scene_count

def read_dramas(datadir):
    """
    Reads all XMLs in the inputfolder,
    returns a list of lxml.etree-objects created with lxml.etree.parse("dramafile.xml").
    """
    dramafiles = glob.glob(os.path.join(datadir, '*.xml'))
    dramas = {}
    for drama in dramafiles:
        tree = etree.parse(drama)
        filename = os.path.splitext(os.path.basename((drama)))[0]
        ID, ps = parse_drama(tree, filename)
        dramas[ID] = ps
    return dramas

def create_charmap(personae):
    """
    Maps aliases back to the definite personname,
    returns a dictionary:
    charmap =
    {"alias1_1":"PERSON1",
     "alias1_2":"PERSON1",
     "alias2_1":"PERSON2",
     "alias2_2":"PERSON2"
    }
    """
    charmap = {}
    for person in personae:
        for charname, aliases in person.items():
            for alias in aliases:
                charmap[alias] = charname
    return charmap

def create_graph(speakerset, personae):
    """
    First creates a bipartite graph with scenes on the one hand,
    and speakers in one scene on the other.
    The graph is then projected into a unipartite graph of speakers,
    which are linked if they appear in one scene together.

    Returns a networkx weighted projected graph.
    """
    charmap = create_charmap(personae)
    if debug:
        print(charmap)

    B = nx.Graph()
    labels = {}
    for act, scenes in speakerset.items():
        for scene, speakers in scenes.items():
            try:
                source = " ".join([act, scene])
            except TypeError:
                source = " ".join([scene, scene])
            targets = speakers

            if not source in B.nodes():
                B.add_node(source, bipartite=0)
                labels[source] = source

            for target in targets:
                target = charmap.get(target)
                if not target in B.nodes():
                    B.add_node(target, bipartite=1)
                B.add_edge(source, target)

    scene_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
    person_nodes = set(B) - scene_nodes
    nx.is_bipartite(B)
    G = nx.bipartite.weighted_projected_graph(B, person_nodes)

    return G

def analyze_graph(G):
    """
    Computes various network metrics for a graph G,
    returns a dictionary:
    values =
    {
        "charcount" = len(G.nodes()),
        "edgecount" = len(G.edges()),
        "maxdegree" = max(G.degree().values()) or "NaN" if ValueError: max() arg is an empty sequence,
        "avgdegree" = sum(G.degree().values())/len(G.nodes()) or "NaN" if ZeroDivisionError: division by zero,
        "density" = nx.density(G) or "NaN",
        "avgpathlength" = nx.average_shortest_path_length(G) or "NaN" if NetworkXError: Graph is not connected,
                            then it tries to get the average_shortest_path_length from the giant component,
        "avgpathlength" = nx.average_shortest_path_length(max(nx.connected_component_subgraphs(G), key=len))
                                except NetworkXPointlessConcept: ('Connectivity is undefined ', 'for the null graph.'),
        "clustering_coefficient" = nx.average_clustering(G) or "NaN" if ZeroDivisionError: float division by zero
    }
    """
    values = {}
    values["charcount"] = len(G.nodes())
    values["edgecount"] = len(G.edges())
    try:
        values["maxdegree"] = max(G.degree().values())
    except:
        print("ValueError: max() arg is an empty sequence")
        values["maxdegree"] = "NaN"

    try:
        values["avgdegree"] = sum(G.degree().values())/len(G.nodes())
    except:
        print("ZeroDivisionError: division by zero")
        values["avgdegree"] = "NaN"

    try:
        values["density"] = nx.density(G)
    except:
        values["density"] = "NaN"

    try:
        values["avgpathlength"] = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        print("NetworkXError: Graph is not connected.")
        try:
            values["avgpathlength"] = nx.average_shortest_path_length(max(nx.connected_component_subgraphs(G), key=len))
        except:
            values["avgpathlength"] = "NaN"
    except:
        print("NetworkXPointlessConcept: ('Connectivity is undefined ', 'for the null graph.')")
        values["avgdegree"] = "NaN"

    try:
        values["clustering_coefficient"] = nx.average_clustering(G)
    except:
        print("ZeroDivisionError: float division by zero")
        values["clustering_coefficient"] = "NaN"
    return values

def analyze_characters(G):
    """
    Computes per-character metrics of a graph G,
    returns dictionary of dictionaries:
    character_values =
    {
        "betweenness" = nx.betweenness_centrality(G),
        "degree" = nx.degree(G),
        "closeness" = nx.closeness_centrality(G)
    }
    """
    character_values = {}
    character_values["betweenness"] = nx.betweenness_centrality(G)
    character_values["degree"] = nx.degree(G)
    character_values["closeness"] = nx.closeness_centrality(G)
    return character_values

def transpose_dict(d):
    """
    Transpose dict of character-network metrics to an exportable dict,
    essentially transposes rows and columns of the character.csv.
    """
    td = {}
    try:
        for cent, chars in d.items():
            for char in chars:
                td[char] = {}
    except:
        pass
    try:
        for cent, chars in d.items():
            for char, value in chars.items():
                td[char][cent] = value
    except:
        pass
    return td

def export_dict(d, filepath):
    with open(filepath, 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, d.keys())
        w.writeheader()
        w.writerow(d)

def export_dicts(d, filepath):
    with open(filepath, 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=";")
        d = transpose_dict(d)
        try:
            subkeys = list(list(d.values())[0].keys())
            w.writerow([""] + subkeys)
            for k, v in d.items():
                w.writerow([k] + list(v.values()))
        except:
            print("Empty values.")

def randomize_graph(n,e):
    """
    Creates 1000 random graphs with networkx.gnm_random_graph(nodecount, edgecount),
    and computes average_clustering_coefficient and average_shortest_path_length,
    to compare with drama-graph.
    Returns a tuple:
    randavgpathl, randcluster = (float or "NaN", float or "NaN")
    """
    randcluster = 0
    randavgpathl = 0
    c = 0

    for i in range(0, 1000):
        R = nx.gnm_random_graph(n, e)
        try:
            randcluster += nx.average_clustering(R)
            c += 1
        except ZeroDivisionError:
            pass
        j = 0
        while True:
            j += 1
            try:
                R = nx.gnm_random_graph(n, e)
                randavgpathl += nx.average_shortest_path_length(R)
            except:
                pass
            else:
                break
            if j > 50:
                randavgpathl = "NaN"
                break
    try:
        randcluster = randcluster / c
    except:
        randcluster = "NaN"
    try:
        randavgpathl = randavgpathl / 1000
    except:
        randavgpathl = "NaN"
    return randavgpathl, randcluster

def plotGraph(G, figsize=(8, 8), filename=None):
    """
    Plots an individual graph, node size by degree centrality,
    edge size by edge weight.
    """
    labels = {n:n for n in G.nodes()}

    try:
        # for networks with only one node
        d = nx.degree_centrality(G)
        nodesize = [v * 500 for v in d.values()]
    except:
        nodesize = [1 * 250 for n in G.nodes()]

    layout=nx.spring_layout
    pos=layout(G)

    plt.figure(figsize=figsize)
    plt.subplots_adjust(left=0,right=1,bottom=0,top=0.9,wspace=0.01,hspace=0.01)

    # nodes
    nx.draw_networkx_nodes(G,pos,
                            nodelist=G.nodes(),
                            node_color="dodgerblue",
                            node_size=nodesize,
                            alpha=0.8)
    try:
        weights = [G[u][v]['weight'] for u,v in G.edges()]
    except:
        weights = [1 for u,v in G.edges()]
    nx.draw_networkx_edges(G,pos,
                           with_labels=False,
                           edge_color="darkslategrey",
                           width=weights
                        )

    if G.order() < 1000:
        nx.draw_networkx_labels(G,pos, labels)
    plt.savefig(filename)
    plt.close("all")

def plot_superposter(datadir, outputdir):
    """
    Plot harmonically layoutted drama network subplots in 16:9 format.
    Node size by degree centrality,
    edge size by log(weight+1).
    """
    dramas = read_dramas(datadir)
    size = len(dramas)
    y = int(math.sqrt(size/2)*(16/9))
    x = int(size/y)+1

    fig = plt.figure(figsize = (160,90))
    gs = gridspec.GridSpec(x, y)
    gs.update(wspace=0.0, hspace=0.00) # set the spacing between axes.
    i = 0

    # build rectangle in axis coords for text plotting
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height

    id2date = {ID:drama.get("metadata").get("date_definite") for ID, drama in dramas.items()}
    if debug:
        print(id2date)

    # http://pythoncentral.io/how-to-sort-python-dictionaries-by-key-or-value/
    sorted_by_date = sorted(id2date, key=id2date.__getitem__)

    for ID in sorted_by_date:
        drama = dramas.get(ID)

        if debug:
            print(drama.get("metadata"))

        title = drama.get("metadata").get("title")
        if title is None:
            title = drama.get("metadata").get("filename")
            print(title)

        speakers = drama.get("speakers")
        personae = drama.get("personae")
        G = create_graph(speakers, personae)

        try:
            # for networks with only one node
            d = nx.degree_centrality(G)
            nodesize = [v * 110 for v in d.values()]
        except:
            nodesize = [1 * 110 for n in G.nodes()]
        layout=nx.spring_layout
        pos=layout(G)

        ax = plt.subplot(gs[i])
        ax.tick_params(color='white', labelcolor='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')

        if "Goethe" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('firebrick')
            ax.patch.set_alpha(0.2)
        if "Hebbel" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('purple')
            ax.patch.set_alpha(0.2)
        if "Weißenthurn" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('darkgreen')
            ax.patch.set_alpha(0.2)
        if "Schiller" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('darkslategrey')
            ax.patch.set_alpha(0.2)
        if "Wedekind" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('darkslateblue')
            ax.patch.set_alpha(0.2)
        if "Schnitzler" in drama.get("metadata").get("author"):
            ax.patch.set_facecolor('tomato')
            ax.patch.set_alpha(0.2)

        node_color = "steelblue"
        nx.draw_networkx_nodes(G,pos,
                            nodelist=G.nodes(),
                            node_color=node_color,
                            node_size=nodesize,
                            alpha=0.8)

        weights = [math.log(G[u][v]['weight']+1)  for u,v in G.edges()]

        edge_color = "grey"
        nx.draw_networkx_edges(G,pos,
                               with_labels=False,
                               edge_color=edge_color,
                               width=weights
                            )



        title_bark = "".join([w[0] for w in title.split()])
        caption = ", ".join([drama.get("metadata").get("author").split(",")[0],
                             title_bark,
                             str(drama.get("metadata").get("date_definite"))])

        ax.text(0.5*(left+right), 0*bottom, caption,
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=20, color='black',
                transform=ax.transAxes)

        ax.set_frame_on(True)
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.get_xaxis().set_visible(False)

        i += 1

    fig.savefig(os.path.join(outputdir,"superposter.svg"))
    plt.close(fig)

def dramavis(ZFDir, DataDir, GraphDir, random):
    """
    Main function executing the pipeline from
    reading and parsing lina-xmls,
    creating and plotting drama-networks,
    computing graph-metrics and random-graph-metrics,
    exporting SVGs, CSVs and edgelists.
    Can take a while.
    """
    dramas = read_dramas(ZFDir)
    for ID, drama in dramas.items():
    # yields parsed dramas dicts
        title = drama.get("metadata").get("title")
        if not title:
            title = ID
        print("tc"+ID, title)
        if debug:
            print(title)
        if os.path.isfile(os.path.join(GraphDir, str(ID)+title+".svg")):
            continue
        speakers = drama.get("speakers")
        personae = drama.get("personae")
        if debug:
            print(personae)
            print(speakers)
        G = create_graph(speakers, personae)

        graph_metrics = analyze_graph(G)
        graph_metrics["ID"] = ID
        graph_metrics["average_path_length_random"], graph_metrics["clustering_coefficient_random"] = randomize_graph(graph_metrics.get("charcount"), graph_metrics.get("edgecount"))
        graph_metrics["year"] = drama.get("metadata").get("date_print")
        graph_metrics["author"] = drama.get("metadata").get("author")
        graph_metrics["title"] = title
        graph_metrics["filename"] = drama.get("metadata").get("filename")
        graph_metrics["genretitle"] = drama.get("metadata").get("genretitle")
        graph_metrics["scenecount"] = drama.get("metadata").get("scenecount")
        character_metrics = analyze_characters(G)

        if random: 
            for i in range(0, 5):
                R = nx.gnm_random_graph(graph_metrics.get("charcount"), graph_metrics.get("edgecount"))
                plotGraph(R, filename=os.path.join(GraphDir, "tc"+str(ID)+"_"+"random"+str(i)+".svg"))
        export_dict(graph_metrics, os.path.join(DataDir, "tc"+str(ID)+"_graph.csv"))
        export_dicts(character_metrics, os.path.join(DataDir, "tc"+str(ID)+"_chars.csv"))
        plotGraph(G, filename=os.path.join(GraphDir, "tc"+str(ID)+"_nw.svg"))
        nx.write_edgelist(G, os.path.join(DataDir, "tc"+str(ID)+"_edges.csv"), delimiter=";", data=["weight"])


def main(ZFDir, DataDir, GraphDir, action, random, debug):
    if not os.path.isdir(DataDir):
        os.mkdir(DataDir)
    if not os.path.isdir(GraphDir):
        os.mkdir(GraphDir)
    if action == "plotsuperposter":
        plot_superposter(ZFDir, GraphDir)
    if action == "dramavis":
        dramavis(ZFDir, DataDir, GraphDir, random)

main(ZFDir, DataDir, GraphDir, action, random, debug)

#parser = argparse.ArgumentParser(description='analyze and plot from lina-xml to networks')
#parser.add_argument('--input', dest='inputfolder', help='relative or absolute path of the input-xmls folder')
#parser.add_argument('--output', dest='outputfolder', help='relative or absolute path of the output folder')
#parser.add_argument('--action', dest='action', help='what to do, either plotsuperposter or dramavis')
#parser.add_argument('--debug', dest='debug', help='print debug message or not', action="store_true")
#args = parser.parse_args()#

#if __name__ == '__main__':
#    main(args)
