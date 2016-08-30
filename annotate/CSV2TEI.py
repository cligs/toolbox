# -*- coding: utf-8 -*-
"""
This script places as metadata some values from a CSV file.

The script was written for a specific task; for new tasks, the script should be modified more than just changing the parameters.

Created on Tue Aug 30 07:01:49 2016

@author: jose
"""

import pandas as pd
import re
import glob
import os
import numpy as np


def main(basic_wdir, input_wdir, output_wdir, csv_wdir):
    """
    This is the main and only function. To use it:
    
    tablita = main("/home/jose/cligs/ne/","master/*.xml", "master2/", "/home/jose/cligs/ne/autores.csv")
    
    """
    # First the table is opened
    df_data = pd.read_csv(csv_wdir, encoding="utf-8", sep="\t")
    #print(df_data)
    
    # The we open each file
    for doc in glob.glob(basic_wdir+input_wdir):
        idno_file = os.path.basename(doc)
        #print(idno_file)
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            
            # We take the author of the text (we take the author and not the id because we want to place in the file information about the author)            
            author = re.findall(r'<author>\s+<idno type=".*?</idno>\s+<name type="short">(.*?)</name>', content)[0]
            print(author)

            # Now we save in variables the different information that we have in the CSV

            # First we take the information about the volume where the author is treated and from that we take the information about the prefered genre and the period
            volumen = str(int(df_data.loc[df_data['Nombre corto'] == author]['Volumen de Manual'].values))
            print(volumen)            
            if volumen == "7" or volumen == "9" or volumen == "10":
                genre = "prose"
            elif volumen == "8" or volumen == "11" or volumen == "12" or volumen == "13":
                genre = "poetry"

            if volumen == "7":
                period = "realism_naturalism"
            elif volumen == "8" or volumen == "9":
                period = "modernism_gen98"
            elif volumen == "10" or volumen == "11":
                period = "novencentismo_gen27"
            elif volumen == "12" or volumen == "13":
                period = "postwar"
                

            # Than we take all the information about birth, death, range_toc and pages:                
            birth = str(int(df_data.loc[df_data['Nombre corto'] == author]['Nacimiento'].values))

            death = str(int(df_data.loc[df_data['Nombre corto'] == author]['Muerte'].values))

            range_toc = str(int(df_data.loc[df_data['Nombre corto'] == author]['Range'].values))

            pages = str(int(df_data.loc[df_data['Nombre corto'] == author]['Amount pages'].values))
            
            # Finally, we put with a regex all the information where we want to place it (after the element <term type="author-gender">)
            content = re.sub(r'(<term type="author-gender">.*?</term>)', r'\1\n\t\t\t\t\t<term type="author-date-birth">'+re.escape(birth)+r'</term>\n\t\t\t\t\t<term type="author-date-death">'+re.escape(death)+r'</term>\n\t\t\t\t\t<term type="author-TOC-range" resp="MdL'+re.escape(volumen)+'">'+re.escape(range_toc)+r'</term>\n\t\t\t\t\t<term type="author-histlit-pages" resp="MdL'+re.escape(volumen)+r'">'+re.escape(pages)+r'</term>\n\t\t\t\t\t<term type="author-movement">'+re.escape(period)+r'</term>\n\t\t\t\t\t<term type="author-prefered-genre">'+re.escape(genre)+r'</term>', content)

            with open (os.path.join(basic_wdir+output_wdir, idno_file), "w", encoding="utf-8") as fout:
                fout.write(content)
    return df_data       
    
#tablita = main("/home/jose/cligs/ne/","master/*.xml", "master2/", "/home/jose/cligs/ne/autores.csv")