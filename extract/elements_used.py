# -*- coding: utf-8 -*-
# Filename: elements-used.py
"""
Created on Thu May 21 15:57:56 2015

@author: Ulrike Henny

- creates an overview of the TEI elements and attributes used in a text collection
- generates a json file named "fileinfos.json" with the following information for each file in the text collection:
   {filename:{"usage_el":{"el_name":number},"usage_att":{"att_name":number}}}
- generates bar charts stored as "elements_used.png"
- possible bar chart outputs:
  (1) overall usage of elements and attributes in all text files
  (2) usage of elements and attributes in a specific text file
  (3) usage of a specific element in all text files
  (4) usage of a specific attribute in all text files

Args:
    collection_path (str): path to the collection (of TEI files)
    collection_name (str): name of the collection
    name (str): optional argument; filename or elememt/attribute name
    
Returns:
    str: A message.

"""

#######################
# Import statements   #
#######################

import os
import glob
import json
import numpy as np
import re
from lxml import etree
from matplotlib import pyplot as plt
from sys import argv,exit,stdout


#######################
# Functions           #
#######################

def print_err(err):
    """
    Prints an error message.
    
    Args:
        err (?): error
    
    Returns:
        Error message
    """
    return stdout.write(err.args[0])
    
    

def get_fileinfos(collection_path):
    """
    Creates a dictionary containing all the necessary information:
    for each file - which element and attributes occur and how often?
    
    Args:
        collection_path (str): path to the collection
        
    Returns:
        dict: information about element/attribute usage in a text collection
    """
    pathpattern = collection_path + "*.xml"
    
    try:
        if not os.path.exists(collection_path):
            raise ValueError("Error: The collection cound not be found.")
    except ValueError as err:
        print(err)
        exit(1)
    list_of_filenames = glob.glob(pathpattern)
    try:
        if not list_of_filenames:
            raise ValueError("Error: No XML file was found in the collection.")
    except ValueError as err:
        print(err)
        exit(1)
        
    fileinfos = {}
    # loop trough each file in the collection
    for filepath in list_of_filenames:
        filename = os.path.basename(filepath)
        
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
    dump_to_json(fileinfos)
    
    return fileinfos



def get_all_names(nodes, type):
    """
    Gets the names of occurring elements/attributes.
    
    Args:
        nodes (list): list of XML element/attribute nodes
        type (str): "el" or "att"
        
    Returns:
        list: a list of element/attribute names
    """
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
        


def get_usage(names):
    """
    Gets the number of occurrences for each element/attribute.
    
    Args:
        names (list): List of element/attribute names
        
    Returns:
        dict: Dictionary containing element/attribute names and their number of occurrences
    """   
    usage = {}    
    for item in sorted(set(names)):
        usage[item] = names.count(item)
    return usage



def dump_to_json(fileinfos):
    """
    Dump the fileinfos to a JSON file.
    
    Args:
        fileinfos (dict): Dictionary containing information about element/attribute usage
        
    Returns:
        None
    """
    jsonarray = json.dumps(fileinfos)
    text_file = open("fileinfos.json", "w")
    text_file.write(jsonarray)
    text_file.close()



def count_items(fileinfos, type, name=""):
    """
    Counts the element/attribute usage based on the information found in fileinfos.
    
    Args:
        fileinfos (dict): Information about element/attribute usage in a collection
        type (str): "el" or "att"
        name (str): optional argument; filename or element/attribute name
                    If a filename is indicated, elements/attributes are counted for that file only.
                    Otherwise, they are counted for all texts.
                    If an attribute or element name is indicated, occurrences are only counted
                    for that element/attribute.
    
    Returns:
        dict: Information about the number of items.
    """
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
    
    
    
def is_filename(name):
    """
    Tests if the input string is an XML filename
    
    Args:
        name (str): string to test
        
    Returns:
        bool
    """
    test = re.search("[A-Za-z0-9_-]+\.xml$", name)
    if test:
        return True
    else:
        return False
        


def is_attname(name):
    """
    Tests if the input string is an attribute name
    
    Args:
        name (str): string to test
        
    Returns:
        bool
    """
    test = re.search("^@[a-z]+", name)
    if test:
        return True
    else:
        return False



