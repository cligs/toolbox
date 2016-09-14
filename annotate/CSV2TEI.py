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


def metadata_from_author(basic_wdir, input_wdir, output_wdir, csv_wdir):
    """
    This is the main and only function. To use it:
    
    tablita = metadata_from_author("/home/jose/cligs/ne/","master/*.xml", "master2/", "/home/jose/cligs/ne/authors-from-cataloge.csv")
    
    """
    # First the table is opened
    df_data = pd.read_csv(csv_wdir, encoding="utf-8", sep="\t")
    #print(df_data)
    
    # The we open each file
    for doc in glob.glob(basic_wdir+input_wdir):
        idno_file = os.path.basename(doc)
        print(idno_file)
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            
            # We take the author of the text (we take the author and not the id because we want to place in the file information about the author)            
            author = re.findall(r'<author>\s+<idno type=".*?</idno>\s+<name type="short">(.*?)</name>', content)[0]
            print(author)

            # We delete the items if they were there
            content = re.sub(r'(\s+<term type="author-movement">.*?</term>)', r'', content)    
            content = re.sub(r'(\s+<term type="author-prefered-genre">.*?</term>)', r'', content)    

            # Now we save in variables the different information that we have in the CSV

            # Than we take all the information about birth, death, range_toc and pages:                
            author_movement = df_data.loc[df_data['short-name'] == author]['author-movement'].values[0]
            author_submovement = df_data.loc[df_data['short-name'] == author]['author-submovement'].values[0]
            non_novel_genre = df_data.loc[df_data['short-name'] == author]['non-novel-genre'].values[0]

            
            # Finally, we put with a regex all the information where we want to place it (after the element <term type="author-gender">)
            content = re.sub(r'(<term type="author-gender">.*?</term>)', r'\1\n\t\t\t\t\t<term type="author-movement">' + author_movement + r'</term>\n\t\t\t\t\t<term type="author-submovement">' + author_submovement + r'</term>\n\t\t\t\t\t<term type="non-novel-genre">' + non_novel_genre + r'</term>', content)

            with open (os.path.join(basic_wdir+output_wdir, idno_file), "w", encoding="utf-8") as fout:
                fout.write(content)
    return df_data       

    
tablita = metadata_from_author("/home/jose/cligs/ne/","master/*.xml", "master2/", "/home/jose/cligs/ne/authors-from-cataloge.csv")
    

def metadata_from_text(basic_wdir, input_wdir, output_wdir, csv_wdir):
    """
    This is the main and only function. To use it:
    
    tablita = metadata_from_text("/home/jose/cligs/ne/","master/*.xml", "master2/", "/home/jose/cligs/ne/texts-from-cataloge.csv")
    
    """
    # First the table is opened
    df_data = pd.read_csv(csv_wdir, encoding="utf-8", sep="\t")
    #print(df_data)
    
    # The we open each file
    for doc in glob.glob(basic_wdir+input_wdir):
        idno_file = os.path.basename(doc)
        print(idno_file)
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
            
            # We take the author of the text (we take the author and not the id because we want to place in the file information about the author)            
            id_ = re.findall(r'<idno\s+type="cligs">(.*?)</idno>', content)[0]
            #print(id_)

            # We delete the items if they were there
            content = re.sub(r'(\s+<term type="text-movement">.*?</term>)', r'', content)    

            # Now we save in variables the different information that we have in the CSV

            # Than we take all the information about birth, death, range_toc and pages:                
            text_movement = df_data.loc[df_data['id'] == id_]['text-movement'].values[0]
            text_histlit_pages = str(df_data.loc[df_data['id'] == id_]['text-histlit-pages'].values[0])



            # Finally, we put with a regex all the information where we want to place it (after the element <term type="author-gender">)
            content = re.sub(r'(\s+</keywords>)', r'\n\t\t\t\t\t<term type="text-movement">' + text_movement + r'</term>\n\t\t\t\t\t<term type="text-histlit-pages">' + text_histlit_pages + r'</term>\1', content)

            with open (os.path.join(basic_wdir+output_wdir, idno_file), "w", encoding="utf-8") as fout:
                fout.write(content)
    return df_data


tablita = metadata_from_text("/home/jose/cligs/ne/","master2/*.xml", "master3/", "/home/jose/cligs/ne/texts-from-cataloge.csv")