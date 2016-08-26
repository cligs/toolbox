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
df = get_all("/home/jose/cligs/ne/master/", "ne0002")
"""


def parse_text(wdir, txtFolder):
    """
    This function opens the file, reads it as xml and delete some elements.
    The other funcionts of this file use it. For example:
        content =  parse_text(wdir, txtFolder)
    """
    # We parse the text as xml
    file = wdir+txtFolder+".xml"
        
    xml_tree = etree.parse(file)
    
    # Let's print it to see if everything is ok    
    # print(etree.tostring(xml_tree, pretty_print=True, encoding="unicode"))

    # Namespaces are specified
    specific_namespaces = {'tei':'http://www.tei-c.org/ns/1.0','xi':'http://www.w3.org/2001/XInclude'}

    # Back, front, teiHeader and heads are deleted
    etree.strip_elements(xml_tree, "{http://www.tei-c.org/ns/1.0}back", with_tail=False)
    etree.strip_elements(xml_tree, "{http://www.tei-c.org/ns/1.0}front", with_tail=False)
    etree.strip_elements(xml_tree, "{http://www.tei-c.org/ns/1.0}teiHeader", with_tail=False)
    etree.strip_elements(xml_tree, "{http://www.tei-c.org/ns/1.0}head", with_tail=False)

    # Only text is kept and saved as string
    content = xml_tree.xpath("//text()", namespaces=specific_namespaces)
    content = ''.join(content)
    
    #print(content)
    #print(type(content))

    return content

def get_names(wdir, txtFolder, to_csv = False, full_name = True, protagonist = True, number_protagonists = 3 ):
    """
    This function gives you several dataframe with proper names (searched with a regexp) found in a file.
    It should be useful to know who the protagonist is, or where the action of the text takes place.
    The regexps are thought for Spanish.
    
    For default it will also give us a list of the fullname ordered by frequency and, more interesting, it will try
    to find the whole name of the most frequent names. It is interesting to know the surname of the protagonist,
    but it comes only once in the whole text, so sorting it by frequency won't give us this information. What we do
    instead is to search for the single proper names most frequent (normally three, but we can change it with the
    number_protagonists argument) and try to reconstruct its full name.

    Example of how to use it at the console:
    
    df = get_names("/home/jose/cligs/ne/master/", "ne0002")
    print(get_names("/home/jose/cligs/ne/master/", "ne0002"))

    """
    
    # We open the file
    content =  parse_text(wdir, txtFolder)
    
    #We create a list for the names
    names=[]

    # We search for any word that starts with capital letter and that before didn't have anything that looks like an starting of a sentence
    names = re.findall(r'(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+)', content)
    for name in names:
            name = name.strip()

    # We delete the duplicated items in the list            
    names = list(set(names))
    #print(names)
    # Now we put the list in a data frame
    df_names = pd.DataFrame(names,columns=["name"])
    #print(df_names)
    #And we add a new column for the frequency and we fill it with zeros
    df_names["freq"] = 0
    #print(df_names)
    # Now, for every row, we take the indexes and the other columns with the real values (names and frequency)            
    for index, row in df_names.iterrows():
        # For each, we fill the frecuency with the the amount (len) of a times that the name appears in the text with something 
        df_names.at[index,"freq"] = len(re.findall(r'\W'+ re.escape(row["name"]) + r'\W', content))
    # The df is sorted after the frequency
    df_names = df_names.sort(["freq"], ascending=True)
    print(df_names)
    # If we have defined like this, the data is saved as csv
    if to_csv is True:
        df_names.to_csv(wdir+txtFolder+'_names.csv', sep='\t', encoding='utf-8')

    # Now we try to find the most frequent complete proper names
    if full_name is True:
        #We create a list for the names
        fullNames = []
        #print(fullNames)
        #We put the search in a regexp. Between words that start with a capital letter might be also some preposition, articles and hyphen (for Spanish)
        regexp_fullnames= "(?<=[a-zá-úñüç,;] )([A-ZÁ-ÚÜÑ][a-zá-úñüç]+(?:(?: de | el | del | de la | |\-)[A-ZÁ-ÚÜÑ][a-zá-úñüç]+)+)"
    
        if re.search(r''+regexp_fullnames+'', content) is None:
            print("==========\nno fullNames found (weird!!!) \n:(\n\n")
        else:
            print("==========\nyey! We found some fullNames :)\n")
            # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
            fullNames = re.findall(r''+regexp_fullnames+'', content)
            # We put the list a counter element
            countfullNames = Counter(fullNames)
            #From that, a dataframe is created
            dfCountFullNames = pd.DataFrame.from_dict(countfullNames, orient='index').reset_index()
            # Columns are renamed
            dfCountFullNames = dfCountFullNames.rename(columns={'index':'Fullname', 0:'freq'})
            # And sort by frequency
            dfCountFullNames = dfCountFullNames.sort(["freq"], ascending=True)        
            print(dfCountFullNames)
        #print(dfCountFullNames)
        if to_csv is True:
            # The data is printed as a file
            dfCountFullNames.to_csv(wdir+txtFolder+'_full_names.csv', sep='\t', encoding='utf-8')

    # Now we try to reconstruct the complete names of the most frequent names. The idea is to get the complete name of the protagonists    
    if protagonist is True:

        # First we take the list of names that we created at the beginning of this function and we delete the words that are shorter than two (because many times words like "El" or "La" are kind of used as proper names like in "fuimos a El Retiro".
        df_names_protagonist = df_names[df_names['name'].map(len) > 2]

        # We take only the most frequent; number_protagonists is an argument of the function, with some default value
        df_names_protagonist = df_names_protagonist.tail(n = number_protagonists)
        #print(df_names_protagonist)

        # A empty counter is created
        count_full_names_protagonist = Counter("")
        #print(count_full_names_protagonist)
        # For every name
        for name_protagonist in df_names_protagonist.loc[:,"name"]:
            #print(name_protagonist)

            # We create an empty list of fullnames    
            fullNames = []
            #We search it
            fullNames = re.findall(r'(?<=[a-zá-úñüç,;] )(' + re.escape(name_protagonist) + r'(?:(?: de | el | del | de la | |\-)(?:[A-ZÁ-ÚÜÑ][a-záéíóúñüç]+))+|(?:(?:[A-ZÁ-ÚÜÑ][a-záéíóúñüçñüç]+)(?: de | el | del | de la | |\-)*)+' + re.escape(name_protagonist) + r'(?:(?: de | el | del | de la | |\-)(?:[A-ZÁ-ÚÜÑ][a-zzáéíóúñüçñüç]+))*)', content)                       
            # We cleant it
            for fullName in fullNames:
                fullName = fullName.strip()
            # And we create a Counter
            count_full_names_protagonist = count_full_names_protagonist+Counter(fullNames)
            #print(count_full_names_protagonist)
        # Miramos si el contador está vacío

        # A data frame is created
        df_count_full_names_protagonists = pd.DataFrame.from_dict(count_full_names_protagonist, orient='index').reset_index()
        #The columns are renamed
        df_count_full_names_protagonists = df_count_full_names_protagonists.rename(columns={'index':'full_name_protagonist', 0:'freq'})
        #print(df_count_full_names_protagonists)
        # And sorted
        df_count_full_names_protagonists = df_count_full_names_protagonists.sort(["freq"], ascending=True)        
        print(df_count_full_names_protagonists)
        if to_csv is True:
            # The data is printed as a file
            df_count_full_names_protagonists.to_csv(wdir+txtFolder+'_full_name_protagonist.csv', sep='\t', encoding='utf-8')

        return df_count_full_names_protagonists        

    return df_names, 

def get_places(wdir, txtFolder, to_csv = False):
    """
    This function tries to get 
    wdir is the path of the gile
    txtFolder is the name (without format ending) of the file to be analized

    Example of how to use it at the console:
    
    df = get_places("/home/jose/cligs/ne/master/", "ne0002")
    """
    # We open the file
    content =  parse_text(wdir, txtFolder)
    #We create a list for the places
    places = []

    regexp_places = "(?:en|En) ([A-ZÁ-ÚÜÑ][a-zá-úñüç]+(?:(?: de | el | del | de la | |\-)[A-ZÁ-ÚÜÑ][a-zá-úñüç]*)*)"
    if re.search(r''+regexp_places+'', content) is None:
        print("==========\nno place  :(\n\n")
    else:
        print("==========\nyey! We found some places :)\n")

        # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
        places = re.findall(r''+regexp_places+'', content)
        countPlaces = Counter(places)

        dfCountPlaces = pd.DataFrame.from_dict(countPlaces, orient='index').reset_index()
        dfCountPlaces = dfCountPlaces.rename(columns={'index':'Places', 0:'freq'})
        dfCountPlaces = dfCountPlaces.sort(["freq"], ascending=True)        

    print(dfCountPlaces)
    if to_csv is True:
        # The data is printed as a file
        dfCountPlaces.to_csv(wdir+txtFolder+'_places.csv', sep='\t', encoding='utf-8')
    
    return dfCountPlaces


def get_time(wdir, txtFolder, to_csv = False):
    """
    This function gets some information about years found in the text
    Parameters:
        - wdir is the path of the gile
        - txtFolder is the name (without format ending) of the file to be analized
    
    Example of how to use it at the console:
    df = get_time("/home/jose/cligs/ne/master/", "ne0022")
    
    """
    # We open the file
    content =  parse_text(wdir, txtFolder)

    #We create a list for the info
    years=[]
    centuries=[]
    decades=[]

    # We search if there are numbers with four digits in the text at all
    if re.search(r'\D(\d\d\d\d)\D', content) is None:
        print("==========\nno year found :(\n\n")
    else:
        print("==========\nyey! We found some years :)\n")
        
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

        if to_csv is True:
            # The data is printed as a file
            dfCountCentury.to_csv(wdir+txtFolder+'_century.csv', sep='\t', encoding='utf-8')
            dfCountDecades.to_csv(wdir+txtFolder+'_decades.csv', sep='\t', encoding='utf-8')
            dfCountYears.to_csv(wdir+txtFolder+'_years.csv', sep='\t', encoding='utf-8')
 
        return dfCountYears, dfCountDecades, dfCountCentury


def get_narrator(wdir, txtFolder):
    """
    This function gets some information about the narrator
    
    Example of how to use it at the console:
    df = get_narrator("/home/jose/cligs/ne/master/", "ne0249")
    
    """
    # We open the file
    content =  parse_text(wdir, txtFolder)

    
    narrators = []

    # We search if there are numbers with four digits in the text at all
    if re.search(r'\W(dij(?:o|e))\W', content) is None:
        print("==========\nno dijo or dije found  (weird!!!) \n:(\n\n")
    else:
        print("==========\nyey! We found some dijo or dije! :)\n")


        # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
        narrators = re.findall(r'\W(dij(?:o|e))\W', content)
        countNarrators = Counter(narrators)

        dfCountNarrators = pd.DataFrame.from_dict(countNarrators, orient='index').reset_index()
        dfCountNarrators = dfCountNarrators.rename(columns={'index':'Narrator', 0:'freq'})
        dfCountNarrators = dfCountNarrators.sort(["freq"], ascending=True)        

        print(dfCountNarrators)                
        return dfCountNarrators
                

def get_gender(wdir, txtFolder):
    """
    This function gets some information about the narrator
    
    Example of how to use it at the console:
    df = get_gender("/home/jose/cligs/ne/master/", "ne0249")
    
    """
    # We open the file
    content =  parse_text(wdir, txtFolder)

    genders = []

    # We search if there are numbers with four digits in the text at all
    if re.search(r'\W(él|ella)\W', content) is None:
        print("no gender found   (weird!!!) \n:(\n\n")
    else:
        print("==========\nyey! We found some gender! :)\n")


        # We search for any word that starts with capital letter and that before had the Spanish preposition "de" or "en" (an intuitiv thing I though myself)
        genders = re.findall(r'\W(él|ella)\W', content)
        countGenders = Counter(genders)

        dfCountGenders = pd.DataFrame.from_dict(countGenders, orient='index').reset_index()
        dfCountGenders = dfCountGenders.rename(columns={'index':'Narrator', 0:'freq'})
        dfCountGenders = dfCountGenders.sort(["freq"], ascending=True)        

        print(dfCountGenders)                
        return dfCountGenders



def get_all(wdir, txtFolder):
    """
    We put all the functions in a single function to use it in a more comfortable way
    Example of how to use it:
    df = get_all("/home/jose/cligs/ne/master/", "ne0002")
    """
    names = get_names(wdir, txtFolder, to_csv = False, full_name = True, protagonist = True, number_protagonists = 3)
    places = get_places(wdir, txtFolder, to_csv = False)
    times = get_time(wdir, txtFolder, to_csv = False)
    narrators = get_narrator(wdir, txtFolder)
    genders = get_gender(wdir, txtFolder)
    print("documento analizado: ",txtFolder)
    return names, places, times, narrators, genders
    

df = get_all("/home/jose/cligs/ne/master/", "ne0230")
