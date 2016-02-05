# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: biblita-requests.py

"""
# Using "requests" to get stuff from the web (in this case, from biblita).
"""

import requests
import re

ids = list(range(1200, 1400, 1))
#print(ids)
for id in ids:
    id = '{:06d}'.format(id)
    #print(id)
    suffix = "bibit"+id+"/bibit"+id+".xml"
    url = "http://ww2.bibliotecaitaliana.it/repository/bibit/" + suffix
    #print(url)
    filename = suffix[-15:]
    try:
        play = requests.get(url, timeout=3.1)
        print(filename, "ok")
        #print(play.text)
        filepath = "./texte2/" + filename
        with open(filepath, "w", encoding="utf8") as outfile:
            outfile.write(play.text)
    ## exception fangen und überspringen ##
    except Exception:
        print(filename, "error")

## Ab ca 004000 nur noch 404; getestet bis 018946.