# -*- coding: utf-8 -*-
"""
    This script lemmatize in different flavours spanish text using Freeling. In order to use it, you have to have
    Freeling 3.0 running in your computer (which is not the newest version of Freeling, since in 2016 Freeling 4.0 was published.
    Good luck installing it. May the the gods be kind with you.

    @author: jct

    Example of how to use it:

        inpath="/home/jose/cligs/ne/master/"
        output="/home/jose/cligs/ne/processed/"
        input_nlp = output
        
        lemmatizeText(inpath,output)
        
        make_dataframe_nlp(input_nlp)
        
        make_basic_versions(input_nlp)
"""

# We call some libraries that we are going to need
import sys
import os
sys.path.append(os.path.abspath("/home/jose/cligs/toolbox/"))

import csv
import subprocess
import glob
import re
import assist_metadata
import pandas as pd
from io import StringIO
from nltk.corpus import wordnet as wn

# The next functions lemmatize the texts that are in the 0-input folder
def lemmatizeText(inpath,output):
    """
    This function call the Freeling 3.0 and lemmatize the text in the basic way.
    Example of how to use it:

        inpath="/home/jose/cligs/ne/master/"
        output="/home/jose/cligs/ne/processed/"
        
        lemmatizeText(inpath,output)
    """
    print("lemmatizazing text from inpath: "+inpath)
    # For every file in the 0-input folder
    for file in glob.glob(inpath+"/*.*"):

        # The programs takes a path of import, of export and a format
        pathname=os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname = fullfilename[:-4]
        
        # The TEI structure is deleted, included back, front and headers        
        content = assist_metadata.parse_text(inpath,basicname)
        
        # We save a name for the new document
        plaintextInpath = output+'/1-plaintext/'
        # If we don't have already a folder called 1-plaintext, we create it
        if not os.path.exists(os.path.dirname(plaintextInpath)):
            os.makedirs(os.path.dirname(plaintextInpath))            
        # And finally we save the document
        with open (plaintextInpath+'/'+basicname+'.txt', "w", encoding="utf-8") as fout:
            fout.write(content)

        # We create a folder for the POS and if there is not such folder, we create it
        fullPosInpath = output+'2-fullMorphoPOS/'        
        if not os.path.exists(os.path.dirname(fullPosInpath)):
            os.makedirs(os.path.dirname(fullPosInpath))            
        
        # We call the Freeling to do the magic!
        subprocess.call ('analyze -f es.cfg <'+plaintextInpath+basicname+'.txt  >'+fullPosInpath+basicname+'.txt', shell=True)

