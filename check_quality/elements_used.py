# -*- coding: utf-8 -*-
# Filename: elements_used.py
"""
Created on Thu May 21 15:57:56 2015

@author: Ulrike Henny

The program creates an overview of the elements and attributes 
used in a collection of XML files.

It is possible: 
- to get an overview of which and how many elements and 
attributes are used in the collection as a whole
- to get an overview of which and how many elements and
attributes are used in a certain file
- to get an overview of in which files a certain element
or a certain attribute is used and how often

The output is:
- a CSV file listing the filenames of the XML files in
the collection, the element and attribute names and the
number of their occurrences
- a JSON file listing the information compactly
- in single mode: an image file with a group of bar charts displaying 
the results for the chosen options
- in all mode: all possible bar charts are created

Args:
    coll_path (str): path to the collection of XML files
    coll_name (str): name of the collection
    mode (str): optional argument; possible values: "single", "all". In all-mode, all possible visualizations are created. In single-mode, a specific visualization can be selected. Default: "single"
    name (str): optional argument; filename or elememt/attribute name, e.g. "nl0025.xml" or "div" or "@type"
    out (str): optional argument; path to the output directory; defaults to the current working directory
    namespace (str): optional argument; namespace for the collection; defaults to the TEI namespace
    xpath (str): optional argument; XPath expression indicating which elements and/or attributes to select for the overview; defaults to the TEI body 
    log (bool): sets the y scale to logarithmic
    
Returns:
    str: A message.
    
A documentation can be found at http://cligs.hypotheses.org/276
"""


#######################
# Import statements   #
#######################

import argparse
import glob
import json
import numpy as np
import os
import re
from lxml import etree
from matplotlib import pyplot as plt
from sys import argv,exit,stdout


#######################
# Variable, General   #
#######################

# name of the output folder which will be created by this program
out_dir_name = "elements_used"


#######################
# Functions, General  #
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
    


def unique_names(names):
    """
    Return only unique elements of a list of names.
    
    Args:
        names (list): List of element or attribute names        
        
    Returns:
        List with unique names
    """
    return sorted(set(names))
    


def create_out_dir(out):
    """
    Creates the output directory.
    
    Args:
        out (str): path to the output directory
    Returns:
        None
    """    
    out_path = os.path.join(out,out_dir_name)
    try:
        os.stat(out_path)
    except:
        os.mkdir(out_path)


#######################
# Functions, Get Info #
#######################

def get_fileinfos(coll_path, namespace, xpath, out):
    """
    Creates a dictionary containing all the necessary information:
    for each file - which element and attributes occur and how often?
    Dumps the result to a JSON and a CSV file.
    
    Args:
        coll_path (str): path to the collection
        namespace (str): namespace for the collection; defaults to the TEI namespace
        xpath (str): XPath expression indicating which elements and/or attributes to select for the overview; defaults to the TEI body
        out (str): path to output directory; defaults to the current working directory        
        
    Returns:
        dict: information about element/attribute usage in a text collection
    """
    
    list_of_filenames = check_paths(coll_path, out)
        
    fileinfos = {}
    stdout.write("... gathering information\n")
    
    all_el_names_set = []
    all_att_names_set = []
    
    # loop trough each file in the collection
    for filepath in list_of_filenames:
        filename = os.path.basename(filepath)
        print(filename)
        
        xml = etree.parse(filepath)
        if (namespace != ""):
            namespaces = {"ns":namespace}
        else:
            namespaces = {}
        
        # get all elements
        all_el = xml.xpath(xpath, namespaces=namespaces)
        
        # collect all element/attribute names
        all_el_names = get_all_names(all_el, "el")
        all_att_names = get_all_names(all_el, "att")
        
        for el_name in all_el_names:
            all_el_names_set.append(el_name)
        for att_name in all_att_names:
            all_att_names_set.append(att_name)
       
        
        # count different elements/attributes
        usage_el = get_usage(all_el_names)
        usage_att = get_usage(all_att_names)        
        
        # add to fileinfos
        fileinfos[filename] = {"usage_el":usage_el, "usage_att":usage_att}
        
    all_el_names_set = sorted(set(all_el_names_set))
    all_att_names_set = sorted(set(all_att_names_set))
    
    
    # write results to JSON file
    dump_to_json(fileinfos, out)
    # write results to CSV file
    dump_to_csv(fileinfos, out, all_el_names_set, all_att_names_set)
    
    
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
    for item in unique_names(names):
        usage[item] = names.count(item)
    return usage



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
                
    items_counted = {}
    
    if is_filename(name) or name == "":
        for singleName in unique_names(names):
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


