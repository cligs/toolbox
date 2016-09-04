# ./bin/env python3
# make_zwischenformat_tc.py
# author: #cf

"""
# Function to extract data from dramatic texts marked up in TEI P5 and save it to the DLINA Zwischenformat.
# This has been developed for and probably only works with the CLiGS P5-versions built from theatre-classique.fr. 
"""

import os
import re
import glob
from lxml import etree
from collections import Counter



WorkDir = "/"
InPath = WorkDir+"tei/*.xml"
OutFolder = WorkDir+"zf/"



def read_xml(File):
    """
    Reads an XML-TEI file and parses it into an LXML object.
    Status: OK.
    """
    with open(File, "r") as InFile: 
        PlayXML = etree.parse(InFile)
        etree.strip_tags(PlayXML, "{http://www.tei-c.org/ns/1.0}seg")
        etree.strip_tags(PlayXML, "{http://www.tei-c.org/ns/1.0}hi")
        etree.strip_elements(PlayXML, "{http://www.tei-c.org/ns/1.0}note", with_tail=False)
        etree.strip_elements(PlayXML, "{http://www.tei-c.org/ns/1.0}quote", with_tail=False)
        #XML = etree.tostring(XML)
        #print("Length of PlayXML", len(etree.tostring(PlayXML)))
        return PlayXML


def get_processing(Idno): 
    """
    Call up the processing instructions (including the root element!) for the zwischenformat.
    Status: OK. 
    TODO: Maybe include full idno if schema is relaxed to allow non-integers in the play id.
    """
    Processing = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<?xml-model href=\"http://raw.githubusercontent.com/DLiNa/project/master/rules/lina.rnc\"?>\n<?xml-model href=\"http://raw.githubusercontent.com/DLiNa/project/master/rules/lina.sch\"?>\n<play id=\""+str(Idno[2:])+"\" xmlns=\"http://lina.digital\">"
    return Processing


def create_header(PlayXML, Idno): 
    """
    Generate the header section of the zwischenformat with metadata. 
    Status: OK
    TODO: maybe split up into individual sub-functions and do similar things using parameters. 
    """
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_titleshort = "//tei:teiHeader//tei:title[@type='short']//text()"
    Title = PlayXML.xpath(XP_titleshort, namespaces=namespaces)[0]
    #print(Title)
    XP_subtitle = "//tei:teiHeader//tei:title[@type='sub']//text()"
    Subtitle = PlayXML.xpath(XP_subtitle, namespaces=namespaces)
    if len(Subtitle) == 1: 
        Subtitle = Subtitle[0]
    else: 
        Subtitle = "N/A"
    #print(Subtitle)
    XP_genrelabel = "//tei:teiHeader//tei:keywords//tei:term[@type='genre']//text()"
    Genrelabel = PlayXML.xpath(XP_genrelabel, namespaces=namespaces)
    if len(Genrelabel) == 1: 
        Genrelabel = Genrelabel[0]
    else: 
        Genrelabel = "N/A"
    #print(Genrelabel)
    XP_authorshort = "//tei:teiHeader//tei:author//tei:name[@type='short']//text()"
    Author = PlayXML.xpath(XP_authorshort, namespaces=namespaces)[0]
    #print(Author)
    XP_yearprint = "//tei:teiHeader//tei:bibl[@type='print-source']//tei:date//text()"
    YearPrint = PlayXML.xpath(XP_yearprint, namespaces=namespaces)
    if len(YearPrint) == 1: 
        if len(YearPrint[0]) == 4: 
            YearPrint = YearPrint[0]
        else:
            YearPrint = "9999"
            print("WARNING. A date is missing.")
    else: 
        YearPrint = "0000"
        print("WARNING. A date is missing.")
    
    #print(YearPrint)
    XP_yearpremiere = "//tei:teiHeader//tei:bibl[@type='performance-first']//tei:date//text()"   
    YearPremiere = PlayXML.xpath(XP_yearpremiere, namespaces=namespaces)
    if len(YearPremiere) == 1: 
        if len(YearPremiere[0]) == 4: 
            YearPremiere = YearPremiere[0]
        else:
            YearPremiere = "9999"
            print("WARNING. A date is missing.")
    else: 
        YearPremiere = "0000"
        print("WARNING. A date is missing.")
    #print(YearPremiere)
    XP_source = "//tei:teiHeader//tei:bibl[@type='digital-source']//tei:ref/@target"
    Source = PlayXML.xpath(XP_source, namespaces=namespaces)
    if len(Source) == 1: 
        Source = Source[0]
    else: 
        Source = "N/A"
    #print(Source)
    Header = "<header>\n<title>"+Title+"</title>\n<subtitle>"+Subtitle+"</subtitle>\n<genretitle>"+Genrelabel+"</genretitle>\n<author>"+Author+"</author>\n<date type=\"print\" when=\""+str(YearPrint)+"\">"+str(YearPrint)+"</date>\n<date type=\"premiere\" when=\""+str(YearPremiere)+"\">"+str(YearPremiere)+"</date>\n<date type=\"written\"/>\n<source>"+Source+"</source>\n</header>"
    #print(Header)
    return Header


