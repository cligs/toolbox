# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:35:08 2016

@author: jose
"""
import pandas as pd
import re
import glob
from collections import Counter
from lxml import etree

"""
To use all of them just use:
df = get_all("/home/jose/cligs/ne/master/", "ne0030")
"""


def parse_text(doc):
    # We delimit that we only want to find information in the text() of XML-TEI
    xml = etree.parse(doc)
    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
    xp_bodytext = "//tei:body//text()"
    content = xml.xpath(xp_bodytext, namespaces=namespaces)
    # etree gives us a string where each line a string; but we only want a string:          
    content = ' '.join(content)
    return content

def get_names(wdir, txtFolder):
    """
    This function gives you a dataframe with the proper names (searched with a regexp) found in a file.
    It should be useful to know who the protagonist is, or where the action of the text takes place.
    The regexps are thought for Spanish. In stead of [a-zá-úñüç] we could be using \w if the English speaking comunity had thought that other languages have other characters and our regexp would be much more elegant...

    wdir is the path of the gile
    txtFolder is the name (without format ending) of the file to be analized

    Example of how to use it at the console:
    
    df = get_names("/home/jose/cligs/ne/master/", "ne0002")
    """
    #Lets open the file
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            #We create a list for the names
            names=[]
            # We search for any word that starts with capital letter and that before didn't have anything that looks like an starting of a sentence
            names = re.findall(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+)', content)
            for name in names:
                    name = name.strip()
            #print(names)

            # We delete the duplicated items in the list            
            names=list(set(names))
            #print(names)
            
            # Now we put the list in a data frame
            df=pd.DataFrame(names,columns=["name"])
            #print(df)
            #And we add a new column for the frequency and we fill it with zeros
            df["freq"]=0
            #print(df)

            # Now, for every row, we take the indexes and the other columns with the real values (names and frequency)            
            for index, row in df.iterrows():
                # For each, we fill the frecuency with the the amount (len) of a times that the name appears in the text with something 
                df.at[index,"freq"] = len(re.findall(r'[^a-zá-úçñüA-ZÁ-ÚÜÑ]'+ re.escape(row["name"]) + r'[^a-zá-úçñüA-ZÁ-ÚÜÑ]', content))

            df=df.sort(["freq"], ascending=True)
            # The df is sorted after the frequency
            print(df)
            # The data is printed as a file
            #df.to_csv(wdir+txtFolder+'_ProperNames.csv', sep='\t', encoding='utf-8')
        fin.close()        
        return df

def get_full_names(wdir, txtFolder):
    """

    wdir is the path of the gile
    txtFolder is the name (without format ending) of the file to be analized

    Example of how to use it at the console:
    
    df = get_full_names("/home/jose/cligs/ne/master/", "ne0032")
    """
    #Lets open the file
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()

            # We take only the text            
            content = parse_text(doc)
            
            #We create a list for the places
            fullNames = []


            if re.search(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+(?:(?: de | el | del | de la | |\-)[A-ZÁ-ÚÜÑ][a-zá-úñüç]+)+)', content) is None:
                print("no fullNames found (weird!!!) \n:(\n\n\n")
            else:
                print("\nyey! We found some fullNames :)\n")

                # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
                fullNames = re.findall(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+(?:(?: de | el | del | de la | |\-)[A-ZÁ-ÚÜÑ][a-zá-úñüç]+)+)', content)
                countfullNames = Counter(fullNames)

                dfCountFullNames = pd.DataFrame.from_dict(countfullNames, orient='index').reset_index()
                dfCountFullNames = dfCountFullNames.rename(columns={'index':'Fullname', 0:'freq'})
                dfCountFullNames = dfCountFullNames.sort(["freq"], ascending=True)        
        fin.close()
        print(dfCountFullNames)
    
        return dfCountFullNames

def get_full_names_protagonist(wdir, txtFolder,number):
    """
    This function tries to get the full name of the protagonists
    df = get_full_names_protagonist("/home/jose/cligs/ne/master/", "ne0249",2)
    
        
    """

    names = get_names(wdir, txtFolder)
    #print(names)

    names = names[names['name'].map(len) > 2]

    names = names.tail(n=number)
    print("\n\nMore info about the names: ",names)

    #Lets open the file
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            # We take only the text            
            content = parse_text(doc)
            
            countfullNames = Counter("")
            for name in names.loc[:,"name"]:
                #print(name)
        
                fullNames = []
                fullNames = re.findall(r'(?<=[a-zá-úñüç,;] )(' + re.escape(name) + r'(?:(?: de | el | del | de la | |\-)(?:[A-ZÁ-ÚÜÑ][a-záéíóúñüç]+))+|(?:(?:[A-ZÁ-ÚÜÑ][a-záéíóúñüçñüç]+)(?: de | el | del | de la | |\-)*)+' + re.escape(name) + r'(?:(?: de | el | del | de la | |\-)(?:[A-ZÁ-ÚÜÑ][a-zzáéíóúñüçñüç]+))*)', content)                       
                for fullName in fullNames:
                    fullName = fullName.strip()
                countfullNames = countfullNames+Counter(fullNames)
                #print(countfullNames)
            #print(countfullNames)
            dfCountFullNames = pd.DataFrame.from_dict(countfullNames, orient='index').reset_index()
            dfCountFullNames = dfCountFullNames.rename(columns={'index':'Fullname', 0:'freq'})
            dfCountFullNames = dfCountFullNames.sort(["freq"], ascending=True)        
            print(dfCountFullNames)
        fin.close()
        return dfCountFullNames

def get_places(wdir, txtFolder):
    """

    wdir is the path of the gile
    txtFolder is the name (without format ending) of the file to be analized

    Example of how to use it at the console:
    
    df = get_places("/home/jose/cligs/ne/master/", "ne0002")
    """
    #Lets open the file
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            # We take only the text            
            content = parse_text(doc)
            
            #We create a list for the places
            places = []


            if re.search(r'(?:en|En) ([A-ZÁ-ÚÜÑ][a-zá-úñüç]+)', content) is None:
                print("no place  :(\n\n\n")
            else:
                print("\nyey! We found some places :)\n")

                # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
                places = re.findall(r'(?:en|En) ([A-ZÁ-ÚÜÑ][a-zá-úñüç\-]+)', content)
                countPlaces = Counter(places)

                dfCountPlaces = pd.DataFrame.from_dict(countPlaces, orient='index').reset_index()
                dfCountPlaces = dfCountPlaces.rename(columns={'index':'Places', 0:'freq'})
                dfCountPlaces = dfCountPlaces.sort(["freq"], ascending=True)        
        fin.close()
        print(dfCountPlaces)
        
        return dfCountPlaces


def get_time(wdir, txtFolder):
    """
    This function gets some information about years found in the text
    Parameters:
        - wdir is the path of the gile
        - txtFolder is the name (without format ending) of the file to be analized
    
    Example of how to use it at the console:
    df = get_time("/home/jose/cligs/ne/master/", "ne0022")
    
    """
    # The file is opened
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            
            # We take only the text            
            content = parse_text(doc)
            
            #We create a list for the info
            years=[]
            centuries=[]
            decades=[]

            # We search if there are numbers with four digits in the text at all
            if re.search(r'\D(\d\d\d\d)\D', content) is None:
                print("no year found :(\n\n\n")
            else:
                print("\nyey! We found some years :)\n")
                
                #We look for them and we format it a little bit
                years = re.findall(r'\D(\d\d\d\d)\D', content)
                decades = re.findall(r'\D(\d\d\d)\d\D', content)
                centuries = re.findall(r'\D(\d\d)\d\d\D', content)
                decades = [decade + "*"  for decade in decades]
                centuries = [century + "**"  for century in centuries]
                
                # The frequency is counted
                countYears = Counter(years)
                countDecades = Counter(decades)
                countCentury = Counter(centuries)
                
                # And we create the three dataframes, we change the indexs and we order them through frequency
                dfCountYears = pd.DataFrame.from_dict(countYears, orient='index').reset_index()
                dfCountYears = dfCountYears.rename(columns={'index':'Year', 0:'freq'})
                dfCountYears = dfCountYears.sort(["freq"], ascending=True)        
                print(dfCountYears)
                dfCountDecades = pd.DataFrame.from_dict(countDecades, orient='index').reset_index()
                dfCountDecades = dfCountDecades.rename(columns={'index':'Decade', 0:'freq'})
                dfCountDecades = dfCountDecades.sort(["freq"], ascending=True)        
                print(dfCountDecades)
                dfCountCentury = pd.DataFrame.from_dict(countCentury, orient='index').reset_index()
                dfCountCentury = dfCountCentury.rename(columns={'index':'Century', 0:'freq'})
                dfCountCentury = dfCountCentury.sort(["freq"], ascending=True)        
                print(dfCountCentury)
 
                return dfCountYears, dfCountDecades, dfCountCentury
        fin.close()

        
def get_narrator(wdir, txtFolder):
    """
    This function gets some information about the narrator
    
    Example of how to use it at the console:
    df = get_narrator("/home/jose/cligs/ne/master/", "ne0249")
    
    """
    # The file is opened
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            
            # We take only the text            
            content = parse_text(doc)
            
            narrators = []

            # We search if there are numbers with four digits in the text at all
            if re.search(r'\W(dij(?:o|e))\W', content) is None:
                print("no dijo or dije found :(\n\n\n")
            else:
                print("\nyey! We found some dijo or dije! :)\n")


                # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
                narrators = re.findall(r'\W(dij(?:o|e))\W', content)
                countNarrators = Counter(narrators)

                dfCountNarrators = pd.DataFrame.from_dict(countNarrators, orient='index').reset_index()
                dfCountNarrators = dfCountNarrators.rename(columns={'index':'Narrator', 0:'freq'})
                dfCountNarrators = dfCountNarrators.sort(["freq"], ascending=True)        

                print(dfCountNarrators)                
                return dfCountNarrators
                
        fin.close()

def get_gender(wdir, txtFolder):
    """
    This function gets some information about the narrator
    
    Example of how to use it at the console:
    df = get_gender("/home/jose/cligs/ne/master/", "ne0249")
    
    """
    # The file is opened
    for doc in glob.glob(wdir+txtFolder+"*"):
        
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            
            # We take only the text            
            content = parse_text(doc)
            
            genders = []

            # We search if there are numbers with four digits in the text at all
            if re.search(r'\W(él|ella)\W', content) is None:
                print("no gender found :(\n\n\n")
            else:
                print("\nyey! We found some gender! :)\n")


                # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
                genders = re.findall(r'\W(él|ella)\W', content)
                countGenders = Counter(genders)

                dfCountGenders = pd.DataFrame.from_dict(countGenders, orient='index').reset_index()
                dfCountGenders = dfCountGenders.rename(columns={'index':'Narrator', 0:'freq'})
                dfCountGenders = dfCountGenders.sort(["freq"], ascending=True)        

                print(dfCountGenders)                
                return dfCountGenders
                
        fin.close()


def get_all(wdir, txtFolder):
    """
        This function uses all the other functions from this file
        df = get_all("/home/jose/cligs/ne/master/", "ne0002")
    """
    get_names(wdir, txtFolder)
    get_full_names(wdir, txtFolder)
    get_full_names_protagonist(wdir, txtFolder,3)

    get_time(wdir, txtFolder)
    get_places(wdir, txtFolder)
    get_gender(wdir, txtFolder)
    get_narrator(wdir, txtFolder)
