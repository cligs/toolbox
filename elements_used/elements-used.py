# -*- coding: utf-8 -*-
# Filename: elements-used.py
"""
Created on Thu May 21 15:57:56 2015

@author: Ulrike

# - creates an overview of the TEI elements and attributes used in a text collection
# - generates a json file named "fileinfos.json" 
#   with the following information for each file in the text collection:
#   {filename:{"usage_el":{"el_name":number},"usage_att":{"att_name":number}}}
# - generates bar charts stored as "elements_used.png"
# - possible bar chart outputs:
#   (1) overall usage of elements and attributes in all text files
#   (2) usage of elements and attributes in a specific text file
#   (3) usage of a specific element in all text files
#   (4) usage of a specific attribute in all text files
"""

#######################
# Import statements   #
#######################

import glob
import json
import numpy as np
import re
from lxml import etree
from matplotlib import pyplot as plt


#######################
# Functions           #
#######################


# get names of occurring elements or attributes
# type = "el" | "att"
def get_all_names(nodes, type):
    if type == "el":
        el_names = []        
        for el in nodes:
            el_names.append(etree.QName(el).localname)
        return el_names
    elif type == "att":
        att_names = []
        for el in nodes:
            for att_name in el.keys():
                att_names.append(etree.QName(att_name).localname)
        return att_names
                
# get the number of occurrences for each element/attribute
# creates a dictionary
def get_usage(names):
    usage = {}    
    for item in sorted(set(names)):
        usage[item] = names.count(item)
    return usage
                
# creates a dictionary containing all the necessary information:
# for each file - which elements and attributes occur and how often?
def get_fileinfos(collection_name):
    pathpattern = "../../" + collection_name + "/master/*.xml"
    
    fileinfos = {}    
    # loop trough each file in the collection
    for filepath in glob.glob(pathpattern):
        filename = re.search("[A-Za-z0-9_-]+\.xml$", filepath).group(0)
        
        xml = etree.parse(filepath)
        namespaces = {"tei":"http://www.tei-c.org/ns/1.0"}
        
        # get all elements
        all_el = xml.xpath("//tei:body//*", namespaces=namespaces)
        
        # collect all element/attribute names
        all_el_names = get_all_names(all_el, "el")
        all_att_names = get_all_names(all_el, "att")
        
        # count different elements/attributes
        usage_el = get_usage(all_el_names)
        usage_att = get_usage(all_att_names)        
        
        # add to fileinfos
        fileinfos[filename] = {"usage_el":usage_el, "usage_att":usage_att}
    
    # write results to json file
    jsonarray = json.dumps(fileinfos)
    text_file = open("fileinfos.json", "w")
    text_file.write(jsonarray)
    text_file.close()
    
    return fileinfos
    

# test if the input string/name is a filename
def is_filename(name):
    test = re.search("[A-Za-z0-9_-]+\.xml$", name)
    if test:
        return True
    else:
        return False
        
        
# test if the input string/name is an attribute name
def is_attname(name):
    test = re.search("^@[a-z]+", name)
    if test:
        return True
    else:
        return False
        
        
# count element or attribute usage
# type = "el" | "att"
# name = optional parameter; filename
# if a filename is indicated, elements/attributes are counted for that file
# otherwise, they are counted for all texts
# if an attribute or element name is indicated, occurrences are only counted
# for that element/attribute
def count_items(fileinfos, type, name=""):
    names = []    
    if is_filename(name):
       # count all elements/attributes for one text
        for nodeName in fileinfos[name]["usage_" + type].keys():
            names.append(nodeName) 
    elif name == "":
        # count all elements/attributes for all texts
        for filename in fileinfos:
            for nodeName in fileinfos[filename]["usage_" + type].keys():
                names.append(nodeName)
                
    names_unique = sorted(set(names))
    items_counted = {}
    
    if is_filename(name) or name == "":
        for singleName in names_unique:
            counter = 0
            for file in fileinfos:
                counter += fileinfos[file]["usage_" + type].get(singleName, 0)
            items_counted[singleName] = counter
    elif is_attname(name):
        # count attribute usage for all texts
        for file in fileinfos:
            if name[1:] in fileinfos[file]["usage_att"].keys():
                items_counted[file] = fileinfos[file]["usage_att"][name[1:]]
    else:
        # count element usage for all texts
        for file in fileinfos:
            if name in fileinfos[file]["usage_el"].keys():
                items_counted[file] = fileinfos[file]["usage_el"][name]
    return items_counted
    

