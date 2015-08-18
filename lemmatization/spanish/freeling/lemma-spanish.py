# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 17:09:44 2015

@author: jose
"""
import subprocess
import os
import glob
import re

#subprocess.call ('analyze -f es.cfg <'+path+file+'.xml  >/home/jose/CLiGS/pruebas-lemma/ne0043pos.txt', shell=True)

def deleteHeader(content):
    content = re.sub(r'<teiHeader>.*?</teiHeader>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    return content

def deleteFrontBack(content):
    content = re.sub(r'<front>.*?</front>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'<back>.*?</back>', r'', content, flags=re.DOTALL|re.IGNORECASE)
    return content

def deleteTags(content):
    content = re.sub(r'<[^>]*?>', r' ', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'[\r\n]+[ \t]*', r'\r\n', content, flags=re.DOTALL|re.IGNORECASE)
    content = re.sub(r'[\r\n]+', r'\r\n', content, flags=re.DOTALL|re.IGNORECASE)
    return content
    

def lemmatizeText(inpath):
    print("inpath: "+inpath)
    os.chdir(inpath)

    #1. The programs takes a path of import, of export and a format
    for file in glob.glob(""+inpath+"0-input/*.xml"):
        pathname=os.path.basename        
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname=fullfilename[:-4]
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            content=deleteHeader(content)
            content=deleteFrontBack(content)
            content=deleteTags(content)
            with open (inpath+'1-plaintext/'+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)

        subprocess.call ('analyze -f es.cfg <'+inpath+'1-plaintext/'+basicname+'.txt  >'+inpath+'2-pos/'+basicname+'.txt', shell=True)

lemmatizeText("/home/jose/CLiGS/toolbox/lemmatization/spanish/freeling/")