def create_personae(PlayXML): 
    """
    Generate the personae (cast list) section of the Zwischenformat.
    Status: OK.
    TODO (optional): Also extract character sex, if information is available. 
    """
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_speakers = "//tei:sp/@who"
    SpeakersXML = PlayXML.xpath(XP_speakers, namespaces=namespaces)
    SpeakersList = list(set(SpeakersXML))
    #print("Number of (speaking) characters in this play:", len(SpeakersList))
    Personae = ""
    for Speaker in SpeakersList: 
        SpeakerName = re.sub("-", " ", Speaker[7:])
        SpeakerID = Speaker
        Personae = Personae+"<character>\n<name>"+SpeakerName+"</name>\n<alias xml:id=\""+SpeakerID+"\">\n<name>"+SpeakerName+"</name>\n</alias>\n</character>"
    Personae = "<personae>\n"+Personae+"\n</personae>"
    #print(Personae)
    return Personae
    

def get_acts(PlayXML): 
    """
    Splits the full drama into individual acts. 
    Status: OK.
    """
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_acts = "//tei:div[@type='acte']"
    ActsXML = PlayXML.xpath(XP_acts, namespaces=namespaces)
    XP_actsheads = "//tei:div[@type='acte']/tei:head/text()"
    ActsHeads = PlayXML.xpath(XP_actsheads, namespaces=namespaces)
    #print(len(ActsXML), "acts")
    #print(ActsHeads)
    if len(ActsXML) < 1: 
        print("ERROR. No acts found!")
    if len(ActsHeads) < 1: 
        print("WARNING. No act heads found!")
        ActsHeads = ["N/A"]*10
    return ActsXML, ActsHeads


def get_scenes(ActXML, ActsCounter): 
    """
    Splits each act into individual scenes. 
    Status: OK. (maybe unnecessary)
    """
    #print("Length of ActXML", len(etree.tostring(ActXML)))
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_scenes = "//tei:div[@n='"+str(ActsCounter)+"']/tei:div[@type='scene']"
    ScenesXML = ActXML.xpath(XP_scenes, namespaces=namespaces)
    XP_scenesheads = "//tei:div[@n='"+str(ActsCounter)+"']/tei:div[@type='scene']/tei:head/text()"
    ScenesHeads = ActXML.xpath(XP_scenesheads, namespaces=namespaces)
    #print(len(ScenesXML), "scenes")
    if len(ScenesXML) < 1: 
        print("ERROR. No scenes found!")
    if len(ScenesHeads) < 1: 
        print("WARNING. No scene heads found!")
        ScenesHeads = ["N/A"]*30
    return ScenesXML, ScenesHeads


def get_speakers(SceneXML, ActsCounter, ScenesCounter): 
    """
    Extracts a list of different speakers from a scene.
    Format: List of IDs.
    Status: OK.
    """
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_SceneSpeakers = "//tei:div[@n='"+str(ActsCounter)+"']/tei:div[@n='"+str(ScenesCounter)+"']/tei:sp/@who"
    SceneSpeakers = SceneXML.xpath(XP_SceneSpeakers, namespaces=namespaces)
    SceneSpeakersDict = Counter(SceneSpeakers)
    SceneSpeakersList = list(set(SceneSpeakers))
    #print("Number of characters in scene:", len(SceneSpeakersList))
    #print("SpeakerIDs of characters in scene:", SceneSpeakersList)
    #print("Number of speeches per character in scene:", SceneSpeakersDict)
    return SceneSpeakersList, SceneSpeakersDict