#######################
# Functions, Dump  #
#######################

def dump_to_json(fileinfos, out):
    """
    Dump the fileinfos to a JSON file.
    
    Args:
        fileinfos (dict): Dictionary containing information about element/attribute usage
        out (str): path to output directory; defaults to the current working directory
        
    Returns:
        None
    """
    jsonarray = json.dumps(fileinfos)
    json_filename = "all_elements_used.json"
    text_file = open(os.path.join(out,out_dir_name,json_filename), "w")
    text_file.write(jsonarray)
    text_file.close()
    stdout.write("... "+json_filename+" created\n")



def dump_to_csv(fileinfos, out, all_el_names, all_att_names):
    """
    Dump the fileinfos to a CSV file.
    
    Args:
        fileinfos (dict): Dictionary containing information about element/attribute usage
        out (str): path to output directory; defaults to the current working directory
        all_el_names (list): list of all occurring element names
        all_att_names (list): list of all occurring attribute names
        
    Returns:
        None
    """
    uni_el_names = unique_names(all_el_names)
    uni_att_names = unique_names(all_att_names)    
    att_names_prefixed = ["@%s" % item for item in uni_att_names]
    csv_filename = "all_elements_used.csv"
    
    # transform information from dictionary to CSV format
    with open(os.path.join(out,out_dir_name,csv_filename), "w") as fout:
        fout.write("," + ",".join(uni_el_names) + "," + ",".join(att_names_prefixed) + "\n")
        for key in fileinfos:
            el_str = ""
            for eln in uni_el_names:
                if (eln in fileinfos[key]["usage_el"]):
                    el_str += "," + str(fileinfos[key]["usage_el"][eln])
                else:
                    el_str += ",0"
            att_str = ""
            for attn in uni_att_names:
                if (attn in fileinfos[key]["usage_att"]):
                    att_str += "," + str(fileinfos[key]["usage_att"][attn])
                else:
                    att_str += ",0"
            fout.write(key + el_str + att_str + "\n")
    stdout.write("... "+csv_filename+" created\n")
    
    
#######################
# Functions, Check    #
#######################
    
def check_paths(coll_path, out):
    """
    Checks whether the collection and XML files can be found.    
    
    Args:
        coll_path (str): path to the collection of XML files
        out (str): path to output directory; defaults to the current working directory
    
    Returns:
        list: a list of filenames
    """
    pathpattern = os.path.join(coll_path,"*.xml")
    try:
        if not os.path.exists(coll_path):
            raise ValueError("Error: The collection could not be found.")
    except ValueError as err:
        print(err)
        exit(1)
    try:
        if not os.path.exists(out):
            raise ValueError("Error: The output directory could not be found.")
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
    return list_of_filenames
    
    
    
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


#######################
# Functions, Charts   #
#######################

def draw_figure(els_counted, atts_counted, arg, name=""):
    """
    Creates a figure to hold charts about element/attribute usage.
    
    Args:
        els_counted (dict): Information about element names and their occurrences
        atts_counted (dict): Information about attribute names and their occurrences
        args (obj): arguments passed to the main function
        name (str): optional argument; filename of element/attribute name
        
    Returns:
        None; saves the figure/image file
    """
    
    stdout.write("... drawing chart\n")    
    fig_width = max(len(els_counted),len(atts_counted),10)
    fig_height = 6
    if is_filename(name) or name == "":
        fig_height *= 2
    fig = plt.figure(figsize=(fig_width,fig_height))
    
    chart_info = get_chart_info(arg.coll_name, name)    
    add_subplots(fig, els_counted, atts_counted, chart_info, name, arg.log)
    
    plt.tight_layout()   
    save_figure(fig, arg.out, name)
    plt.close()
    
    

