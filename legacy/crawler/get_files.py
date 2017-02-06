# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# File: get_files.py
# Author: #cf
# Date: 2017-02-03

"""
Using "requests" to get stuff from the web (in this case, from theatre-classique.fr).
"""

import requests
import re


workdir = "/media/christof/data/repos/cligs/theatre-classique-private/"
baseurl = "http://www.theatre-classique.fr/pages/documents/"
listfile = workdir + "list-of-files_2017-02.html"
targetfolder = workdir + "tei4_2017-02"


def read_html(listfile):
    with open(listfile, "r") as infile:
        htmllist = infile.read()
        print(htmllist)
        return htmllist




def main(listfile, baseurl, targetfolder):
    print("Starting...")
    htmllist = read_html(listfile)
    #idlist = get_idlist(htmllist)
    #for id in idlist:
    #    xmlfile = request_file(baseurl, id)
    #    save_file(xmlfile, targetfolder)


main(listfile, baseurl, targetfolder)






"""
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
"""