def check_filename(name, fileinfos):
    """
    Check if a file exists in the collection.
    
    Args:
        name (str): name of the file
        fileinfos (dict): Dictionary with information about files in the collection
        
    Returns:
        None
    """    
    try:
        if not name in fileinfos.keys():
            raise ValueError("Error: The XML file could not be found.")
    except ValueError as err:
        print(err)
        exit(1)      
        

        
def check_attname(name, fileinfos):
    """
    Check if an attribute exists in the collection.
    
    Args:
        name (str): name of the attribute
        fileinfos (dict): Dictionary with information about attributes in the collection
        
    Returns:
        None
    """
    num = 0            
    for file in fileinfos:
        if name[1:] in fileinfos[file]["usage_att"].keys():
            num += fileinfos[file]["usage_att"][name[1:]]
    try:
        if num == 0:
            raise ValueError("Error: No attribute '"+name+"' was found in the collection.")
    except ValueError as err:
        print(err)
        exit(1)


def check_elname(name, fileinfos):
    """
    Check if an element exists in the collection.
    
    Args:
        name (str): name of the element
        fileinfos (dict): Dictionary with information about elements in the collection
        
    Returns:
        None
    """
    num = 0
    for file in fileinfos:
        if name in fileinfos[file]["usage_el"].keys():
            num += fileinfos[file]["usage_el"][name]
    try:
        if num == 0:
            raise ValueError("Error: No element '"+name+"' was found in the collection.")
    except ValueError as err:
        print(err)
        exit(1)


def draw_figure(els_counted, atts_counted, collection_name, name=""):
    """
    Creates a figure to hold charts about element/attribute usage.
    
    Args:
        els_counted (dict): Information about element names and their occurrences
        atts_counted (dict): Information about attribute names and their occurrences
        collection_name (str): name of the text collection
        name (str): optional argument; filename of element/attribute name
        
    Returns:
        None; saves the figure/image file
    """
    
    fig_width = max(len(els_counted),len(atts_counted),36) / 3
    fig_height = 6
    if is_filename(name) or name == "":
        fig_height *= 2
    fig = plt.figure(figsize=(fig_width,fig_height))
    
    chart_info = get_chart_info(collection_name, name)    
    
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
    


def get_chart_info(collection_name, name):
    """
    Creates some metadata for the chart: position, title, axis lables etc.
    
    Args:
        collection_name (str): name of the text collection
        name (str): name of the file or element/attribute name
        
    Returns:
        dict: Some general information for the chart
    """
    
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
    return chart_info



def draw_chart(data, figure, chart_info):
    """
    Draws a chart (adds a subplot to the figure).
        
    Args:
        data (dict): element/attribute names and their number of occurrences
        figure (obj): the figure object to which the subplot shall be added
        chart_info (dict): some information about the chart (title, labels etc.)
    
    Returns:
        None; changes the figure
    """    
    
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
    
        

#######################
# Main                #
#######################

def main(collection_path,collection_name,name=""):
    """
        Creates an overview of the TEI elements and attributes used in a text collection.
        
        Args:
            collection_path (str): path to the collection
            collection_name (str): name of the text collection
            name (str): optional argument. 
                        - overall element/attribute usage? - leave name empty
                        - element/attribute usage for a specific text? - indicate filename
                        - overview for a specific element/attribute? - indicate element/attribute name
                        e.g. "nl0025.xml" or "div" or "@type"
        
        Returns:
            str: A message.
    """    
    
    # collect all the necessary information (for all scenarios)
    fileinfos = get_fileinfos(collection_path)
    
    # does the file name exist?
    if is_filename(name):
        check_filename(name, fileinfos)
    # does the attribute name exist?
    elif is_attname(name):
        check_attname(name, fileinfos)
    # does the element name exist?             
    elif name != "":
        check_elname(name, fileinfos)
            
    # count el and att usage
    els_counted = count_items(fileinfos,"el",name)
    atts_counted = count_items(fileinfos,"att",name)

    # draw bar charts
    draw_figure(els_counted, atts_counted, collection_name, name)

    stdout.write("Info: The element usage overview has been created.")
    
        

if len(argv) == 4:
    main(argv[1],argv[2],argv[3])
elif len(argv) == 3:
    main(argv[1],argv[2])
elif len(argv) == 2:
    stdout.write("Error: Please indicate a collection name.")    
elif len(argv) == 1:
    stdout.write("Error: Please indicate a collection path.")
else:
    stdout.write("Error: Too many arguments.")