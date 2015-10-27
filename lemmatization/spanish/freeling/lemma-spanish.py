# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 17:09:44 2015

@author: jct
"""

"""
    This script lemmatize in different flavours spanish text using Freeling. In order to use it, you have to have
    Freeling running in your computer. Good luck installing it. May the the gods be kind with you.
    
"""

# We call some libraries that we are going to need
import subprocess
import os
import glob
import re

# Definition of some basic functions
# The next three functions make a clean plain text version of the TEI, deliting teiHeader, front and back and all the tags
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

# The next function deletes the first (token), the second (lemma) and the last (probability) of the freeling document
def savePOS(content):
    # The following regular expression deletes the first column, the second, it keeps the third column (which have to be somethin)
    content = re.sub(r'[^\s]+? [^\s]+? ([^\s]+?) [\.0-9]+', r'\1', content,  flags=re.IGNORECASE)
    return content

#  This function keeps the first letter of the third column of the Freeling
def saveVerySimplePOS(content):
    content = re.sub(r'([^\s])[^\s]+', r'\1', content,  flags=re.IGNORECASE)
    return content

#  This function keeps the two first letters of the third column of the Freeling
def saveSimplePOS(content):
    content = re.sub(r'([^\s][^\s]?)[^\s]*', r'\1', content,  flags=re.IGNORECASE)
    return content

# This function deletes the category of the punctuation
def deletePunctuation(content):
    content = re.sub(r'\nF[^\s]?', r'\n', content,  flags=re.IGNORECASE)
    return content



# The next functions lemmatize the texts that are in the 0-input folder
def lemmatizeText(inpath):
    print("lemmatizazing text from inpath: "+inpath)
    """
    jct: can I delete the next line?
    os.chdir(inpath)
    """
    # For every file in the 0-input folder
    for file in glob.glob(inpath+"0-input/*.*"):

        # The programs takes a path of import, of export and a format
        pathname=os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname=fullfilename[:-4]

        # We open it and read every line
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            # We delete the teiHeader
            content=deleteHeader(content)
            # And the front and back
            content=deleteFrontBack(content)
            # And we delete everything that looks like a tag
            content=deleteTags(content)

            # We save a name for the new document
            plaintextInpath=inpath+'1-plaintext/'
            # If we don't have already a folder called 1-plaintext, we create it
            if not os.path.exists(os.path.dirname(plaintextInpath)):
                os.makedirs(os.path.dirname(plaintextInpath))            
            # And finally we save the document
            with open (plaintextInpath+'/'+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)

        # We create a folder for the POS and if there is not such folder, we create it
        fullPosInpath=inpath+'2-fullPOS/'        
        if not os.path.exists(os.path.dirname(fullPosInpath)):
            os.makedirs(os.path.dirname(fullPosInpath))            
        
        # We call the Freeling to do the magic!
        subprocess.call ('analyze -f es.cfg <'+plaintextInpath+basicname+'.txt  >'+fullPosInpath+basicname+'.txt', shell=True)

def saveVersionsPos(inpath):
    print("Versions of lemmatizationg from: "+inpath)
    #os.chdir(inpath)

    print("Lets get the third column!")
    i=0    
    # For every file in the 2-fullPOS folder
    for file in glob.glob(inpath+"2-fullPOS/*.*"):
        i+=1
        # The programs takes a path of import, of export and a format    
        pathname=os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname=fullfilename[:-4]

        # We open it and read every line
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            # We delete everything, only the POS column not
            content=savePOS(content)

            # We save a name for the new document
            PosInpath=inpath+'3-FullMorphoPOS/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(PosInpath)):
                os.makedirs(os.path.dirname(PosInpath))            
            
            # We save the files
            with open (PosInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)
    # We print the number of files analyzed
    print(i ," files done!")


    # 
    print("Lets make some versions!")
    i=0
    for file in glob.glob(inpath+"3-FullMorphoPOS/*.*"):
        i+=1
        # The programs takes a path of import, of export and a format    
        pathname=os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname=fullfilename[:-4]

        # We open it and read every line
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            # We save only the first letter
            content=saveVerySimplePOS(content)

            # We save a name for the new document
            VerySimplePOSInpath=inpath+'3-VerySimplePOS/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(VerySimplePOSInpath)):
                os.makedirs(os.path.dirname(VerySimplePOSInpath))            
            
            # We save the files
            with open (VerySimplePOSInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)

            # We make a copy of it WITHOUT punctuation (because this is not really a POS)
            content=deletePunctuation(content)
            # We save a name for the new document
            VerySimplePOSwpInpath=inpath+'3-VerySimplePOS-wp/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(VerySimplePOSwpInpath)):
                os.makedirs(os.path.dirname(VerySimplePOSwpInpath))            
            
            # We save the files
            with open (VerySimplePOSwpInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)


        # We open it and read every line
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            # We delete everything, only the POS column not
            content=saveSimplePOS(content)

            # We save a name for the new document
            SimplePOSInpath=inpath+'3-SimplePOS/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(SimplePOSInpath)):
                os.makedirs(os.path.dirname(SimplePOSInpath))            
            
            # We save the files
            with open (SimplePOSInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)

            # We make a copy of it WITHOUT punctuation (because this is not really a POS)
            content=deletePunctuation(content)
            # We save a name for the new document
            SimplePOSwpInpath=inpath+'3-SimplePOS-wp/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(SimplePOSwpInpath)):
                os.makedirs(os.path.dirname(SimplePOSwpInpath))            
            
            # We save the files
            with open (SimplePOSwpInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)
    # We print the number of files analyzed
    print(i ," files done!")



inpath="/home/jose/CLiGS/toolbox/lemmatization/spanish/freeling/"
lemmatizeText(inpath)
saveVersionsPos(inpath)

