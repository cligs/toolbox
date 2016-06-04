#!/usr/bin/env python3
# Filename: md2tei.py

"""
# Function to transform html files from Markdown into simple, clean TEI files.
"""

import re
import glob
import os


#######################
# Functions           #
#######################

def md2tei(file,teiheader):
    with open(file,"r") as sourcefile:
        h_text = sourcefile.read()
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        print("Now working on: ", textname)


        #######################################################
        #### Preliminary text preparation                  ####
        #######################################################

        # Remove troublemakers
         
        #################################################################
        #### Segmentation into: header, front, body, back, finale.   ####
        #################################################################

        h_header = h_text[0:5000]
        
        h_body = h_text
        
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


        ## Identify and mark chapter headings, including divisions
        t_body = re.sub("<p>##([IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>##(Chapitre [IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>##([0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>##(Chapitre [0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        t_body = re.sub("<p>#([IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>#(Chapitre [IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>#([0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>#(Chapitre [0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        t_body = re.sub("<p># ([IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># (Chapitre [IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># ([0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># (Chapitre [0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        t_body = re.sub("<p>## \*\*([IVXLMC]{1,5})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>## \*\*(Chapitre [IVXLMC]{1,5})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>## \*\*([0-9]{1,3})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p>## \*\*(Chapitre [0-9]{1,3})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        t_body = re.sub("<p># \*\*([IVXLMC]{1,5})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># \*\*(Chapitre [IVXLMC]{1,5})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># \*\*([0-9]{1,3})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)
        t_body = re.sub("<p># \*\*(Chapitre [0-9]{1,3})\*\*</p>", "</div>\n<div>\n<head>\\1</head>", t_body)

        t_body = re.sub("<p>\n# ([IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body, re.DOTALL, re.MULTILINE)
        t_body = re.sub("<p>\n# (Chapitre [IVXLMC]{1,5})</p>", "</div>\n<div>\n<head>\\1</head>", t_body, re.DOTALL, re.MULTILINE)
        t_body = re.sub("<p>\n# ([0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body, re.DOTALL, re.MULTILINE)
        t_body = re.sub("<p>\n# (Chapitre [0-9]{1,3})</p>", "</div>\n<div>\n<head>\\1</head>", t_body, re.DOTALL, re.MULTILINE)

        
        t_body = re.sub("<p></p>\n","",t_body)
        t_body = re.sub("<p> </p>\n","",t_body)
        t_body = re.sub("<p>[^<]</p>","",t_body)
        
        
        ## Formerly protected spaces; ignore
        t_body = re.sub(r'\\!','!',t_body)
        t_body = re.sub(r'\(','(',t_body)
        
        ## Some md formatting
        t_body = re.sub(r'\*(.*?)\*','<hi rend=\"italic\">\\1</hi>',t_body)
        t_body = re.sub(r'([a-z])<hi rend=\"italic\"> ','\\1 <hi rend=\"italic\">',t_body)
        
       
        
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
        filename = os.path.basename(file)[:-4] + ".xml"
        with open("./md_tei/" + filename,"w") as outputfile:
            outputfile.write(t_text)


       


#######################
# Main                #
########################


def main(inputpath,teiheader):
    for file in glob.glob(inputpath):
        md2tei(file,teiheader)

main('./md/*.txt', "teiHeader.xml")