def add_subplots(fig, els_counted, atts_counted, chart_info, name="", log=False):
    """
    Adds subplots to the figure.
    
    Args:
        fig (obj): Figure for the charts
        els_counted (dict): Information about element names and their occurrences
        atts_counted (dict): Information about attribute names and their occurrences  
        chart_info (dict): Some general information for the chart
        name (str): optional argument; filename of element/attribute name
        log (bool): sets the y scale to logarithmic
    
    Returns:
        None
    """
    if name != "":
        if is_filename(name):
            # overview of element/attribute usage for a single text
            draw_chart(els_counted, fig, chart_info["elements_used_text"], log)
            draw_chart(atts_counted, fig, chart_info["attributes_used_text"], log)
        elif is_attname(name):
            # overview for a specific attribute
            draw_chart(atts_counted, fig, chart_info["attribute_used"], log)
        else:
            # overview for a specific element
            draw_chart(els_counted, fig, chart_info["element_used"], log)
    else:
        # overall overview of element and attribute usage
        draw_chart(els_counted, fig, chart_info["elements_used_all"], log)
        draw_chart(atts_counted, fig, chart_info["attributes_used_all"], log)



def save_figure(fig, out, name=""):
    """
    Save the figure
    
    Args:
        fig (obj): Figure for the charts
        out (str): path to output directory; defaults to the current working directory        
        name (str): optional argument; filename of element/attribute name
    
    Returns:
        None
    """
    filename_out = ""    
    if name != "":
        if is_filename(name):
            filename_out = "file_"+name+".png"
        elif is_attname(name):
            filename_out = "att_"+name[1:]+".png"
        else:
            filename_out = "el_"+name+".png"
    else:
        filename_out = "all_elements_used.png"
    fig.savefig(os.path.join(out,out_dir_name,filename_out))
    stdout.write("... "+filename_out+" created\n")



def get_chart_info(coll_name, name):
    """
    Creates some metadata for the chart: position, title, axis lables etc.

    Args:
        coll_name (str): name of the text collection
        name (str): name of the file or element/attribute name
        
    Returns:
        dict: Some general information for the chart
    """
    
    chart_info = {
        "elements_used_all":{"position":211,
                         "color":"#4785C2",
                         "label_x":"element names",
                         "label_y":"element occurrences",
                         "title":"elements used in collection '"+coll_name+"'"},
        "attributes_used_all":{"position":212,
                           "color":"#339999",
                           "label_x":"attribute names",
                           "label_y":"attribute occurrences",
                           "title":"attributes used in collection '"+coll_name+"'"},
        "elements_used_text":{"position":211,
                              "color":"#4785C2",
                              "label_x":"element names",
                              "label_y":"element occurences",
                              "title":"elements used in file '"+name+"'"},
        "attributes_used_text":{"position":212,
                                "color":"#339999",
                                "label_x":"attribute names",
                                "label_y":"attribute occurrences",
                                "title":"attributes used in file '"+name+"'"},
        "element_used":{"position":111,
                        "color":"#4785C2",
                        "label_x":"filenames",
                        "label_y":"number of occurrences",
                        "title":"usage of element '"+name+"' in collection '"+coll_name+"'"},
        "attribute_used":{"position":111,
                          "color":"#339999",
                          "label_x":"filenames",
                          "label_y":"number of occurrences",
                          "title":"usage of attribute '"+name+"' in collection '"+coll_name+"'"}
    }
    return chart_info



def draw_chart(data, figure, chart_info, log=False):
    """
    Draws a chart (adds a subplot to the figure).
        
    Args:
        data (dict): element/attribute names and their number of occurrences
        figure (obj): the figure object to which the subplot shall be added
        chart_info (dict): some information about the chart (title, labels etc.)
        log (bool): sets the y scale to logarithmic
    
    Returns:
        None; changes the figure
    """    
    
    # number of elements on x-axis
    N = len(data)
    if N == 0:    
        N = 1
    # prepare labels and values
    labels_x = tuple(sorted(data.keys()))
    values_y = []
    for val in labels_x:
        values_y.append(data[val])
    if not values_y:
        values_y.append(1)
    tuple(values_y)
    max_y = max(values_y)
    # x locations for the bars
    ind = np.arange(N)
    # width of bars
    width = 0
    if N < 5:
        width = 0.25
    else:
        width = 0.75
    # x axis margin
    x_ma = 0
    if N == 1:
        x_ma = 1
    else:
        x_ma = 0.5/N
        
    # add subplot     
    sp = figure.add_subplot(chart_info["position"])
    sp.bar(ind,values_y,width,color=chart_info["color"],align="center",log=log) 
    # customize axes
    sp.axes.margins(x_ma,0)
    sp.axes.set_ylim(top=max_y+max_y/4+0.2)
    if log == True:
        sp.axes.set_yscale("log",nonposy="clip")
    # add text for labels, title, axis ticks
    sp.set_xlabel(chart_info["label_x"])
    sp.set_ylabel(chart_info["label_y"])
    sp.set_title(chart_info["title"])
    sp.set_xticks(ind)
    sp.set_xticklabels(labels_x,rotation=90)
    
    
