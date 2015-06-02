# cleanutf8.py
# Function to clean-up XML files converted from ISO-8859-15 to UTF-8 that have funny stuff in them.
# Makes use of "re"; see: http://docs.python.org/2/library/re.html


#######################
# Good to know   
#######################

# 1. By default, expects files to be in a subfolder called "sth" and files end in ".xml.utf8". 
# 2. By default, expects there to be an empty folder called "utf8" for the output.


#######################
# Import statements   
#######################

import re
import os
import glob


#######################
# Functions           
#######################

def clean_txt(file,output_dir):
    with open(file,"r") as text:
        text = text.read()   
        # Basic stuff for all files
        text = re.sub(r'iso-8859-1',r'UTF-8',text)  
        text = re.sub(r'\r\n',r'\n',text)  
        text = re.sub(r'\r\n',r'\n',text)  
        
        # Some files have funny stuff.
        text = re.sub(r'Ã',r'É',text)  
        text = re.sub(r'Ã©',r'é',text)  
        text = re.sub(r'Ã§',r'ç',text)  
        text = re.sub(r'Ãš',r'è',text)  
        text = re.sub(r'Ã¢',r'â',text)  
        text = re.sub(r'Ã',r'È',text)  
        text = re.sub(r'Ã',r'Ê',text)  
        text = re.sub(r'Ãª',r'ê',text)  
        text = re.sub(r'Ã®',r'î',text)  
        text = re.sub(r'Ã¹',r'ù',text)  
        text = re.sub(r'ÃŽ',r'ô',text)  
        text = re.sub(r'Ã',r'À',text)  
        text = re.sub(r'Ã ',r'à',text)  
        text = re.sub(r'Ã»',r'û',text)  
        text = re.sub(r'Ã¯',r'ï',text)  
        text = re.sub(r'Ã',r'Ô',text)  
        text = re.sub(r'',r"'",text)  
        text = re.sub(r'',r"?",text)  
        text = re.sub(r'',r"œ",text)  

        basename = os.path.basename(file)    
        newfilename = basename  
        print(newfilename)
    with open(os.path.join(output_dir, newfilename),"w") as output:  
        output.write(text)                  


#######################
# Main                #
#######################


def main(inputpath,output_dir):
    for file in glob.glob(inputpath):
        clean_txt(file,output_dir)
            
main('./tei/*.xml','./tei2/')

