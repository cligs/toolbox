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
def cleaning(content):
    content = re.sub(r' ', r' ', content, flags=re.DOTALL|re.IGNORECASE)
    
    return content

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
    content = re.sub(r'^.+? .+? (.+?) [\.0-9]+$', r'\1', content,  flags=re.I|re.M)
    return content

#  This function keeps the first letter of the third column of the Freeling
def saveVerySimplePOS(content):
    content = re.sub(r'^(.).*?$', r'\1', content,  flags=re.I|re.M)
    return content

#  This function keeps the two first letters of the third column of the Freeling
def saveSimplePOS(content):
    content = re.sub(r'^(..?).*?$', r'\1', content,  flags=re.I|re.M)
    return content

# This function deletes the category of the punctuation
def deletePunctuation(content):
    content = re.sub(r'^f.*?$', r'\n', content,  flags=re.I|re.M)
    return content

# This function deletes the category of the punctuation
def deleteNonPunctuation(content):
    content = re.sub(r'^[^f][a-z0-9]*$', r'', content,  flags=re.I|re.M)
    return content

"""
    The next function delete one category from the column
"""

def deleteAdjectiveColumn(content):
    content = re.sub(r'^a.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteAdverbColumn(content):
    content = re.sub(r'^r.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteDeterminantColumn(content):
    content = re.sub(r'^d.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteNameColumn(content):
    content = re.sub(r'^n.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteVerbColumn(content):
    content = re.sub(r'^v.*$', r'', content,  flags=re.I|re.M)
    return content

def deletePronounColumn(content):
    content = re.sub(r'^p.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteInterjectionColumn(content):
    content = re.sub(r'^i.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteConjuctionColumn(content):
    content = re.sub(r'^c.*$', r'', content,  flags=re.I|re.M)
    return content

def deletePrepositionColumn(content):
    content = re.sub(r'^s.*$', r'', content,  flags=re.I|re.M)
    return content

def deletePunctuationColumn(content):
    content = re.sub(r'^f.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteNumbersColumn(content):
    content = re.sub(r'^z.*$', r'', content,  flags=re.I|re.M)
    return content

def deleteTimeColumn(content):
    content = re.sub(r'^w.*$', r'', content,  flags=re.I|re.M)
    return content


# The next function deletes the column for non personal verbs like infinitivos, participios and gerundios
def deleteNonPersonalVerbs(content):
    content = re.sub(r'^v...0.+$', r'', content,  flags=re.I|re.M)
    return content

# The next function deletes the column for pronouns withouth information from the person
def deleteNonPersonalPronouns(content):
    content = re.sub(r'^p.0.+$', r'', content,  flags=re.I|re.M)
    return content


# The next function deletes everything from verbs and pronouns, only leaving the person
def leavesOnlyPersonVerbsPronouns(content):
    content = re.sub(r'^v...(..).+$', r'\1', content,  flags=re.I|re.M)
    content = re.sub(r'^p.(.).(.).+$', r'\1\2', content,  flags=re.I|re.M)
    return content

#  This function keeps the first letter of the third column of the Freeling
def savePersonFromVerb(content):
    content = re.sub(r'v...([1-3][SP]).', r'\1', content,  flags=re.I|re.M)
    return content

#  This function keeps the first letter of the third column of the Freeling
def changeNumberToText(content):
    content = re.sub(r'1', r'First', content,  flags=re.I|re.M)
    content = re.sub(r'2', r'Second', content,  flags=re.I|re.M)
    content = re.sub(r'3', r'Third', content,  flags=re.I|re.M)
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
            content=cleaning(content)

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
        fullPosInpath=inpath+'2-fullMorphoPOS/'        
        if not os.path.exists(os.path.dirname(fullPosInpath)):
            os.makedirs(os.path.dirname(fullPosInpath))            
        
        # We call the Freeling to do the magic!
        subprocess.call ('analyze -f es.cfg <'+plaintextInpath+basicname+'.txt  >'+fullPosInpath+basicname+'.txt', shell=True)

def saveVersionsPos(inpath):
    print("Versions of lemmatizationg from: "+inpath)
    #os.chdir(inpath)

    pathMorpho=inpath+"3-MorphoPOS/"
    print("Lets get the third column!")
    i=0    
    # For every file in the 2-fullPOS folder
    for file in glob.glob(inpath+"2-fullMorphoPOS/*.*"):
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
            PosInpath=pathMorpho+'all/'
            # If we don't have already a folder, we create it
            if not os.path.exists(os.path.dirname(PosInpath)):
                os.makedirs(os.path.dirname(PosInpath))            
            
            # We save the files
            with open (PosInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(content)
    # We print the number of files analyzed
    print(i ," files done!")


    # We make versions of everything
    print("Lets make some versions!")
    i=0
    for file in glob.glob(pathMorpho+"all/*.*"):
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

            """
                The following blocks of code create a version of the information from Freeling
                1 - It takes some content and modifies it somehow
                2 - It creates some folder if it doesn't exist
                3 - It saves the text somewhere
            """
 
            # This one keeps only the first letter            
            contentVerySimplePOS=saveVerySimplePOS(content)
            OneLetterInpath=pathMorpho+'1Letter/'
            if not os.path.exists(os.path.dirname(OneLetterInpath)):
                os.makedirs(os.path.dirname(OneLetterInpath))            
            with open (OneLetterInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(contentVerySimplePOS)



            # This one keeps only the first letter WITHOUT punctuation (because this is not really a POS)
            contentVerySimplePOSwp=deletePunctuation(contentVerySimplePOS)
            OneLetterNoPunctInpath=pathMorpho+'1LetterNoPunct/'
            if not os.path.exists(os.path.dirname(OneLetterNoPunctInpath)):
                os.makedirs(os.path.dirname(OneLetterNoPunctInpath))            
            with open (OneLetterNoPunctInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(contentVerySimplePOSwp)


            # This one keeps only the two first letters
            TwoLetterContent=saveSimplePOS(content)
            TwoLetterInpath=pathMorpho+'2Letter/'
            if not os.path.exists(os.path.dirname(TwoLetterInpath)):
                os.makedirs(os.path.dirname(TwoLetterInpath))            
            with open (TwoLetterInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(TwoLetterContent)


            # This one keeps only the two first letters WITHOUT punctuation
            TwoLetterContentNoPunct=deletePunctuation(TwoLetterContent)
            TwoLetterNoPunctInpath=pathMorpho+'2LetterNoPunct/'
            if not os.path.exists(os.path.dirname(TwoLetterNoPunctInpath)):
                os.makedirs(os.path.dirname(TwoLetterNoPunctInpath))            
            with open (TwoLetterNoPunctInpath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(TwoLetterContentNoPunct)


            # This one keeps only the two first letters FROM the punctuation
            TwoLetterContentOnlyPunct=deleteNonPunctuation(TwoLetterContent)
            TwoLetterContentOnlyPunctPath=pathMorpho+'2LetterOnlyPunct/'
            if not os.path.exists(os.path.dirname(TwoLetterContentOnlyPunctPath)):
                os.makedirs(os.path.dirname(TwoLetterContentOnlyPunctPath))            
            with open (TwoLetterContentOnlyPunctPath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(TwoLetterContentOnlyPunct)


            # This one keeps the person from pronouns and verbs
            PersonVerbsPronounsContent=deleteAdjectiveColumn(content)
            PersonVerbsPronounsContent=deleteAdverbColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteDeterminantColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteNameColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteConjuctionColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteInterjectionColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deletePrepositionColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deletePunctuationColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteNumbersColumn(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteTimeColumn(PersonVerbsPronounsContent)


            PersonVerbsPronounsContent=deleteNonPersonalPronouns(PersonVerbsPronounsContent)
            PersonVerbsPronounsContent=deleteNonPersonalVerbs(PersonVerbsPronounsContent)

            PersonVerbsPronounsContent=leavesOnlyPersonVerbsPronouns(PersonVerbsPronounsContent)

            PersonVerbsPronounsContent=changeNumberToText(PersonVerbsPronounsContent)
            
            
            VerbPronounPersonPath=pathMorpho+'VerbPronounPersonTogether/'
            if not os.path.exists(os.path.dirname(VerbPronounPersonPath)):
                os.makedirs(os.path.dirname(VerbPronounPersonPath))        
            with open (VerbPronounPersonPath+basicname+'.txt', "w", encoding="utf-8") as fout:
                fout.write(PersonVerbsPronounsContent)

    # We print the number of files analyzed
    print(i ," files done!")



inpath="/home/jose/CLiGS/toolbox/lemmatization/spanish/freeling/"
lemmatizeText(inpath)
saveVersionsPos(inpath)