# draw a chart (adds a subplot to the figure)
def draw_chart(data, figure, chart_info):
    
    # number of elements on x-axis
    N = len(data)
    # prepare labels and values
    labels_x = tuple(sorted(data.keys()))
    values_y = []
    for val in labels_x:
        values_y.append(data[val])
    tuple(values_y)
    # x locations for the bars
    ind = np.arange(N)
    # width of bars
    width = 0.75
        
    # add subplot     
    ax = figure.add_subplot(chart_info["position"])
    ax.bar(ind,values_y,width,color=chart_info["color"]) 
    # add text for labels, title, axis ticks
    ax.set_xlabel(chart_info["label_x"])
    ax.set_ylabel(chart_info["label_y"])
    ax.set_title(chart_info["title"])
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(labels_x,rotation=90)
    
    
# draw charts for element and attribute usage
def draw_charts(els_counted, atts_counted, collection_name, name=""):
    
    fig_width = max(len(els_counted),len(atts_counted),36) / 3
    fig_height = 6
    if is_filename(name) or name == "":
        fig_height *= 2
    fig = plt.figure(figsize=(fig_width,fig_height))
    
    # some data for chart title, labels, ...
    chart_info = {
        "elements_used_all":{"position":211,
                         "color":"g",
                         "label_x":"element names",
                         "label_y":"element occurrences",
                         "title":"elements used in text collection '"+collection_name+"'"},
        "attributes_used_all":{"position":212,
                           "color":"r",
                           "label_x":"attribute names",
                           "label_y":"attribute occurrences",
                           "title":"attributes used in text collection '"+collection_name+"'"},
        "elements_used_text":{"position":211,
                              "color":"g",
                              "label_x":"element names",
                              "label_y":"element occurences",
                              "title":"elemens used in text '"+name+"'"},
        "attributes_used_text":{"position":212,
                                "color":"r",
                                "label_x":"attribute names",
                                "label_y":"attribute occurrences",
                                "title":"attributes used in text '"+name+"'"},
        "element_used":{"position":111,
                        "color":"g",
                        "label_x":"filenames",
                        "label_y":"number of occurrences",
                        "title":"usage of element '"+name+"' in text collection '"+collection_name+"'"},
        "attribute_used":{"position":111,
                          "color":"r",
                          "label_x":"filenames",
                          "label_y":"number of occurrences",
                          "title":"usage of attribute '"+name+"' in text collection '"+collection_name+"'"}
    }
    
    # add suplots to the figure
    if name != "":
        if is_filename(name):
            # overview of element/attribute usage for a single text
            draw_chart(els_counted, fig, chart_info["elements_used_text"])
            draw_chart(atts_counted, fig, chart_info["attributes_used_text"])
        elif is_attname(name):
            # overview for a specific attribute
            draw_chart(atts_counted, fig, chart_info["attribute_used"])
        else:
            # overview for a specific element
            draw_chart(els_counted, fig, chart_info["element_used"])
    else:
        # overall overview of element and attribute usage
        draw_chart(els_counted, fig, chart_info["elements_used_all"])
        draw_chart(atts_counted, fig, chart_info["attributes_used_all"])
    
    plt.tight_layout()        
    fig.savefig("elements_used.png")
        

#######################
# Main                #
#######################

def main(collection_name,name=""):
    
    # collect all the necessary information (for all scenarios)
    fileinfos = get_fileinfos(collection_name)
    
    # count el and att usage
    els_counted = count_items(fileinfos,"el",name)
    atts_counted = count_items(fileinfos,"att",name)

    # draw bar charts
    draw_charts(els_counted, atts_counted, collection_name, name)
        
        
        
    

# 1st parameter: name of the text collection
# optional 2nd parameter: name
#   which information to show: 
#       - overall element/attribute usage? - leave name empty
#       - element/attribute usage for a specific text? - indicate filename
#       - overview for a specific element/attribute? - indicate element/attribute name
#       e.g. "nl0025.xml" or "div" or "@type"
main("novelaslatinoamericanas","p")