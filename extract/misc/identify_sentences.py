# ./bin/env python3
# identify_sentences.py

"""
# Script to identify and mark up sentences in French prose texts available as XML-TEI.
# Version 0.1, 18.5.2015, by #cf.
"""

import re
import glob
import os

def identify_sentences(file):
    """Identify and mark up sentences."""
    basename = os.path.basename(file)
    textname, ext = os.path.splitext(basename)
    #print(textname)

    with open(file, "r") as file:
        document = file.read()
        document = str(document)
        #print(document)

        ### Gets header as string
        result = re.search(r"(<\?xml[^$]*?</teiHeader>)", document, re.DOTALL)
        if result:
            header = result.group(0)
            #print(header,"\n")
        else:
            print("There is an error. No header was found.")
        
        ### Gets text as string
        result = re.search(r"(<text[^$]*?</TEI>)", document, re.DOTALL)
        if result: 
            text = result.group(0)
            #print(text,"\n")
        else:
            print("There is an error. No text was found.")

            ### Preprocessing
            text = re.sub("<hi rend=\"italic\">","",text)
            text = re.sub("<hi rend=\"bold\">","",text)
            text = re.sub("<hi>","",text)
            text = re.sub("</hi>","",text)



            ### Identify and mark up sentences boundaries
            ## At paragraph boundaries (pairs)
            text = re.sub("<p>","<p><s>",text)
            text = re.sub("</p>","</s></p>",text)
            text = re.sub("<said>","<said><s>",text)
            text = re.sub("</said>","</s></said>",text)
            ## Classical sentence boundaries
            text = re.sub("([a-z|é]\. )([A-Z])","\\1</s><s>\\2",text)
        
            newdocument = header + text
            outtext = str(newdocument)
            outfile = "./outfolder/" + textname + "_s.xml"
            with open(outfile,"w") as output:
                output.write(outtext)


         

def main(inpath):
    numberoffiles = 0
    for file in glob.glob(inpath):
        identify_sentences(file)
        numberoffiles +=1
    print("Done. Number of files treated: " + str(numberoffiles))



main('./infolder/*.xml')
