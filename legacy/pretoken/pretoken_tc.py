# pretoken.py
# Function to prepare text files for lemmatization and POS-tagging with TreeTagger.
# Basically splits hyphenated words apart to make sure TreeTagger doesn't get confused over them.
# Makes use of "re"; see: http://docs.python.org/2/library/re.html


#######################
# Good to know   
#######################

# 1. By default, expects files to be in a subfolder called "in". 
# 2. By default, expects there to be an empty folder called "out" for the output.


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
    """Deletion of unwanted elided and hyphenated words."""
    with open(file,"r") as text:
        text = text.read()                                               
        text = re.sub("’","'",text)                                   
        text = re.sub("J'","Je ",text)                                   
        text = re.sub("j'","je ",text)                                   
        text = re.sub("S'","Se ",text)                                   
        text = re.sub("s'","se ",text)                                   
        text = re.sub("C'","Ce ",text)                                   
        text = re.sub("c'","ce ",text)                                   
        text = re.sub("N'","Ne ",text)                                   
        text = re.sub("n'","ne ",text)                                   
        text = re.sub("D'","De ",text)                                   
        text = re.sub("d'","de ",text)                                   
        text = re.sub("L'","Le ",text)                                
        text = re.sub("l'","la ",text)                                
        #text = re.sub("T'","T ",text)                                   
        #text = re.sub("t'","t ",text)                                   
        text = re.sub("-le"," le",text)                                  
        text = re.sub("-moi"," moi",text)                                  
        text = re.sub("m'","me ",text)                                  
        text = re.sub("M'","Me ",text)                                  
        text = re.sub("-je"," je",text)                                  
        text = re.sub("-il"," il",text)                                  
        text = re.sub("-on"," on",text)                                  
        text = re.sub("-lui"," lui",text)                                  
        text = re.sub("-elle"," elle",text)                              
        text = re.sub("-nous"," nous",text)                              
        text = re.sub("-vous"," vous",text)                              
        text = re.sub("-nous"," nous",text)                            
        text = re.sub("-ce"," ce",text)                                  
        text = re.sub("-tu"," tu",text)                                      
        text = re.sub("-toi"," toi",text)                                      
        text = re.sub("jusqu'à'","jusque à",text)                                      
        #text = re.sub("aujourd'hui","aujourdhui",text)                                      
        text = re.sub("-t","",text)                                      
        text = re.sub("-y"," y",text)                                      
        text = re.sub("-en"," en",text)                                      
        text = re.sub("-ci"," ci",text)                                      
        text = re.sub("-là"," là",text)                                      
        #text = re.sub("là-bas","là bas",text)                                      
        text = re.sub("Qu'","Que ",text)                                      
        text = re.sub("qu'","que ",text)                                      
        #text = re.sub("-même"," même",text)
        basename = os.path.basename(file)                                
        cleanfilename = basename[:-4] + ".txt"                           
        print(cleanfilename)
    with open(os.path.join(output_dir, cleanfilename),"w") as output:    
        output.write(text)                  


#######################
# Main                #
#######################


def main(inputpath,output_dir):
    for file in glob.glob(inputpath):
        clean_txt(file,output_dir)
            
main('./in/*.txt','./out/')

