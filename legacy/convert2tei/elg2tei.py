#!/usr/bin/env python3
# Filename: elg2tei.py

"""
# Function to transform html files from ELG into simple, clean TEI files.
"""

import re
import glob
import os


#######################
# Functions           #
#######################

def elg2tei(file,teiheader):
    with open(file,"r") as sourcefile:
        h_text = sourcefile.read()
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        print("Now working on: ", textname)


        #######################################################
        #### Preliminary text preparation                  ####
        #######################################################

        # Remove troublemakers

        h_text = re.sub("<hr />","",h_text)
        h_text = re.sub("<p>À propos de cette édition électronique du groupe « Ebooks libres et gratuits »</p>","",h_text)
        h_text = re.sub("<p>À PROPOS DE CETTE ÉDITION ÉLECTRONIQUE</p>","<p>À propos de cette édition électronique</p>", h_text) 
        
        
        #################################################################
        #### Segmentation into: header, front, body, back, finale.   ####
        #################################################################

        h_header = re.match("<p>[^<]*?</p>\n<p>[^<]*?</p>\n<p>[^<]*?</p>\n<p>[^<]*?</p>\n<p>[^<]*?</p>", h_text, re.DOTALL)
        if h_header: 
            h_header = h_header.group(0)
        else: 
            print("Error with header:", textname)
        #print("\n" + textname)
        #print(h_header)

        h_body = re.match("<p>.*</p>\n<p>À propos.*?</p>", h_text, re.DOTALL)
        if h_body:
            h_body = h_body.group(0)
            h_body = re.sub("\n<p>À propos de cette édition électronique</p>","", h_body)
        else: 
            print("Error with body:", textname)
        #print("\n" + textname)
        #print(h_body)

        h_back = re.search("<p>À propos de cette édition électronique</p>.*", h_text, re.DOTALL)
        h_back = h_back.group(0)
        #print("\n" + textname)
        #print(h_back)

        t_finale = "</text></TEI>"


        ##########################################################################################
        #### Work on the separate text segments                                               ####
        ##########################################################################################

        #################
        #### header  ####
        #################

        # Read empty header
        with open(teiheader,"r") as infile:
            t_header = infile.read()

        # Identify and add publication date
        date_stmt = re.findall("<p>\([\d]{4}\)</p>",h_header)
        if len(date_stmt) > 0:
            date_stmt = date_stmt[0]
            date_stmt = date_stmt[4:-5]
            #print(date_stmt)
        else:
            date_stmt = "n.av."
        t_header = re.sub("<date>first</date>", "<date>" + date_stmt + "</date>", t_header)
        
        # Identify and add author name
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        index = textname.find('_')
        author_name = textname[:index]
        t_header = re.sub("<idno type=\"cligs\">author</idno>", "<idno type=\"cligs\">" + author_name + "</idno>", t_header)

        # Identify and add short title
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        index = textname.find('_')
        short_title = textname[index+1:]
        t_header = re.sub("<title type=\"short\"></title>", "<title type=\"short\">" + short_title + "</title>", t_header)


        #################
        #### front   ####
        #################


        #################
        #### body    ####
        #################

        # Call it t_body from now
        t_body = h_body

        # Initial and final body tags.
        t_body = "<body>\n<div>\n" + t_body + "\n</div>\n</body>"

        # Identify and mark chapter headings, including divisions
        t_body = re.sub("<p>([IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>(Chapitre [IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>([0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>(Chapitre [0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        # If there is such a thing, mark prefaces
        t_body = re.sub("<p>Préface</p>", "</div><div><head>Préface</head>", t_body)


        #################
        #### back    ####
        #################

        t_back = "\n<back><div>\n<p></p>\n</div></back>\n" + h_back
        
        digital_date = re.search("\d\d\d\d", t_back)
        digital_date = digital_date.group(0)
        #print(digital_date)
        
        t_header = re.sub("<date>digital</date>", "<date>" + digital_date + "</date>", t_header)

        #################
        #### finale  ####
        #################

        t_finale = t_finale
        
        

        ####################################################################
        #### Putting all the separate parts of the text into one        ####
        ####################################################################


        ### Concatenate the separate parts of the text into one.
        t_text = t_header + t_body + t_back + t_finale

        ### Save complete text to new file
        filename = os.path.basename(file)[:-5] + ".xml"
        with open("./tei/" + filename,"w") as outputfile:
            outputfile.write(t_text)


       


#######################
# Main                #
########################


def main(inputpath,teiheader):
    for file in glob.glob(inputpath):
        elg2tei(file,teiheader)

main('./html/*.html', "teiHeader.xml")

