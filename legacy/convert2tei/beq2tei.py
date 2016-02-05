#!/usr/bin/env python3
# Filename: beq2tei.py

"""
# Function to transform html files from BEQ into simple, clean TEI files.
"""

import re
import glob
import os


#######################
# Functions           #
#######################

def beq2tei(file,teiheader):
    with open(file,"r") as sourcefile:
        h_text = sourcefile.read()
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        print("Now working on: ", textname)


        #######################################################
        #### Preliminary text preparation                  ####
        #######################################################

        # Remove troublemakers

        h_text = re.sub("<hr />","<p>***</p>",h_text)
         
        #################################################################
        #### Segmentation into: header, front, body, back, finale.   ####
        #################################################################

        h_header = re.match("<p>[^#]*?<ol ", h_text, re.DOTALL)
        if h_header: 
            h_header = h_header.group(0)
        else: 
            print("Error with header:", textname)
        #print("\n" + textname)
        #print(h_header)


        h_body = re.match(".*</ol>\n(.*)<p>Cet ouvrage est le ", h_text, re.DOTALL)
        if h_body:
            h_body = h_body.group(1)
            h_body = str(h_body)
            #print(h_body[-200:])
        else: 
            print("Error with body:", textname)

        t_back = "<back><div>\n<p></p>\n</div></back>"

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
        
        #################
        #### front   ####
        #################


        #################
        #### body    ####
        #################
        
        # Call it t_body from now
        t_body = h_body

        # Initial and final body tags.
        t_body = "<body>\n<div>\n" + str(t_body) + "\n</div>\n</body>"


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

        t_back = t_back 

        
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
        with open("./tei_beq/" + filename,"w") as outputfile:
            outputfile.write(t_text)


       


#######################
# Main                #
########################


def main(inputpath,teiheader):
    for file in glob.glob(inputpath):
        beq2tei(file,teiheader)

main('./html_proust/*.html', "teiHeader.xml")

