# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/jose/.spyder2/.temp.py
"""
import re
import os
import html.parser

def cleaningHTML(text):
    """
        It decodes the HTML entities and it deletes some anoying characters
    """
    # HTML-Entities decodieren
    h = html.parser.HTMLParser()
    text = h.unescape(content)
    
    # Geschützte Leerzeichen löschen
    text = re.sub('\u00A0', " ", text)
    return text

def cleaningIndent(text):
    """
    Cleaning the HTML indent
    """
    text = re.sub(r'^[\s \t]+', r'', text)
    text = re.sub(r'[\s \t]+$', r'', text)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    text = re.sub(r'(<(/p|/h[1-6]|/?div|/head|/l|/?lg|/?body|/?back|/?text|/?front)>)', r'\1\r\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([^\s<>])[\r\n]+([^\s<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([^>$])\r?\n\s*(<seg)', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(>)[\r\n]+([^\s<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p> +', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    return text


def deletingNonBody(text):
    """
        It deletes the possible several elements before and after the <body>
    """
    # Delete everything before <div id="obra">
    text = re.sub(r'<!DOCTYPE html>.*?(<div id="obra")', r"\1", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<!DOCTYPE html.*?<body>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    #Delete everything after </body>
    text = re.sub(r'</body>.*?</body>.*?</html>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    return text

def deletingElements(text):
    """
    Delete different tags
    """
    text = re.sub(r'</?a(>| [^>]*>)', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?br(>| [^>]*>)', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<img[^>]*>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span style="font-style:normal;">(.*?)</span>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<font(>| [^>]*>)(.*?)</font>', r'\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', r'', text, flags=re.DOTALL|re.IGNORECASE)
    return text

def replacingBasicElements(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    # Replace some elements with atributes with other cleaner elements
    text = re.sub(r'<p style="text-align: justify;text-indent:30px;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="text-align: justify;text-indent:30px;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="text-align: right;text-indent:30px;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="font-size:12pt;text-align: justify;text-indent:30px;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="text-align: justify;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="font-size:12pt;text-align: right;text-indent:30px;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p style="font-size:12pt;text-align: justify;">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p [^>]*?>\s*<hr.*?>\s*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p [^>]*?>\s*\* \* \*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)

    # Replace spain foreign words and italics elements    
    text = re.sub(r'<span .*?lang="([^"]*)".*?>(.*?)</span>', r'<seg type="foreign" xml:lang="\1">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em(>| [^>]+)(.*?)</em>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i(>| [^>]+)(.*?)</i>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(\r?\n)([A-Z Á-ÚÜÑ,\.\-\?\!¡¿]{10,500})(\r?\n)', r'\1<ab>\2</ab>\3', text, flags=re.IGNORECASE)
    #Improvement: Actaully it would be better to work with this, but for some reason, it doesn't
    # text = re.sub(r'^([A-Z Á-ÚÜÑ,\.\-\?\!¡¿]{,10})$', r'<ab>\1</ab>', text, flags=re.IGNORECASE)

    return text

def replacingTables(text):
    """
    Replace tables with <quote> or <lg>
    """
    text = re.sub(r'<table width="70%" align="center">', r'<lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<table cellpadding="0" cellspacing="0" align="center" width="462">', r'<lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<td nowrap="yes">(.*?)</td>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)   
    text = re.sub(r'</table>(\s*<p>)', r'</lg>\1', text, flags=re.DOTALL|re.IGNORECASE)   
    text = re.sub(r'</?t[rd]>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<td align="right">', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<lg>\s*)<table[^>]*?>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</table>(\s*</lg>)', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    return text

def setDivs(text):
    """
    Setting the <div>s searching for the <hn>
    """
    #It takes in the <hn> the textual information about the chapter or part
    text = re.sub(r'(</h[1-5]>)[\s]+([^<\r\n ][^\r\n]*)([\r\n]*)', r' : \2 \1\3', text, flags=re.DOTALL|re.IGNORECASE)

    # It deletes the <h1> and its next <p>
    text = re.sub(r'<h1.*?\r?\n<p.*?\r?\n', r'', text, flags=re.DOTALL|re.IGNORECASE)

    # It deletes the <h1> and its next <p>
    text = re.sub(r'(\A.*?)(<h[2-4])', r'\1<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)


    # It it looks in the document if there is any <h3>. If there is, then it will close the divs both from h2 and h3        
    listh3=re.findall("<h3",text)
    if not listh3:
        print("<h3> not found")
        # That closes the <div> of an <h2> and opens another one
        text = re.sub(r'(</p>|</ab>)\s*?(<h2>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)

        # That closes the last <div> from <h2>
        text = re.sub(r'\Z', r'</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    else:
        print("<h3> found")
        # That opens the <div> of a <h3>
        text = re.sub(r'(</h2>)\s*?(<h3>)', r'\1\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the div of a <h3> and opens one more for a new <h3>
        text = re.sub(r'(</p>|</ab>)\s*?(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the divs both from <h3> and <h2> and open another for <h2>
        text = re.sub(r'(</p>|</ab>)\s*?(<h2>)', r'\1\r\n</div>\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        
        # That closes the last divs from <h2> and <h3>
        text = re.sub(r'\Z', r'</div>\r\n</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    #That changes the <hn> to <head> (also the closing tags!)      
    text = re.sub(r'<(/?)h[1-6]>', r'<\1head>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno"><idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<idno type="cligs"></idno>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="y"></principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="restricted">\r\n                    <!-- Optionen: restricted, publicdomain, unknown. -->\r\n					<p>Files prepared for personal research use only. Not for publication.</p>\r\n				</availability>\r\n				<date></date>\r\n				<idno type="cligs"><!--[a-z]{2}[0-9]{4}, z.B. ne0034 --></idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source">\r\n					<date></date>, <idno></idno>, <ref target="#"/>.\r\n				</bibl>\r\n				<bibl type="print-source">\r\n					<date></date>\r\n				</bibl>\r\n				<bibl type="edition-first">\r\n					<date></date>\r\n				</bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p></p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract>\r\n				<p></p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv">\r\n					<term type="supergenre"></term>\r\n					<term type="genre" cert="high"></term>\r\n					<term type="subgenre" cert="low" resp="x"></term>\r\n					<term type="genre-label"></term>\r\n					<term type="narrative-perspective"></term>\r\n					<term type="form"></term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2015" who="#">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    return text

listdocs=["Bazan_Dulce_ne086.html","Bazan_Insolacion_ne079.html","Bazan_Milagros_ne080.html","Bazan_Naturaleza_ne078.html","Bazan_Novios.html","bazan_Pascual_ne088.html","Bazan_Pazos_ne077.html","Bazan_Piedra_ne082.html","Bazan_Prueba_ne083.html","Bazan_Quimera_ne084.html","Bazan_Sirena_ne085.html","Bazan_Solteron_ne081.html"]
listdocs=["Bazan_Pazos_ne077.html"]

i=0
for doc in listdocs:
    
    with open(os.path.join("input",doc), "r", errors="replace") as fin:
        content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=cleaningHTML(content)
        
        # It deletes elements before <body> and after </body>
        content=deletingNonBody(content)
        
        #It deletes different kind of elements        
        content=deletingElements(content)

        #It cleans the white space
        content=cleaningIndent(content)
        
        #It replaces some HTML elements with TEI elements    
        content=replacingBasicElements(content)
        
        #It cleans the white space
        content=cleaningIndent(content)
    
        #It replaces the tables with <lg>
        content=replacingTables(content)   
    
        #It cleans the white space, again
        content=cleaningIndent(content)
        
        #It sets divs 
        content=setDivs(content)
        
        #We introduce the teiHeader
        content=settingTeiHeader(content)
        
        # And once again
        content=cleaningHTML(content)
        
        # Improvement!: That should actually save the document as xml

        # It writes the result in the output folder
        with open (os.path.join("output", doc), "w") as fout:
            fout.write(content)
    print(doc)
    i+=1