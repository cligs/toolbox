# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: biblita-requests.py

"""
# Using "requests" to get stuff from the web (in this case, from biblita).
"""

import requests
import re

"""
# Liste der relevanten Text-IDs
with open("1.html", "r") as infile: 
    page = infile.read()
    #print(alldata)

    data = re.findall("bibit[\d]{5,7}",page)
    #print(len(data))
    #print(data)
    
    suffixes = []
    for entry in data: 
    #print(entry)
        suffix = entry + "/" + entry + ".xml"
        #print(suffix)
        suffixes.append(suffix)
    suffixes = list(set(suffixes))
    suffixes = suffixes[14:16]
    #print(len(suffixes))
    #print(suffixes)
    
    #11, 12, 15


	  ### Herunterladen der einzelnen XML-Dateien
    for suffix in suffixes:
        url = "http://ww2.bibliotecaitaliana.it/repository/bibit/" + suffix
        print(url)
        filename = suffix[-15:]
        #print(filename)
        play = requests.get(url)
        #print(play.text)
        filepath = "./plays/" + filename
        with open(filepath, "w", encoding="utf8") as outfile:
            outfile.write(play.text)

"""


url = "http://ww2.bibliotecaitaliana.it/repository/bibit/bibit000389/bibit000389.xml"
filename = url[-15:]
print(filename)
play = requests.get(url)
#print(play.text)
filepath = "./plays3/" + filename
with open(filepath, "w", encoding="utf8") as outfile:
    outfile.write(play.text)