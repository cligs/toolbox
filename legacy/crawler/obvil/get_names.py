#!/usr/bin/env python3
# Filename: teireader.py

import re

def get_names(file):
    with open(file, "r") as raw:
        raw = raw.read()
        #print(raw)
        
        names = re.findall("<(.*?)>", raw)
        names = ".xml \n".join(names)
        names = re.sub("/.xml", ".xml", names)
        
        with open("names.txt","w") as outfile:
            outfile.write(names)

def main(file):
    get_names(file)

main("obvil_names.txt")
