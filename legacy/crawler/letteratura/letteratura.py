# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: biblita-requests.py

"""
# Using "requests" to get stuff from the web (in this case, from biblita).
"""

import requests
import re

vols = list(range(1,9,1))
ids = list(range(0,400,1))
#print(ids)
for vol in vols:
    for id in ids: 
        #print(id)
        suffix = "Volume_"+str(vol)+"/t"+str(id)+".pdf"
        url = "http://www.letteraturaitaliana.net/pdf/" + suffix
        print(url)
        filename = suffix
        #print(filename)
        play = requests.get(url, timeout=3.1)
        #print(play.text)
        filepath = "./texte/" + filename
        with open(filepath, "w", encoding="utf8") as outfile:
            outfile.write(play.text)