def get_speakertext(SceneXML, SceneSpeaker, ActsCounter, ScenesCounter):
    """
    For a speaker in a scene, extracts the text spoken by the speaker.
    Format: XML so that structural data can still be extracted. 
    Status: OK.
    """
    namespaces = {"tei" : "http://www.tei-c.org/ns/1.0"}
    XP_SceneSpeakertextProse = "//tei:div[@n='"+str(ActsCounter)+"']/tei:div[@n='"+str(ScenesCounter)+"']/tei:sp[@who='"+str(SceneSpeaker)+"']/tei:p/tei:s"    
    SceneSpeakertextProse = SceneXML.xpath(XP_SceneSpeakertextProse, namespaces=namespaces)
    if SceneSpeakertextProse: 
        SceneSpeakertextXML = SceneSpeakertextProse
        #print("There is some prose!")
        #print(SceneSpeakertextXML)
    else: 
        XP_SceneSpeakertextVerse = "//tei:div[@n='"+str(ActsCounter)+"']/tei:div[@n='"+str(ScenesCounter)+"']/tei:sp[@who='"+str(SceneSpeaker)+"']/tei:l"    
        SceneSpeakertextVerse = SceneXML.xpath(XP_SceneSpeakertextVerse, namespaces=namespaces)
        SceneSpeakertextXML = SceneSpeakertextVerse
        #print("There is some verse!")
        #print(SceneSpeakertextXML)
    return SceneSpeakertextXML


def get_speakerstats(SceneSpeakertextXML, SceneSpeakerID, SceneSpeakersDict): 
    """
    For the text spoken by one speaker, calculates some statistics and puts them in a list.
    Data includes: Number of chars, words, lines, speeches. 
    Status: OK
    """
    #print("Now:", SceneSpeakerID)
    NumSpeechActs = SceneSpeakersDict[SceneSpeakerID]   
    AllNumChars = 0
    AllNumWords = 0
    AllNumLines = 0 
    for SpeechXML in SceneSpeakertextXML:
        SceneSpeakertextText = SpeechXML.text
        SST = SceneSpeakertextText
        #print(SST, "\n")
        NumChars = len(SST)
        AllNumChars = AllNumChars + NumChars
        NumWords = len(re.split("\W", SST))
        AllNumWords = AllNumWords + NumWords
        NumLines = len(re.split("\n", SST))
        AllNumLines = AllNumLines+NumLines
    SceneSpeakerstats = [SceneSpeakerID, NumSpeechActs, AllNumLines, AllNumWords, AllNumChars]
    #print(SceneSpeakerstats)
    return SceneSpeakerstats


def SceneSpeakerstats_to_ZF(SceneSpeakerstats): 
    """
    Converts the list of speaker statistics into an XML snippet to be inserted into the Zwischenformat.
    Status: OK.
    """
    SceneSpeakerIDZF = "<sp who=\"#"+str(SceneSpeakerstats[0])+"\">"
    NumSpeechActsZF = "<amount n=\""+str(SceneSpeakerstats[1])+"\" unit=\"speech_acts\"/>"
    NumLinesZF = "<amount n=\""+str(SceneSpeakerstats[2])+"\" unit=\"lines\"/>"
    NumWordsZF = "<amount n=\""+str(SceneSpeakerstats[3])+"\" unit=\"words\"/>"
    NumCharsZF = "<amount n=\""+str(SceneSpeakerstats[4])+"\" unit=\"chars\"/>"
    SceneSpeakerstatsZF = SceneSpeakerIDZF+"\n "+NumSpeechActsZF+"\n "+NumWordsZF+"\n "+NumLinesZF+"\n "+NumCharsZF+"\n</sp>"
    #print(SceneSpeakerstatsZF)
    return SceneSpeakerstatsZF


def add_acts(ProtoText, ActsCounter, ActsHeads):  
    """
    Adds an empty "div" structure for each act, as a place-holder for the scene data.
    Status: OK. 
    """
    ProtoText = re.sub("</text>", "<div type=\"act\" n=\""+str(ActsCounter)+"\">\n<head>"+ActsHeads[ActsCounter-1]+"</head>\n</div>\n</text>", ProtoText)
    return ProtoText
    

