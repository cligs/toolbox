# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import html.parser
import glob

def upper_repl(match):
     return match.group(1).upper()

def cleaningHTML(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    # HTML-Entities decodieren
    h = html.parser.HTMLParser()
    text = h.unescape(text)
    
    # Geschützte Leerzeichen löschen
    text = re.sub('\u00A0', " ", text)
    return text


def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<idno type="short"></idno>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="publicdomain">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2015">2015</date>\r\n				<idno type="cligs">ne01</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source"><date when="1000"></date>, <idno></idno>, <ref target="#"/>, <ref target="#"/>.</bibl>\r\n				<bibl type="print-source"><date when="1000"></date></bibl>\r\n				<bibl type="edition-first"><date when="1000"></date></bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract>\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv">\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" cert="low" resp="x"></term>\r\n					<term type="genre-label"></term>\r\n					<term type="narrative-perspective" cert="low" resp="#jct"></term>\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="author-gender">male</term>\r\n					<term type="protagonist-gender">male</term>\r\n					<term type="setting"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2015-08-13" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z', r'\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def replacingBasicElementsFromArchive(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    text = re.sub(r'^(.+)$', r'<p>\1</p>', text, flags=re.MULTILINE)


    #Cleaning some white space
    text = re.sub(r'^ +', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<p>—) *', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    # Delete the name of the work
    text = re.sub(r'(<p>[^a-záéíóúñüí]{20,30}</p>)', r'', text, flags=re.DOTALL)

    text = re.sub(r'(<p>.?[0-9]+.?</p>)', r'', text, flags=re.DOTALL)


    # Trying to fix the lines that the pdf broke
    text = re.sub(r'-</p>\s*<p>([a-zéíóúáñ])', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([a-zéíóúáñ,])</p>\s*<p>([a-zéíóúáñ])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'-</p>\s*<p>([a-zéíóúáñ])', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([a-zéíóúáñ,])</p>\s*<p>([a-zéíóúáñ])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)


    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def lInLg(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    while re.search(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', text, flags=re.DOTALL|re.IGNORECASE) is not None:
        text = re.sub(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', r'\1\2<\4l>', text, flags=re.DOTALL|re.IGNORECASE)
    return text


def main():
    i=1
    for doc in glob.glob("input/*.txt"):
    
        # It takes the base name of the html file, it cuts its ending and keeps a new xml name
        basenamedoc = os.path.basename(doc)[:-3]  
        docFormatOut=basenamedoc+"xml"    
    
        with open(doc, "r", errors="replace", encoding="utf-8") as fin:
            content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=cleaningHTML(content)
        
        # It deletes elements before <body> and after </body>
        #content=deletingNonBody(content)
        
        #It deletes different kind of elements        
        #content=deletingElements(content)
        
        #It replaces some HTML elements with TEI elements    
        content=replacingBasicElementsFromArchive(content)
        
        #It cleans the white space
        #content=cleaningIndent(content)
    
        #It replaces the tables with <lg>
        #content=replacingTables(content)   
    
        #It cleans the white space, again
        #content=cleaningIndent(content)
        
        #It replaces <b> with <h3>. Uncomment to use it!
        #content=replacingBold(content)         
        
        #It sets divs 
        #content=setDivs(content)
        
        #We introduce the teiHeader
        content=settingTeiHeader(content)
        
        # And once again
        #content=cleaningHTML(content)
        
        # Improvement!: That should actually save the document as xml

        # It writes the result in the output folder

        content=lInLg(content)

     
            
            # It writes the result in the output folder
    
        with open (os.path.join("output", docFormatOut), "w", encoding="utf-8") as fout:
                fout.write(content)
        print(doc)
        print("Processed documents: ",i)
        i+=1

main()