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
    text = re.sub(r'([^\r\n<>])[\r\n]+([^\r\n<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'([^>$])\r\n *(<seg)', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(>)[\r\n]+([^\s<>])', r'\1 \2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p> +', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text)
    text = re.sub(r' +', r' ', text)
    text = re.sub(r'<p(>| [^>]*>)\s*</p>', r' ', text)
    return text


def deletingNonBody(text):
    """
        It deletes the possible several elements before and after the <body>
    """
    # Delete everything before <div id="obra">
    text = re.sub(r'<!DOCTYPE html>.*?(<div id="obra")', r"\1", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<!DOCTYPE html.*?<body>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<head(>| [^>]*>).*?</head>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<footer(>| [^>]*>).*?</footer>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<script(>| [^>]*>).*?</script>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?html(>| [^>]*>)', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</article></section>', r"", text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</section>\s*</main>', r"", text, flags=re.DOTALL|re.IGNORECASE)

    #Delete everything after </body>
    text = re.sub(r'</body>.*?</body>.*?</html>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</?body(>| [^>]*>)', r"", text, flags=re.DOTALL|re.IGNORECASE)
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
    text = re.sub(r'<font(>| [^>]*>).{0,2}[0-9]+.{0,2}</font>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<font(>| [^>]*>)(.*?)</font>', r'\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<sup(>| [^>]*>).*?</sup>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    #abr    
    
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
    text = re.sub(r'<p align="center">(.+?)</p>', r'<p>\1</p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p [^>]*?>\s*<hr.*?>\s*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p [^>]*?>\s*\* ?\* ?\*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p(>| [^>]*>)[\.\s]+?</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)

    # Replace spain foreign words and italics elements    
    text = re.sub(r'<span .*?lang="([^"]*)".*?>(.*?)</span>', r'<seg type="foreign" xml:lang="\1">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em(>| [^>]+)(.*?)</em>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i(>| [^>]+)(.*?)</i>', r'<seg rend="italics">\2</seg>', text, flags=re.DOTALL|re.IGNORECASE)

    return text


def replacingTables(text):
    """
    Replace tables with <quote> or <lg>
    """
    text = re.sub(r'<table width="70%" align="center">', r'<lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<table cellpadding="0" cellspacing="0" align="center" width="462">', r'<lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<td nowrap="yes">(.*?)</td>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)   
    text = re.sub(r'</table>(\s*(<p>|<h[1-6]>))', r'</lg>\1', text, flags=re.DOTALL|re.IGNORECASE)   
    text = re.sub(r'</?t[rd]>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<td align="right">', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<lg>\s*)<table[^>]*?>', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</table>(\s*</lg>)', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<td [^>]*>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<lg>\s*<lg>', r'<lg>', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'(\r?\n)([A-Z Á-ÚÜÑ,\.\-\?\!¡¿]{10,500})(\r?\n)', r'\1<ab>\2</ab>\3', text, flags=re.IGNORECASE)
    #Improvement: Actaully it would be better to work with this, but for some reason, it doesn't
    # text = re.sub(r'^([A-Z Á-ÚÜÑ,\.\-\?\!¡¿]{,10})$', r'<ab>\1</ab>', text, flags=re.IGNORECASE)
    return text

def replacingBold(text):
    """
    Replace <b> with <h3>. It doesn't work by default
    """
    text = re.sub(r'<b>( *- *[IVXDCL0-9]+ *- *)</b>', r'<h3>\1</h3>', text, flags=re.DOTALL|re.IGNORECASE)
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
        text = re.sub(r'(</p>|</ab>|</lg>)\s*?(<h2>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)

        # That closes the last <div> from <h2>
        text = re.sub(r'\Z', r'</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    else:
        print("<h3> found")
        # That opens the <div> of a <h3>
        text = re.sub(r'(</h2>)\s*?(<h3>)', r'\1\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the div of a <h3> and opens one more for a new <h3>
        text = re.sub(r'(</p>|</ab>|</lg>)\s*?(<h3>)', r'\1\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        # That closes the divs both from <h3> and <h2> and open another for <h2>
        text = re.sub(r'(</p>|</ab>|</lg>)\s*?(<h2>)', r'\1\r\n</div>\r\n</div>\r\n<div>\r\n\2', text, flags=re.DOTALL|re.IGNORECASE)
        
        # That closes the last divs from <h2> and <h3>
        text = re.sub(r'\Z', r'</div>\r\n</div>\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    #That changes the <hn> to <head> (also the closing tags!)      
    text = re.sub(r'<(/?)h[1-6]>', r'<\1head>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def settingTeiHeader(text):
    text = re.sub(r'\A',r'<?xml version="1.0" encoding="UTF-8"?>\r\n<?xml-model href="https://raw.githubusercontent.com/cligs/toolbox/master/tei/cligs.rnc" type="application/relax-ng-compact-syntax"?>\r\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude">\r\n	<teiHeader>\r\n		<fileDesc>\r\n			<titleStmt>\r\n				<title type="main"></title>\r\n				<title type="sub"></title>\r\n				<title type="short"></title>\r\n				<title type="idno">\r\n					<idno type="viaf"></idno></title>\r\n				<author>\r\n					<idno type="viaf"></idno>\r\n					<idno type="short"></idno>\r\n					<name type="full"></name>\r\n				</author>\r\n				<principal xml:id="jct">José Calvo Tello</principal>\r\n			</titleStmt>\r\n			<publicationStmt>\r\n                <publisher>CLiGS</publisher>\r\n				<availability status="publicdomain">\r\n                    <p>The text is freely available.</p>\r\n				</availability>\r\n				<date when="2015">2015</date>\r\n				<idno type="cligs">ne01</idno>\r\n			</publicationStmt>\r\n			<sourceDesc>\r\n				<bibl type="digital-source">\r\n					<date when="1000"></date>, <idno></idno>, <ref target="#"/>.\r\n				</bibl>\r\n				<bibl type="print-source">\r\n					<date when="1000"></date>\r\n				</bibl>\r\n				<bibl type="edition-first">\r\n					<date when="1000"></date>\r\n				</bibl>\r\n			</sourceDesc>\r\n		</fileDesc>\r\n		<encodingDesc>\r\n			<p>.</p>\r\n		</encodingDesc>\r\n		<profileDesc>\r\n			<abstract>\r\n				<p>.</p>\r\n			</abstract>\r\n			<textClass>\r\n				<keywords scheme="keywords.csv">\r\n					<term type="supergenre">narrative</term>\r\n					<term type="genre">novel</term>\r\n					<term type="subgenre" cert="low" resp="x"></term>\r\n					<term type="genre-label"></term>\r\n					<term type="narrative-perspective" cert="low" resp="jct"></term>\r\n					<term type="publication">book</term>\r\n					<term type="form">prose</term>\r\n					<term type="author-gender">male</term>\r\n					<term type="protagonist-gender">male</term>\r\n					<term type="setting">male</term>\r\n				</keywords>\r\n			</textClass>\r\n		</profileDesc>\r\n		<revisionDesc>\r\n			<change when="2015-08-13" who="#jct">Initial TEI version.</change>\r\n		</revisionDesc>\r\n	</teiHeader>\r\n    <text>\r\n    	<front>\r\n    	</front>\r\n    	<body>\r\n'    , text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'\Z', r'\r\n		</body>\r\n		<back>\r\n			<div>\r\n					<p></p>\r\n			</div>\r\n		</back>\r\n	</text>\r\n</TEI>', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def replacingBasicElementsFromEpubLibre(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    # Replace some elements with atributes with other cleaner elements
    text = re.sub(r'<p class="calibre[0-9]+">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="salto[0-9]+">', r'<milestone />\n<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="saltoc">', r'<milestone />\n<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="sinopsis">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="ilustra">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE) 
    text = re.sub(r'<div class="info">.*?</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<br class="calibre9" />', r' ', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<sup(|[^>]*)>\[[0-9]+\]</sup>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span(|[^>]*)>\s*</span>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<a(|[^>]*)>\s*</a>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(tlogo|tautor|ttitulo|trevision|tfirma)">.*?</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h1 class="ttitulo">.*?</h1>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<img[^>]*>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(bloque|ala)?derecha[0-9]*">(.*?)</p>', r'<ab>\2</ab>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="asangre">', r'<p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado1">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="(normal|calibre)[0-9]*">(.*?)</span>', r'<seg rend="italics">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p><span class="(cap[0-9]*|versalita|smallcaps)">(..?)</span>', r'<p>\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<span class="(versalita|smallcaps)[0-9]*">(.*?)</span>', r'<seg rend="smallcaps">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<div class="poema[0-9]*">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="verso">(.*?)</div>', r'<lg>\1</lg>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="normal1">(.*?)</p>', r'<l>\1</l>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="cursiva">(.*?)</p>', r'<p><seg rend="italics">\1</seg></p>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em(|[^>]*)>(.*?)</em>', r'<seg rend="italics">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<i(|[^>]*)>(.*?)</i>', r'<seg rend="italics">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span class="cursiva[0-9]*">(.*?)</span>', r'<seg rend="italics">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<sub(|[^>]*)>(.*?)</sub>', r'<seg rend="subscript">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<small(|[^>]*)>(.*?)</small>', r'<seg rend="small">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<span class="nosep">(.*?)</span>', r'<seg rend="italics">\1</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<strong(|[^>]*)>(.*?)</strong>', r'<seg rend="bold">\2</seg>', text, flags=re.IGNORECASE)
    text = re.sub(r'<p class="cita">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="micita">(.*?)</p>', r'<quote>\n<p>\1</p>\n</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Setting quotes in floatingText element
    text = re.sub(r'<div class="(mi)?cita">(.*?)</div>', r'<floatingText>\n<body>\n<div>\n\2\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    
    
    text = re.sub(r'<div class="bloquederecha1">(.+?)</div>', r'<quote>\1</quote>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="cursiva[0-9]*">', r'<div><!--italics-->', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="calibre" id="calibre_link-[0-9]+">', r'<div>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado">[… ]+?</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="asteriscos">[\* ]*</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="centrado">\[…\]</p>', r'<milestone />', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div class="banner">(.*?)</div>', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<html.*?<body>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</body></html>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</p>)\s*(<head>.*?</head>)', r'\1</div>\n<div>\n\2', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="(tsub|sub)?tit(ulo)?[0-9]*">(.*?)</p>', r'<head>\3</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<p class="epigrafe">(.*?)</p>', r'<head>\1</head>', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<head>\s*</head>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'</head>\s*<head>', r': ', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Cleaning some <milestone />
    text = re.sub(r'(<div>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</div>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(</head>\s*)<milestone />', r'\1', text, flags=re.DOTALL|re.IGNORECASE)

    # Setting some floatingTexts
    text = re.sub(r'(<div(| [^>]*?)>((?!<div).)*</div>)(\s*<p)', r'<floatingText>\n<body>\n\1\n</body>\n</floatingText>\n\4', text, flags=re.DOTALL|re.IGNORECASE)

    #text = re.sub(r'(<div(|[^>]+?)>.*?</div>)(\s*<p)', r'<floatingText>\n<body>\n<div>\n\1\n</div>\n</body>\n</floatingText>\n\3', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Floating Texts

    text = re.sub(r'<p(| [^>]+)>[\s\r\n]*</p>', r'', text, flags=re.DOTALL|re.IGNORECASE)

    text = re.sub(r'\n[ \t]+', r'\n', text, flags=re.IGNORECASE)
    text = re.sub(r'[\r\n]+', r'\r\n', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<div>[\r?\n]*</div>', r'', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'(<div>((?!<div>).)*</div>\r?\n)\Z', r'<!--\1-->', text, flags=re.DOTALL|re.IGNORECASE)



    text = re.sub(r'', r'', text, flags=re.DOTALL|re.IGNORECASE)

    return text

def lInLg(text):
    """
    It replaces some elements and its styles with TEI elements
    """
    while re.search(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', text, flags=re.DOTALL|re.IGNORECASE) is not None:
        text = re.sub(r'(<lg>)(((?!</lg>).)*?)<(/?)p>', r'\1\2<\4l>', text, flags=re.DOTALL|re.IGNORECASE)
    return text


listdocs=[
"ne0166_Blasco_Calafia"
]

i=0
for doc in listdocs:
    docFormatIn=doc+".html"    
    docFormatOut=doc+".xml"    

    with open(os.path.join("input",docFormatIn), "r", errors="replace", encoding="utf-8") as fin:
        content = fin.read()
    
        # it cleans the HTML from entities, etc        
        content=cleaningHTML(content)
        
        # It deletes elements before <body> and after </body>
        #content=deletingNonBody(content)
        
        #It deletes different kind of elements        
        #content=deletingElements(content)
        
        #It replaces some HTML elements with TEI elements    
        content=replacingBasicElementsFromEpubLibre(content)
        
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

        with open (os.path.join("output", docFormatOut), "w", encoding="utf-8") as fout:
            fout.write(content)
    print(doc)
    i+=1