def add_scenes(ProtoText, ScenesCounter, ScenesHeads):
    """
    Adds an empty "div" structure for each scene as a place-holder for the scene data.
    Status: OK. 
    """
    #print(ScenesCounter)
    ProtoText = re.sub("</div>\n</text>", "<div type=\"scene\" n=\""+str(ScenesCounter)+"\">\n<head>"+ScenesHeads[ScenesCounter-1]+"</head>\n</div>\n</div>\n</text>", ProtoText)
    return ProtoText


def add_stats(ProtoText, SceneSpeakerstatsZF): 
    """
    Adds the Zwischenformat data for each scene into the appropriate place.
    Status: OK. 
    """
    ProtoText = re.sub("</div>\n</div>\n</text>", SceneSpeakerstatsZF+"</div>\n</div>\n</text>", ProtoText)
    return ProtoText            


def get_documentation(): 
    """
    Create the documentations section of the Zwischenformat.
    Currently just a placeholder.
    Status: INACTIVE. 
    """
    Documentation = "<documentation></documentation>"
    return Documentation


def get_closer():
    """
    This is simply necessary to make the Zwischenformat valid XML.
    Status: OK.
    """
    Closer = "</play>"
    return Closer


def build_zwischenformat(Processing, Header, Personae, Text, Closer):
    """
    Adds an empty "div" structure for each act, as a place-holder for the scene data.
    Status: OK. 
    """

    Zwischenformat = Processing +"\n"+ Header +"\n"+ Personae +"\n"+ Text + Closer
    return Zwischenformat


def save_result(Zwischenformat, Idno, OutFolder):
    """
    Save Zwischenformat data as an XML file. 
    Status: OK.
    """
    if not os.path.exists(OutFolder):
        os.makedirs(OutFolder)
    ZFFile = OutFolder+Idno+"_zf.xml"
    with open(ZFFile, "w") as OutFile: 
        OutFile.write(Zwischenformat)


def main(InPath, OutFolder): 
    """
    Set of functions to generate the DLINA Zwischenformat from TEI-P5-encoded dramatic texts.
    Each part (Processing Instructions, Header, Personae, Text, Documenation, Closer) are generated separatedly. 
    Then, these separate parts are joined together and saved. 
    Output is an XML file that conforms to the DLINA Zwischenformat. 
    """
    for File in glob.glob(InPath):
        Idno, Ext = os.path.basename(File).split(".")
        print("Now:", Idno)
        PlayXML = read_xml(File)
        Processing = get_processing(Idno)
        Header = create_header(PlayXML, Idno)
        Personae = create_personae(PlayXML)
        ActsXML, ActsHeads = get_acts(PlayXML)
        ActsCounter = 0
        ProtoText = "<text>\n</text>"
        for ActXML in ActsXML:
            ActsCounter +=1
            ProtoText = add_acts(ProtoText, ActsCounter, ActsHeads) 
            #print("Now act:", ActsCounter)
            ScenesXML, ScenesHeads = get_scenes(ActXML, ActsCounter)
            ScenesCounter = 0
            for SceneXML in ScenesXML:
                ScenesCounter +=1
                ProtoText = add_scenes(ProtoText, ScenesCounter, ScenesHeads)
                #print("Now scene:", ActsCounter, ScenesCounter)
                SceneSpeakersList, SceneSpeakersDict = get_speakers(SceneXML, ActsCounter, ScenesCounter)
                for SceneSpeakerID in SceneSpeakersList: 
                    #print("Now speaker", SceneSpeakerID)
                    SceneSpeakertextXML = get_speakertext(SceneXML, SceneSpeakerID, ActsCounter, ScenesCounter)
                    SceneSpeakerstats = get_speakerstats(SceneSpeakertextXML, SceneSpeakerID, SceneSpeakersDict)
                    SceneSpeakerstatsZF = SceneSpeakerstats_to_ZF(SceneSpeakerstats)
                    ProtoText = add_stats(ProtoText, SceneSpeakerstatsZF)
        Text = ProtoText
        #Documentation = get_documentation() 
        Closer = get_closer()
        Zwischenformat = build_zwischenformat(Processing, Header, Personae, Text, Closer)
        save_result(Zwischenformat, Idno, OutFolder)
    print("Done.")
        
main(InPath, OutFolder)
