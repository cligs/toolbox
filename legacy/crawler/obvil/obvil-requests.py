# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: obvil-requests.py

"""
# Using "requests" to get stuff from the web (in this case, from obvil).
"""

import requests
import re

def get_obvil(file):
    with open(file, "r") as raw:
        raw = raw.read()
        names = re.findall("<(.*?)>", raw)
        #print(names)

        for name in names:
            url = "http://obvil.paris-sorbonne.fr/corpus/critique/" + name[:-1] + ".xml"
            print(url)
            filename = name
            print(name)
            play = requests.get(url)
            filepath = "./texts/" + filename[:-1] + ".xml"
            with open(filepath, "w", encoding="utf8") as outfile:
                outfile.write(play.text)

def main(file):
    get_obvil(file)

main("obvil_names.txt")
