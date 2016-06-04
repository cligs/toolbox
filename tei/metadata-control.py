# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 15:29:35 2016

@author: jose
"""
import glob
import os
import re
dwinput="/home/jose/CLiGS/toolbox/tei/master/"
dwoutput="/home/jose/CLiGS/toolbox/tei/master2/"


print(dwinput)
def main(dwinput):
    betaMetadata=[
    "subgenre-lithist",
    "group-text",
    "representation",
    "author-text-relation"
    "text-movement",

    "protagonist-age",
    "protagonist-name",
    "protagonist-profession",
    "protagonist-social-level",

    "setting-continent",
    "setting-country",
    "setting-name",
    "setting-territory",
    
    "time-period",
    "time-span",

    "type-end",
    ]
    #beta-metadata=["author-text-relation","group-text","protagonist-age","protagonist-name","protagonist-profession","protagonist-social-level","representation","setting-continent","setting-country","setting-name","setting-territory","subgenre-lithist","text-movement","time-period","time-span","type-end"]
    for doc in glob.glob(dwinput+"*.xml"):
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc,extesiondoc= os.path.basename(doc).split(".")
        print(basenamedoc)
    
        with open(doc, "r", errors="replace", encoding="utf-8") as text:
            text = text.read()
            for betaMetadatum in betaMetadata:
                searchMetaDatum=re.findall("<term type=\""+betaMetadatum+"\"",text)
                if not searchMetaDatum:
                    print(betaMetadatum)
                    #Por lo visto el problema está aquí: no sé poner una variable dentro de unl intercambio que tiene que hacer en la expresión regular
                    text = re.sub(r"(</keywords>)", r"\t\t\t\t\t<term type=\""+betaMetadatum+"\"></term>\n\1", text)
                    print(text)
                    with open (os.path.join(dwoutput, basenamedoc+extesiondoc), "w", encoding="utf-8") as fout:
                        fout.write(text)

          

main(dwinput)