#######################
# Mode                #
#######################

def process_single(fileinfos, args):
    """
    Creates just one visualization according to the chosen options.
    
    Args:
        fileinfos (dict): Dictionary with information about elements in the collection
        args (obj): arguments passed to the main function
    Returns:
        None
    """
    # does the file name exist?
    if is_filename(args.name):
        check_filename(args.name, fileinfos)
    # does the attribute name exist?
    elif is_attname(args.name):
        check_attname(args.name, fileinfos)
    # does the element name exist?             
    elif args.name != "":
        check_elname(args.name, fileinfos)
            
    count_and_draw(fileinfos, args, args.name)
    
    
    
def process_all(fileinfos, args):
    """
    Creates all types of visualizations supported by this program.
    
    Args:
        fileinfos (dict): Dictionary with information about elements in the collection
        args (obj): arguments passed to the main function
    Returns:
        None
    """
    # create overall figure
    count_and_draw(fileinfos,args)
    # create figures for all the files
    for key in fileinfos:
        count_and_draw(fileinfos,args,key)
    # create figures for all the elements
    els_processed = []
    for key in fileinfos:
        for key in fileinfos[key]["usage_el"]:
            if key not in els_processed:
                count_and_draw(fileinfos,args,key)
                els_processed.append(key)
    # create figures for all the attributes
    atts_processed = []
    for key in fileinfos:
        for key in fileinfos[key]["usage_att"]:
            if key not in atts_processed:
                count_and_draw(fileinfos,args,"@"+key)
                atts_processed.append(key)
    
    

def count_and_draw(fileinfos, args, name=""):
    """
    Count elements and attributes and draw figure
    
    Args:
        fileinfos (dict): Dictionary with information about elements in the collection
        args (obj): arguments passed to the main function
        name (str): optional argument; filename or elememt/attribute name, e.g. "nl0025.xml" or "div" or "@type"
    Returns:
        None
    """
    els_counted = count_items(fileinfos,"el",name)
    atts_counted = count_items(fileinfos,"att",name)
    draw_figure(els_counted, atts_counted, args, name)


#######################
# Main                #
#######################

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("coll_path", type=str, help="path to the collection")
    parser.add_argument("coll_name", type=str, help="name of the collection")
    parser.add_argument("-m", "--mode", type=str, default="single", help="single: just one visualization which can be selected; all: all visualizations are created")
    parser.add_argument("-n", "--name", type=str, default="", help="name of file, element or attribute")
    parser.add_argument("-o", "--out", type=str, default=".", help="path to output directory; defaults to the current working directory")
    parser.add_argument("-ns", "--namespace", type=str, default="http://www.tei-c.org/ns/1.0", help="namespace for the collection; defaults to the TEI namespace")
    parser.add_argument("-x", "--xpath", type=str, default="//ns:body//*", help="path expression for element selection; defaults to the TEI body")
    parser.add_argument("-l", "--log", type=bool, help="sets the y scale to logarithmic")    
    return parser.parse_args()



def main(argv):
    """
        Creates an overview of the elements and attributes used in a collection of XML files.
        
        Args:
            coll_path (str): path to the collection of XML files
            coll_name (str): name of the collection
            mode (str): optional argument; possible values: "single", "all". In all-mode, all possible visualizations are created. In single-mode, a specific visualization can be selected. Default: "single"
            name (str): optional argument; filename or elememt/attribute name, e.g. "nl0025.xml" or "div" or "@type"
            out (str): optional argument; path to the output directory; defaults to the current working directory
            namespace (str): optional argument; namespace for the collection; defaults to the TEI namespace
            xpath (str): optional argument; XPath expression indicating which elements and/or attributes to select for the overview; defaults to the TEI body 
            log (bool): sets the y scale to logarithmic
   
        Returns:
            str: A message.
    """    
    args = parse_args()    
    
    # create output directory
    create_out_dir(args.out)
    # collect all the necessary information (for all scenarios)
    fileinfos = get_fileinfos(args.coll_path, args.namespace, args.xpath, args.out)
    
    if (args.mode == "all"):
        process_all(fileinfos, args)
    else:
        process_single(fileinfos, args)

    stdout.write("Done: the element usage overview has been created\n")
    
        

if __name__ == "__main__":
    main(argv) 
