# html2tei.py

# Function to transform HTML produced by FineReader or Calibre into simple, clean TEI files.
# Makes use of "re"; see: http://docs.python.org/2/library/re.html

# Basic structure
# - Open and read an HTML text file.
# - Replace HTML header with XML model header
# - Remove whitespace for better handling
# - Remove unnecessary attributes on elements
# - Turn HTML <i> into 'hi rend="italics"'
# - Turn <h1> etc. into divisions and heads
# - Do additional cleanup of remaining markup
# - Write new XML file to disk.



#######################
# Import statements   #
#######################

import re
import glob


#######################
# Functions           #
#######################

def add_teiheader(file,xmlmutandum,teiheader):
    """ Replaces the existing HTML header with a teiHeader and final TEI tags and saves as XML. Needs to come first."""
    with open(teiheader,"r") as teiheader:
        teiheader = teiheader.read()    
    with open(file,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<html><head>.*</head><body>",teiheader,mutandum)
        mutandum = re.sub("</body></html>","</div></body><back><div><p></p></div></back></text></TEI>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)
        
        
def remove_whitespace(xmlmutandum):
    """ Removes unwanted whitespace from the content of elements."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<p>\s","<p>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def remove_spans(xmlmutandum):
    """Removes all span elements and their attributes."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("([^>])\n([^<])",r"\1 \2",mutandum)
        mutandum = re.sub("<span.*?>(.*)</span>",r"\1",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def remove_paragraphclasses(xmlmutandum):
    """Removes class attributes on "p" elements from Calibre."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub(r'<p class="calibre5">',"<p>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)    


def convert_italics(xmlmutandum): 
    """Converts HTML-style italics into TEI-style italics"""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<i>(.*)</i>",r'<hi rend="italic">\1</hi>',mutandum)
        mutandum = re.sub(r'<i class="calibre6">(.*)</i>',r'<hi rend="italic">\1</hi>',mutandum)
        mutandum = re.sub("<span.*?>(.*)</span>","\1",mutandum)
        mutandum = re.sub("<i>","",mutandum)
        mutandum = re.sub("</i>","",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def unify_speeches(xmlmutandum):
    """Turns "emdash" and "endash" at beginning of "p" into "--"."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<p>&mdash;","<p>--",mutandum)
        mutandum = re.sub("<p>&ndash;","<p>--",mutandum)        
        mutandum = re.sub("<p>- ","<p>-- ",mutandum)        
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)    
        
        
def simplify_divs(xmlmutandum):
    """Removes all attributes from divs."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<div .*?>","<div>",mutandum)
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def convert_headings(xmlmutandum):
    """Removes all attributes from h1 and turns it into head."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<b>","",mutandum)     # Remove line if still meaningful "b" somewhere.
        mutandum = re.sub("</b>","",mutandum)    # Remove line if still meaningful "b" somewhere.
        mutandum = re.sub("<h1.*?>[<b>]?","<head>",mutandum)
        mutandum = re.sub("</h1>","</head>",mutandum)
        mutandum = re.sub("<a id=\"calibre_link-[\d]*\"></a>","",mutandum)
        mutandum = re.sub("<h2 id=\"calibre_link-[\d]*\">","<h2>",mutandum)
        mutandum = re.sub("<h2>(.*?) </h2>",r'<head>\1</head>',mutandum)        
        mutandum = re.sub("<h2>","<head>Chapitre ",mutandum)
        mutandum = re.sub("</h2>","</head>",mutandum)
        mutandum = re.sub(r'<div>\n<p>(.{1,15}?)</p>',r'<div><head>\1</head>',mutandum)        
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def cleanup_xml(xmlmutandum):
    """Several smaller deletions of possibly meaningless markup. Deactivate lines selectively as needed."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
        mutandum = re.sub("<br />"," ",mutandum)
        mutandum = re.sub("&nbsp;","",mutandum)
        mutandum = re.sub("&ndash;","--",mutandum)
        mutandum = re.sub("&mdash;","--",mutandum)
        mutandum = re.sub("\n[ ]?\n","\n",mutandum)
        mutandum = re.sub("<span>","",mutandum)        
        mutandum = re.sub("</span>","",mutandum)        
    with open(xmlmutandum,"w") as output:
        output.write(mutandum)


def write_xmloutput(file,xmlmutandum): 
    """Convenience function which saves transformed file to new filename. Needs to come last."""
    with open(xmlmutandum,"r") as mutandum:
        mutandum = mutandum.read()
    xmloutput = file[:-5] + ".xml"                       # Builds filename for outputfile from original filenames but correct extension.
    with open(xmloutput,"w") as output:
        output.write(mutandum)
        

#######################
# Main                #
#######################


def main(inputpath,xmlmutandum,teiheader):
    for file in glob.glob(inputpath):
        add_teiheader(file,xmlmutandum,teiheader)
        remove_whitespace(xmlmutandum) 
        remove_spans(xmlmutandum)
        remove_paragraphclasses(xmlmutandum)
        convert_italics(xmlmutandum)
        unify_speeches(xmlmutandum)
        simplify_divs(xmlmutandum)
        convert_headings(xmlmutandum)
        cleanup_xml(xmlmutandum)
        write_xmloutput(file,xmlmutandum)

            
main('./input/Kernok.html',"MUTANDUM.xml","teiHeader.xml")