def make_dataframe_nlp(inpath):
    """
        This function converts the output of Freeling into CSV and add information from the wordnet from nltk
        
        Example of how to use it:
        
        input_nlp="/home/jose/cligs/ne/processed/"
        make_dataframe_nlp(input_nlp)

    """
    print("Converting everything to a dataframe: "+inpath)
    
    full_inpath = inpath+"2-fullMorphoPOS/"
    outpath = inpath + "3-MorphoPOS-csv/" 
    # For every file in the 2-fullPOS folder
    for file in glob.glob(full_inpath+"*.*"):
        # The programs takes a path of import, of export and a format    
        pathname = os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        print("fullname: "+fullfilename)
        basicname = fullfilename[:-4]
        # We open it and read every line
        with open(file, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
       
            # Some times Freeling give you two different options for a word because the probability of both is exactly 0.5. I have only seen that with the word lo and the difference is very subtle. The next line delete the second option
            content = re.sub(r'^(.+ .+ .+ [\d\.]+) .+ .+ [\d\.]+ *$', r'\1', content,  flags=re.M)
            
            # We pass it to a io element to
            content_io = StringIO(content)

            #From that, we can read it as csv file
            df_nlp = pd.read_csv(content_io, encoding="utf-8", sep=" ", names = ["token", "lemma", "POS", "probility"])
            
            # Now we put specific grammatical values in the different columns
            df_nlp["category"] = df_nlp["POS"].str[0]
            df_nlp["category_subcategory"] = df_nlp["POS"].str[0:2]
            df_nlp["subcategory"] = df_nlp["POS"].str[1]

            # A column for the lexname is added to the dataframe
            df_nlp["first_wdlexname"] = ""
            """df_nlp["all_wdlexname"] = """""
            df_nlp["different_wdlexname"] = ""

            # Now we are goint to put the lexname
            # Verbs
            for index, row in df_nlp.iterrows():
                if row["category"] == "V":
                    if wn.synsets(row["lemma"], lang = 'spa', pos=wn.VERB):

                        df_nlp.loc[index, 'first_wdlexname'] = wn.synsets(row["lemma"], pos=wn.VERB, lang='spa')[0].lexname()
                        list_synsets = []
                        for synset in wn.synsets(row["lemma"], pos=wn.VERB, lang='spa'):
                            list_synsets.append(synset.lexname()) 
                        
                        set_synsets = set(list_synsets)
                        set_synsets = " ".join(set_synsets)
                        df_nlp.loc[index, 'different_wdlexname'] = set_synsets

                        """
                        list_synsets = " ".join(list_synsets)
                        df_nlp.loc[index, 'all_wdlexname'] = list_synsets
                        """

            # Adjectives
            for index, row in df_nlp.iterrows():
                if row["category"] == "A":
                    if wn.synsets(row["lemma"], lang = 'spa', pos=wn.ADJ):

                        df_nlp.loc[index, 'first_wdlexname'] = wn.synsets(row["lemma"], pos=wn.ADJ, lang='spa')[0].lexname()

                        list_synsets = []
                        for synset in wn.synsets(row["lemma"], pos=wn.ADJ, lang='spa'):
                            list_synsets.append(synset.lexname()) 
                        
                        set_synsets = set(list_synsets)
                        set_synsets = " ".join(set_synsets)
                        df_nlp.loc[index, 'different_wdlexname'] = set_synsets

                        """
                        list_synsets = " ".join(list_synsets)
                        df_nlp.loc[index, 'all_wdlexname'] = list_synsets
                        """

            # Adverbs
            for index, row in df_nlp.iterrows():
                if row["category"] == "S":
                    if wn.synsets(row["lemma"], lang = 'spa', pos=wn.ADV):

                        df_nlp.loc[index, 'first_wdlexname'] = wn.synsets(row["lemma"], pos=wn.ADV, lang='spa')[0].lexname()

                        list_synsets = []
                        for synset in wn.synsets(row["lemma"], pos=wn.ADV, lang='spa'):
                            list_synsets.append(synset.lexname()) 
                        
                        set_synsets = set(list_synsets)
                        set_synsets = " ".join(set_synsets)
                        df_nlp.loc[index, 'different_wdlexname'] = set_synsets

                        """
                        list_synsets = " ".join(list_synsets)
                        df_nlp.loc[index, 'all_wdlexname'] = list_synsets
                        """
            # Nouns

            for index, row in df_nlp.iterrows():
                if row["category"] == "N":
                    if wn.synsets(row["lemma"], lang = 'spa', pos=wn.NOUN):

                        df_nlp.loc[index, 'first_wdlexname'] = wn.synsets(row["lemma"], pos=wn.NOUN, lang='spa')[0].lexname()

                        list_synsets = []
                        for synset in wn.synsets(row["lemma"], pos=wn.NOUN, lang='spa'):
                            list_synsets.append(synset.lexname()) 
                        
                        set_synsets = set(list_synsets)
                        set_synsets = " ".join(set_synsets)
                        df_nlp.loc[index, 'different_wdlexname'] = set_synsets

                        """
                        list_synsets = " ".join(list_synsets)
                        df_nlp.loc[index, 'all_wdlexname'] = list_synsets
            
                        """
            # We delete the POS of the wordnet columns
            wdlex_list = ["different_wdlexname","first_wdlexname"]
            wd_pos_list = ["verb.","noun.","adj.","adv."]
            for wdlex in wdlex_list:
                for wd_pos in wd_pos_list:
                    df_nlp[wdlex] = df_nlp[wdlex].str.replace(wd_pos, '')
            
            # Now we save in a column different grammatical values that could be interesting, like the person
            person_possisions = { "A" : 5, "D" : 2, "P" : 2, "V" : 4}
            for key, value in person_possisions.items():
                df_nlp.ix[df_nlp["category"] == key, "person"] = df_nlp["POS"].str[value]

            # The gender
            gender_possisions = { "A" : 3, "D" : 3, "N" : 2, "P" : 3, "V" : 6}
            for key, value in gender_possisions.items():
                df_nlp.ix[df_nlp["category"] == key, "gender"] = df_nlp["POS"].str[value]

            # The number
            number_possisions = { "A" : 4, "D" : 4, "N" : 4, "P" : 4, "V" : 5}
            for key, value in number_possisions.items():
                df_nlp.ix[df_nlp["category"] == key, "number"] = df_nlp["POS"].str[value]

            # Other specific information
            subsubcategory = {
                                "A" : 2, # Degree of adjectives #S:superlative;	V:evaluative
                                "P" : 6, # Polite #P:yes
                               }
            for key, value in subsubcategory.items():
                df_nlp.ix[df_nlp["category"] == key, "subsubcategory"] = df_nlp["POS"].str[value]

            # case of the pronouns
            df_nlp.ix[df_nlp["category"] == "P", "case"] = df_nlp["POS"].str[5]

            # Mood of the verbs
            df_nlp.ix[df_nlp["category"] == "V", "mood"] = df_nlp["POS"].str[2]

            # Or the time of the verbs
            df_nlp.ix[df_nlp["category"] == "V", "time"] = df_nlp["POS"].str[3]
                      
            
            print(df_nlp)
            if not os.path.exists(os.path.dirname(outpath)):
                os.makedirs(os.path.dirname(outpath))    
            df_nlp.to_csv(outpath+basicname+'.csv', sep='\t', encoding='utf-8')

def make_explicit(df):
    """
    This function make explicit the values of the columns that we pass. Is basically a subfunction of the function save_persions_pos
    Example of how tu use it:
    
    df_nlp = make_explicit(df_nlp)
    """
    # Dictionaries are created for each kind column    
    category = {
    "A" : "adjective",
    "C" : "conjunction",

    "D" : "determiner",
    "N" : "noun",
    "P" : "pronoun",
    "R" : "adverb",
    "S" : "adposition",
    "V" : "verb",
    "Z" : "number",
    "W" : "date",
    "I" : "interjection",
    "F" : "punctuation",
    }
    category_subcategory = {
    "AO" : "adjective_ordinal",
    "AQ" : "adjective_qualificative",
    "AP" : "adjective_possessive",
    "CC" : "conjunction_coordinating",
    "CS" : "conjunction_subordinating",

    "DA" : "determiner_article",
    "DD" : "determiner_demonstrative",
    "DI" : "determiner_indefinite",
    "DP" : "determiner_possessive",
    "DT" : "determiner_interrogative",
    "DE" : "determiner_exclamative",

    "NC" : "noun_common",
    "NP" : "noun_proper",

    "P0" : "pronoun_",
    "PD" : "pronoun_demonstrative",
    "PE" : "pronoun_exclamative",
    "PI" : "pronoun_indefinite",
    "PP" : "pronoun_personal",
    "PR" : "pronoun_relative",
    "PT" : "pronoun_interrogative",

    "RN" : "adverb_negative",
    "RG" : "adverb_general",

    "SP" : "adposition_preposition",

    "VM" : "verb_main",
    "VA" : "verb_auxiliary",
    "VS" : "verb_semiauxiliary",

    "Z" : "number_",
    "Zd" : "number_partitive",
    "Zm" : "number_currency",
    "Zp" : "number_percentage",
    "Zu" : "number_unit",

    "W" : "date_",

    "I" : "interjection_",
    
    "Fd" : "punctuation_colon",
    "Fc" : "punctuation_comma",
    "Fl" : "punctuation_bracket",
    "Fs" : "punctuation_etc",
    "Fa" : "punctuation_exclamation",
    "Fg" : "punctuation_hyphen",
    "Fz" : "punctuation_other",
    "Fp" : "punctuation_parenthesis",
    "Fi" : "punctuation_question",
    "Fe" : "punctuation_quotation1",
    "Fr" : "punctuation_quotation2",
    "Fx" : "punctuation_semicolon",
    "Fh" : "punctuation_slash",
    }
    person = {
    1 : "first",
    2 : "second",
    3 : "third",
    }
    gender = {
    "M" : "masculine",
    "F" : "feminine",
    "C" : "common",
    }
    number = {
    "S" : "singular",
    "P" : "masculine",
    "N" : "invariable",
    }
    time = {
    "P" : "present",
    "I" : "imperfect",
    "F" : "future",
    "S" : "past",
    "C" : "conditional",
    }
    subsubcategory = {
    "S" : "superlative",
    "V" : "evaluative",
    "P" : "polite",
    } 
    case = {
    "N" : "nominative",
    "A" : "accusative",
    "D" : "dative",
    "O" : "oblique",
    }
    mood = {
    "I" : "indicative",
    "S" : "subjunctive",
    "M" : "imperative",
    "P" : "participle",
    "G" : "gerund",
    "N" : "infinitive",
    }
    
    # We match the column and the dictionaries and replace its values
    for dfcolumn in df:
        if dfcolumn == "category":
            for key, value in category.items():
                df.loc[df["category"] == key, "category"] = value
        if dfcolumn == "category_subcategory":
            for key, value in category_subcategory.items():
                df.loc[df["category_subcategory"] == key, "category_subcategory"] = value
        if dfcolumn == "person":
            for key, value in person.items():
                df.loc[df["person"] == key, "person"] = value
        if dfcolumn == "gender":
            for key, value in gender.items():
                df.loc[df["gender"] == key, "gender"] = value
        if dfcolumn == "number":
            for key, value in number.items():
                df.loc[df["number"] == key, "number"] = value
        if dfcolumn == "time":
            for key, value in time.items():
                df.loc[df["time"] == key, "time"] = value
        if dfcolumn == "case":
            for key, value in case.items():
                df.loc[df["case"] == key, "case"] = value
        if dfcolumn == "mood":
            for key, value in mood.items():
                df.loc[df["mood"] == key, "mood"] = value        
        if dfcolumn == "subsubcategory":
            for key, value in subsubcategory.items():
                df.loc[df["subsubcategory"] == key, "subsubcategory"] = value

            
    return df


def save_persions_pos(inpath, columns = ["lemma", "POS"], conditions = {}, explicit = False, separator="_", kind_kondition = True, delete_zeros = True, replace_with = {}, mixing_columns = {}):
    """
    This function makes versions from the dataframe converted from the freeling output. It has many option of conditioning, replacing and deleting in order to work with the output in different programs, like stylo
    The next function call some different versions of this function.
    Example of how to use it:
    
    input_nlp="/home/jose/cligs/ne/processed/"
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["category_subcategory","person","number","gender","time","mood","subsubcategory"],
        separator = " ",
        replace_with = {"_":"÷","\.":"÷"},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "÷"},
        conditions = {},
        kind_kondition = False
        )
    """    
    print("Making a version of POS dataframe: "+inpath)
    
    # The next forlder must contain the csv data of Freeling
    full_inpath = inpath+"3-MorphoPOS-csv/"

    # For every file in the original folder
    for file in glob.glob(full_inpath+"*.*"):
        # We create a subfolder for information that we want
        subfolder_path= "_".join(columns)
        # The programs takes a path of import, of export and a format    
        pathname = os.path.basename
        # We get the basic name of the file
        fullfilename = pathname(file)
        #print("fullname: "+fullfilename)
        basicname = fullfilename[:-4]

        # We read the content as csv
        df_nlp = pd.read_csv(full_inpath+fullfilename, encoding = "utf-8", sep = "\t")
        #print("We read it.")
     
        # If we have passed some conditions
        if len(conditions) > 0:
            for key, value in conditions.items():
                subfolder_path = subfolder_path+"_"+key+value
            subfolder_path = subfolder_path+"_"+str(kind_kondition)

            # We iterate thorught them, separating keys and values
            for key, value in conditions.items():
                if kind_kondition is True:
                    # And we delete rfom the columns the values that we have seted
                    df_nlp = df_nlp[df_nlp[key] == value]
                else:
                    # And we delete rfom the columns the values that we have seted
                    df_nlp = df_nlp[df_nlp[key] != value]

        # We give the option to change some characters soit can work better in stylo ot other programs
        if len(mixing_columns) > 0:
            subfolder_path = subfolder_path+"_"+mixing_columns["filter_value"]+"As"+mixing_columns["target_column"]
            # We select the rows that fit the condition
            df_nlp.loc[df_nlp[mixing_columns["filter_column"]] == mixing_columns["filter_value"], mixing_columns["target_column"]] = mixing_columns["extra_str"]+df_nlp[mixing_columns["source_column"]]+mixing_columns["extra_str"]


        # The columns that are not in the list are deleted        
        df_nlp = df_nlp[columns]

        # We give the option to make the tags explicit
        if explicit is True:
            subfolder_path = subfolder_path+"_exp"
            df_nlp = make_explicit(df_nlp)
    
        # We give the option to change some characters so it can work better in stylo ot other programs
        if len(replace_with) > 0:
            for key, value in replace_with.items():
                df_nlp = df_nlp.replace({key: value}, regex=True)


        """
        # The next part is stil not working:
        # Habría que dar la opción de borrar los 0
        if delete_zeros is True:

            df_nlp.replace("0","")
            
            print("Vamos a cargarnos unos caracteres!!!")
            for column in df_nlp:
                df_nlp[column].replace(to_replace="0", method='ffill')
                df_nlp[column].replace(to_replace="0.0", method='ffill')

            #df_nlp = df_nlp.replace('0.0','')
        """

        # We print the result        
        outpath = inpath + "4-Versions/"+subfolder_path+"/" 
        if not os.path.exists(os.path.dirname(outpath)):
            os.makedirs(os.path.dirname(outpath))    
        df_nlp.to_csv(outpath+basicname+'.txt', sep=separator, encoding='utf-8', index = False, quoting=csv.QUOTE_NONE)

def make_basic_versions(input_nlp):
    """
    This function makes some versions of the data that we thought they might be interesting
    Example of how to use it:

        input_nlp="/home/jose/cligs/ne/processed/"
        make_basic_versions(input_nlp)

    """
    print("version 1")
    # This version gives us the tokens. It also includes the idioms found by freeling as tokens. It gives us the punctuation as tags
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["token"],
        separator = " ",
        replace_with = {"_":"÷","\.":"÷"},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "þ"},
        )
    print("version 2")
    # This version gives us tokens, lemma and category_subcategory (this one as the values of the tags). Puntuaction is deleted
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["token","lemma","category_subcategory"],
        separator = " ",
        replace_with = {"_":"÷","\.":"÷"},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "þ"},
        conditions = {"category": "F"},
        kind_kondition = False
        )
    print("version 3")
    # This version gives us only morfological information, and with the values of the tags
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["category_subcategory","person","number","gender","time","mood","subsubcategory"],
        separator = " ",
        replace_with = {"_":"÷","\.":"÷"},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "þ"},
        conditions = {},
        kind_kondition = False
        )

    print("version 4")
    # This version gives us only the punctuation as it is, something like ",,,,.¡!...().()¿?". Just for fun :)
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["token"],
        separator = " ",
        replace_with = {},
        mixing_columns = {},
        conditions = {"category": "F"},
        kind_kondition = True
        )


    print("version 5")
    # This version gives us only the punctuation as the values of the tags
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["category_subcategory"],
        separator = " ", 
        replace_with = {"punctuation_":""},
        mixing_columns = {},
        conditions = {"category": "F"},
        kind_kondition = True
        )

    print("version 6")
    # This one gives us token and subcategory_subcategory alltogether, as a string    
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["token","category_subcategory"],
        separator = "÷", 
        replace_with = {"_":"","\.":""},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "þ"},
        )
    print("version 7")
    # This one gives us the token and all the morfological information as string   
    save_persions_pos(
        input_nlp,
        explicit = True,
        columns = ["token","POS"],
        separator = "÷", 
        replace_with = {"0":"ä","1":"ë","2":"ï","3":"ö"},
        mixing_columns = {"filter_column" : "category", "filter_value" : "F", "source_column" : "category_subcategory", "target_column" : "token", "extra_str" : "þ"},
        )

    print("version 8")
    # Punctuation is deleted    
    save_persions_pos(
        input_nlp,
        explicit = False,
        columns = ["token","POS"],
        separator = "÷", 
        replace_with = {"0":"ä","1":"ë","2":"ï","3":"ö"},
        conditions = {"category": "F"},
        kind_kondition = False
        )