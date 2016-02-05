# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: upgrade_header.py

"""
# Function to replace old teiHeader by new one.
"""

import re
import glob
import os


def upgrade_header(file,teiheader, outdir):
    with open(file,"r") as sourcefile:
        odocument = sourcefile.read()
        basename = os.path.basename(file)
        idno, ext = os.path.splitext(basename)
        print("Now working on: " + str(idno))
        
        ## Separate into header and rest
        oheader = re.findall("<?xml(?s).*</teiHeader>", odocument, re.DOTALL)
        oheader = str(oheader)
        #print(textname, oheader)
        otext = re.findall("<text>(?s).*</TEI>", odocument, re.DOTALL)
        otext = str(otext)
        #print(textname, otext)

        ## Read empty header
        with open(teiheader,"r") as infile:
            eheader = infile.read()
            #print(eheader)

        ## Identify data in oheader 
        title_main = re.findall(r'<title>([^<]*?)</title>', oheader)
        if title_main:
            title_main = str(title_main[0])
        else: 
            title_main = re.findall(r'<title type="main">([^<]*?)</title>', oheader)
            title_main = str(title_main[0])
        #print(title_main)

        title_short = re.findall(r'<idno type="label">([^<]*?)</idno>', oheader)
        if title_short:             
            title_short = str(title_short[0])
            title_short = re.split("_", title_short)[1]
        else: 
            title_short = re.findall(r'<title type="short">([^<]*?)</title>', oheader)
            if title_short: 
                title_short = str(title_short[0])
            else: 
                title_short = title_main
        #print(title_short)
        
        author_full = re.findall(r'<author>([^<]*?)</author>', oheader)
        author_full = str(author_full[0])
        #print(author_full)

        author_short = re.findall(r'<idno type="label">([^<]*?)</idno>', oheader)
        if author_short: 
            author_short = str(author_short[0])
            author_short = re.split("_", author_short)[0]
        else: 
            author_short = author_full
        #print(author_short)
        
        availability_status = re.findall(r'<licence>([^<]*?)</licence>', oheader)
        if availability_status:
            availability_status = str(availability_status[0])
            if availability_status == "Public domain." or availability_status == "Public domain": 
                availability_status = "publicdomain"
            else:
                availability_status = "restricted"
        else: 
            availability_status = "n.av."
        #print(availability_status)
        
        date_first = re.findall(r'<p>First published:(.*?)</p>', oheader, re.DOTALL)
        if date_first:
            date_first = str(date_first[0])
        else: 
            date_first = "n.av."
        #print(date_first)

        source_digital = re.findall(r'<p>Source:(.*?)</p>', oheader, re.DOTALL)
        if source_digital:
            source_digital = str(source_digital[0])
        else: 
            source_digital = "n.av."
        #print(source_digital)

        change = re.findall(r'(<change when="[0-9|-]*?" who="#cf">[^<]*?</change>)', oheader)
        if change:
            change = str(change[0])
        else:
            change = '<change when="2015-01-01" who="#cf">Initial TEI version.</change>'
        #print(change)
                
        ## Write identified data into eheader
        eheader = re.sub('<title type="main"></title>','<title type="main">'+title_main+'</title>',eheader)        
        eheader = re.sub('<title type="short"></title>','<title type="short">'+title_short+'</title>',eheader)        
        eheader = re.sub('<name type="short"></name>','<name type="short">'+author_short+'</name>',eheader)        
        eheader = re.sub('<name type="full"></name>','<name type="short">'+author_full+'</name>',eheader)        
        eheader = re.sub('<availability status="">','<availability status="'+availability_status+'">',eheader)        
        eheader = re.sub('<idno type="cligs"></idno>','<idno type="cligs">'+idno+'</idno>',eheader)         
        eheader = re.sub('</revisionDesc>',"                "+change+"\n                </revisionDesc>",eheader)        
        eheader = re.sub('<bibl type="edition-first">\n.*?<date></date>','<bibl type="edition-first"><date>'+date_first+'</date>',eheader)   
        eheader = re.sub('<bibl type="digital-source">\n.*?<date></date>','<bibl type="edition-first"><date>'+source_digital+'</date>',eheader)
        nheader = eheader
        #print(nheader)
        

        ### Concatenate new header and text
        ndocument = odocument
        ndocument = re.sub("<?xml(?s).*</teiHeader>",nheader,odocument)   
        ndocument = re.sub("<\?<\?", "<\?", ndocument)
        ndocument = re.sub("<hi","<seg",ndocument)
        ndocument = re.sub("</hi>","</seg>",ndocument)
        
 
        ### Save complete text to new file
        filename = basename
        with open(outdir + filename,"w") as outputfile:
            outputfile.write(ndocument)


def main(inputpath, teiheader, outdir):
    for file in glob.glob(inputpath):
        upgrade_header(file, teiheader, outdir)

main("./master/rf1*.xml", "teiHeader.xml", "./newheader/")

