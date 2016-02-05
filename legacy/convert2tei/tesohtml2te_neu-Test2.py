# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Filename: tesohtml2tei.py

"""
# Function to transform html plays from TESO into simple, clean TEI files.
"""

import re
import glob
import os
import html  #Nötig für die Umwandlung der entities


#######################
# Functions           #
#######################

def html2tei(file,teiheader,outputdir):
    with open(file,"r") as sourcefile:
        h_text = sourcefile.read()
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        print("Now working on: " + str(textname))


        ##########################################################################################
        #### Preliminary text preparation                                                     ####
        ##########################################################################################

        # Turn entities into characters whenever legal
        """
        h_text = re.sub("&agrave;","à",h_text)
        h_text = re.sub("&egrave;","è",h_text)
        h_text = re.sub("&igrave;","ì",h_text)
        h_text = re.sub("&ograve;","ò",h_text)
        h_text = re.sub("&ugrave;","ù",h_text)
        h_text = re.sub("&aacute;","á",h_text)
        h_text = re.sub("&eacute;","é",h_text)
        h_text = re.sub("&iacute;","í",h_text)
        h_text = re.sub("&oacute;","ó",h_text)
        h_text = re.sub("&uacute;","ú",h_text)
        h_text = re.sub("&acirc;","â",h_text)
        h_text = re.sub("&ecirc;","ê",h_text)
        h_text = re.sub("&icirc;","î",h_text)
        h_text = re.sub("&ocirc;","ô",h_text)
        h_text = re.sub("&ucirc;","û",h_text)
        h_text = re.sub("&ntilde;","ñ",h_text)
        h_text = re.sub("&ccedil;","ç",h_text)
        """
        
        ## TODO: Funktion für obiges finden. In Uni Testen
        
        h_text = html.unescape(h_text)
        #Wandelt alle entities in Umlaute um, benötigt import html
        
        
        # Mark ampersand with entities
        h_text = re.sub("&c.","&amp;c.",h_text)
        
        #print (h_text)



        ##########################################################################################
        #### Preparatory text segmentation into: header, front, body, back, finale.           ####
        ##########################################################################################

        """
        h_header = re.findall("<HTML>([^%]*?)<CENTER>Preliminares de obra", h_text, re.DOTALL)
        h_header = str(h_header)
        #print(textname, h_header)
        
        """

		## TODO: "[^%]*?" "jedes beliebige Zeichen"; durch bessere Lösung ersetzen; 
        h_header = re.findall("<HTML>(?s).*<CENTER>Preliminares de obra", h_text, re.DOTALL)
        h_header = str(h_header)
        #print(textname, h_header)
        
        
        """
        der Modifikator (?s) setzt die Zeilenumbrüche für den folgenden Ausdruck .* aus. 
        Der Ausdruck .* findet somit den gesamten Inhalt ungehindert der Zeilenumbrüche
        """
        
        h_front = re.findall("<BR><H4><CENTER>Preliminares de obra([^§]*?)<BR><H4><CENTER>Texto de obra", h_text, re.DOTALL)
        h_front = str(h_front)
        #print(textname, h_front)

        h_body = re.findall("<BR><H4><CENTER>Texto de obra </CENTER></H4>([^%]*)", h_text, re.DOTALL)
        h_body = str(h_body)
        h_body = h_body[2:-2]
        #print(textname, h_body)

        h_back = re.findall("<BR><H4><CENTER>Finales de obra([^§]*)", h_text, re.DOTALL)
        h_back = str(h_back)
        h_back = re.findall("<BR><CENTER><STRONG><?E?M?>?([^§]*?)<?/?E?M?>?</STRONG></CENTER>", h_back, re.DOTALL)
        h_back = str(h_back)
        h_back = h_back[2:-2]
        #print(h_back)

        t_finale = "</text></TEI>"



        ##########################################################################################
        #### Work on the separate text segments                                               ####
        ##########################################################################################



        #################
        #### header  ####
        #################

        # Read empty header
        with open(teiheader,"r") as infile:
            t_header = infile.read()

        # Identify and add source description
        source_stmt = re.findall("Información bibliográfica sobre el texto original:[^§]*?<P>Este", h_header, re.DOTALL)
        if len(source_stmt) > 0:
            source_stmt = source_stmt[0]
            source_stmt = str(source_stmt)
        else:
            source_stmt = "n.av."
        source_stmt = re.sub("Información bibliográfica sobre el texto original:", "", source_stmt)
        source_stmt = re.sub("<P>Este", "", source_stmt)
        source_stmt = re.sub("<P>Nota:</P>\n<P>Errores en numeración</P>", "", source_stmt)
        source_stmt = re.sub("<EM>", "", source_stmt)
        source_stmt = re.sub("</EM>", "", source_stmt)
        source_stmt = re.sub("<STRONG>", "", source_stmt)
        source_stmt = re.sub("</STRONG>", "", source_stmt)
        source_stmt = re.sub("<BR>", "", source_stmt)
        source_stmt = re.sub("</BR>", "", source_stmt)
        source_stmt = re.sub(r"\\n", " ", source_stmt)
        source_stmt = re.sub("  ", " ", source_stmt)
        source_stmt = re.sub("  ", " ", source_stmt)
        source_stmt = re.sub(" ,", ",", source_stmt)
        source_stmt = re.sub(" Madrid", ". Madrid", source_stmt)
        source_stmt = re.sub("<P>[^§]*", "", source_stmt)
        #print(source_stmt)
        t_header = re.sub("<p>Digitized from:</p>", "<p>Digitized from: " + source_stmt + "</p>", t_header)

        # Identify and add publication date
        date_stmt = re.findall("\(\d{4}\)",h_header)
        if len(date_stmt) > 0:
            date_stmt = date_stmt[0]
            date_stmt = date_stmt[1:-1]
        else:
            date_stmt = "n.av."
        t_header = re.sub("<date></date>", "<date>" + date_stmt + "</date>", t_header)

        # Identify and add author name
        basename = os.path.basename(file)
        textname, ext = os.path.splitext(basename)
        index = textname.find('_')
        author_name = textname[:index]
        t_header = re.sub("<author></author>", "<author>" + author_name + "</author>", t_header)

        # Full author names (ASCII)
        t_header = re.sub("<author>Calderon</author>","<author><surname>Calderon de la Barca</surname><forename>Pedro</forename></author>",t_header)
        t_header = re.sub("<author>Vega</author>","<author><surname>Lope de Vega</surname><forename>Felix</forename></author>",t_header)
        t_header = re.sub("<author>Tirso</author>","<author><surname>Tirso de Molina</surname></author>",t_header)
        t_header = re.sub("<author>Diamante</author>","<author><surname>Diamante</surname><forename>Juan Bautista</forename></author>",t_header)
        t_header = re.sub("<author>Cueva</author>","<author><surname>Cueva</surname><forename>Juan de la</forename></author>",t_header)
        t_header = re.sub("<author>Benavente</author>","<author><surname>Quinones de Benavente</surname><forename>Luis</forename></author>",t_header)
        t_header = re.sub("<author>Castro</author>","<author><surname>Guillen de Castro</surname></author>",t_header)
        t_header = re.sub("<author>Cervantes</author>","<author><surname>Cervantes Saavedra</surname><forename>Miguel de</forename></author>",t_header)
        t_header = re.sub("<author>Matos</author>","<author><surname>Matos Fragoso</surname><forename>Juan de</forename></author>",t_header)
        t_header = re.sub("<author>Moreto</author>","<author><surname>Moreto</surname><forename>Agustin</forename></author>",t_header)
        t_header = re.sub("<author>Perez</author>","<author><surname>Perez de Montalban</surname><forename>Juan</forename></author>",t_header)
        t_header = re.sub("<author>Rojas</author>","<author><surname>Rojas Zorrilla</surname><forename>Francisco de</forename></author>",t_header)
        t_header = re.sub("<author>Rueda</author>","<author><surname>Rueda</surname><forename>Lope de</forename></author>",t_header)
        t_header = re.sub("<author>Ruiz</author>","<author><surname>Ruiz de Alarcon y Mendoza</surname><forename>Juan</forename></author>",t_header)
        t_header = re.sub("<author>Solis</author>","<author><surname>Solis</surname><forename>Antonio de</forename></author>",t_header)
        t_header = re.sub("<author>Rueda</author>","<author><surname>Rueda</surname><forename>Lope de</forename></author>",t_header)
        t_header = re.sub("<author>Zamora</author>","<author><surname>Zamora</surname><forename>Antonio</forename></author>",t_header)

        # Identify and add TESO and CLGS ids
        teso_id =  textname.split('_')[1]
        t_header = re.sub("<idno type=\"teso\"></idno>", "<idno type=\"teso\">" + teso_id + "</idno>", t_header)
        clgs_id = textname.split('_')[2]
        t_header = re.sub("<idno type=\"clgs\"></idno>", "<idno type=\"clgs\">" + clgs_id + "</idno>", t_header)

        subtitle = re.findall("</FONT>[^§]*?<BR><BR>([^§]*?)<BR>", h_header) #fixme
        if len(subtitle) > 0:
            subtitle = subtitle[0]
            subtitle = str(subtitle)
            subtitle = re.sub("[.].*", "", subtitle, re.DOTALL) #fixme
        else:
            subtitle = "n.av."
        t_header = re.sub("<title type=\"sub\"></title>", "<title type=\"sub\">" + subtitle + "</title>", t_header)

        maintitle = re.findall("<BR><FONT SIZE=\"\+1.5\">([^§]*?)</FONT>", h_header)
        if len(maintitle) > 0:
            maintitle = maintitle[0]
            maintitle = str(maintitle)
            maintitle = maintitle[:-1]
        else:
            maintitle = "n.av."
        t_header = re.sub("<title type=\"main\"></title>", "<title type=\"main\">" + maintitle + "</title>", t_header)



        #################
        #### front   ####
        #################

        # castList
        h_casthead = re.findall("<CENTER><TR><TH COLSPAN=\"2\"><BR>([^<]*).<BR></TH></TR></CENTER>", h_front)
        #print(textname, h_casthead)
        if len(h_casthead) > 0:
            h_casthead = h_casthead[0]
            h_casthead = str(h_casthead)
        else:
            h_casthead = "n.av."
        t_casthead = "<head>" + h_casthead + "</head>"

        h_castitems = re.findall("<TD VALIGN=\"top\">([^§]*?)</TD></TR>", h_front)
        t_castitems = ""
        for castitem in h_castitems:
            castitem = "<castItem><role>" + castitem + "</role></castItem>\n"
            t_castitems = t_castitems + castitem
        #print(textname, t_castitems)

        t_frontstart = "<front>"
        t_frontend = "</front>"
        t_caststart = "<div><castList>"
        t_castend = "</castList></div>"

        t_front = t_frontstart + t_caststart + t_casthead + t_castitems + t_castend + t_frontend
        #print(t_front)




        #################
        #### body    ####
        #################

        # Fix newlines and spaces
        h_body = re.sub("\\\\n","\n", h_body)
        h_body = re.sub("[\\\][x][a][0]", " ", h_body)


        # Remove some potential interferences
        h_body = re.sub("<BR><BR><SMALL><FONT COLOR=RED>\[Página\]</FONT></SMALL><BR><BR>", "", h_body)
        h_body = re.sub("<BR><SMALL><FONT COLOR=RED>\[Página\]</FONT></SMALL><BR>", "", h_body)
        h_body = re.sub("<SMALL><FONT COLOR=RED>\[Página\]</FONT></SMALL>", "", h_body)
        h_body = re.sub("<SMALL><FONT COLOR=RED>\[(\d*?)\]</FONT></SMALL>", "", h_body)
        h_body = re.sub("<BR><BR><SMALL><FONT COLOR=RED>\[Página\s(\d+)\]</FONT></SMALL><BR><BR>", "", h_body)
        h_body = re.sub("<BR><SMALL><FONT COLOR=RED>\[Página\s(\d+)\]</FONT></SMALL><BR>", "", h_body)
        h_body = re.sub("<SMALL><FONT COLOR=RED>\[Página\s(\d+)\]</FONT></SMALL>", "", h_body)
        h_body = re.sub("<FONT COLOR=RED> / </FONT>","",h_body)


        # Division heads
        h_body = re.sub("<BR><H4><CENTER>Finales de obra </CENTER></H4>", "", h_body)
        h_body = re.sub("<BR><H4><CENTER>([^§]*?)</CENTER></H4>","</div><div><head>\\1</head>", h_body)
        
        ## TODO: "div" am Anfang des Body: zu viele divs.

        # Body: Speakers
        h_body = re.sub("<BR><STRONG><EM>([^§]*?)</EM></STRONG>", "</sp><sp><speaker>\\1</speaker>", h_body)
        h_body = re.sub("<STRONG><EM>([^§]*?)</EM></STRONG>", "</sp><sp><speaker>\\1</speaker>", h_body)
        #h_body = re.sub("<BR><EM>([^§]*?)<STRONG><EM>([^§]*?)</EM></STRONG></EM><BR><BR>", "<sp>\n<speaker>\\1 \\2</speaker>", h_body)
        h_body = re.sub("<speaker> ", "<speaker>", h_body)
        h_body = re.sub("</sp><sp><speaker>", "<sp><speaker>", h_body, count=1)

        # Body: Stage directions
        h_body = re.sub("<P ALIGN=CENTER><EM>([^§]*?)\.</EM></P>","<stage>\\1</stage>",h_body, re.M)
        h_body = re.sub("<P ALIGN=CENTER><EM>([^§]*?)</EM></P>","<stage>\\1</stage>",h_body, re.M)
        h_body = re.sub("<P ALIGN=CENTER><EM>([^§]*?)</EM></P>","<stage>\\1</stage>",h_body, re.M)
        h_body = re.sub("<P ALIGN=CENTER>([^§]*?)\.?</P>","<stage>\\1</stage>",h_body, re.M)
        h_body = re.sub("<P ALIGN=CENTER>([^§]*?)</P>","<stage>\\1</stage>",h_body, re.M)
        h_body = re.sub("<EM>([^§]*?)</EM>","<stage>\\1</stage>",h_body, re.M)

        # Body: Speaker text
        h_body = re.sub("<BR><BR>([^§]*?)\n", "<l>\\1</l>\n", h_body)
        h_body = re.sub("<BR>([^§]*?)\n", "<l>\\1</l>\n", h_body)
        h_body = re.sub("<BR></l>", "</l>", h_body)
        h_body = re.sub("<l></l>", "", h_body)
        #h_body = re.sub("<l>\n", "", h_body)
        h_body = re.sub("<P>([^§]*?)</P>", "<p>\\1</p>", h_body)
        h_body = re.sub("<l>[\s]{4,50}", "<l part=\"final\">", h_body)


        # Some more cleaning up
        h_body = re.sub("<stage>([^§]{3,10})</sp><sp><speaker>", "<stage>\\1<speaker>", h_body, re.DOTALL)
        h_body = re.sub("<P ALIGN=CENTER>", "", h_body)
        h_body = re.sub("<P ALIGN=CENTER><stage>", "<stage>", h_body)
        h_body = re.sub("</stage></P>", "</stage>", h_body)
        h_body = re.sub("</stage></P>", "</stage>", h_body)

        h_body = re.sub("<l><div><head>", "<div><head>", h_body)
        h_body = re.sub("</head></l>", "</head>", h_body)
        h_body = re.sub("<l></div><div><head>", "<head>", h_body, count=1)

        h_body = re.sub("<l><stage>", "<stage>", h_body)
        h_body = re.sub("</stage></l>", "</stage>", h_body)



        # Remaining stage directions
        h_body = re.sub("<l><EM>([^§]*?)</EM></l>", "<stage>\\1</stage>", h_body)
        h_body = re.sub("<EM>([^§]*?)</EM>","<stage>\\1</stage>",h_body)

        # Remove end of html text
        h_body = re.sub("<P><FONT SIZE=\"2\">Envie sus sugerencias[^§]*</HTML>", "", h_body, re.M)
        h_body = re.sub("<p><FONT SIZE=\"2\">Envie sus sugerencias[^§]*</HTML>", "", h_body, re.M)
        h_body = re.sub("<CENTER><STRONG>FIN.</STRONG></CENTER>", "", h_body)
        h_body = re.sub("<CENTER><STRONG>FIN.</STRONG></CENTER>", "", h_body)

        # And yet some more cleaning up.
        h_body = re.sub("</stage></P>", "</stage>", h_body)
        h_body = re.sub("<BR>", "", h_body)



        # Putting the body parts together again
        t_bodytext = h_body
        t_bodystart = "<body><div>"
        t_bodyend = "</sp></div></body>"
        t_body = t_bodystart + t_bodytext + t_bodyend


        #################
        #### back    ####
        #################

        t_back = re.sub("<BR><CENTER><STRONG><?E?M?>?([^§]*?)<?/?E?M?>?</STRONG></CENTER>", "<back><div><p>\\1</p></div></back>", h_back)
        t_back = re.sub(r"\\n", " ", t_back)
        t_back = re.sub(r"[\\]", "", t_back)
        if len(t_back) < 5:
            t_back = "<back><div><p/></div></back>"
        #print(tei_back)



        #################
        #### finale  ####
        #################

        t_finale = t_finale


    ####################################################################
    #### Putting all the separate parts of the text into one        ####
    ####################################################################


    ### Concatenate the separate parts of the text into one.
    t_text = t_header + t_front + t_body + t_back + t_finale


    ### Save complete text to new file
    filename = os.path.basename(file)[:-5] + ".xml"
    with open("./tei/" + filename,"w") as outputfile:
        outputfile.write(t_text)




    ##########################################################################################
    #### Extract some basic metadata                                                      ####
    ##########################################################################################


def get_metadata(inputpath):
    all_metadata = "idno,author,date,title,subtitle,tesoid\n"
    for file in glob.glob(inputpath):
        with open(file,"r") as sourcefile:
            h_text = sourcefile.read()

            h_header = re.findall("<HTML>([^§]*?)<CENTER>Preliminares de obra", h_text, re.DOTALL)
            h_header = str(h_header)

            # Turn entities into characters whenever legal
            h_header = re.sub("&agrave;","à",h_header)
            h_header = re.sub("&egrave;","è",h_header)
            h_header = re.sub("&igrave;","ì",h_header)
            h_header = re.sub("&ograve;","ò",h_header)
            h_header = re.sub("&ugrave;","ù",h_header)
            h_header = re.sub("&aacute;","á",h_header)
            h_header = re.sub("&eacute;","é",h_header)
            h_header = re.sub("&iacute;","í",h_header)
            h_header = re.sub("&oacute;","ó",h_header)
            h_header = re.sub("&uacute;","ú",h_header)
            h_header = re.sub("&acirc;","â",h_header)
            h_header = re.sub("&ecirc;","ê",h_header)
            h_header = re.sub("&icirc;","î",h_header)
            h_header = re.sub("&ocirc;","ô",h_header)
            h_header = re.sub("&ucirc;","û",h_header)
            h_header = re.sub("&ntilde;","ñ",h_header)
            h_header = re.sub("&ccedil;","ç",h_header)
            h_header = re.sub("&c.","&amp;c.",h_text)


            date_stmt = re.findall("\(\d{4}\)",h_header)
            if len(date_stmt) > 0:
                date_stmt = date_stmt[0]
                date_stmt = date_stmt[1:-1]
            else:
                date_stmt = "n.av."

            basename = os.path.basename(file)
            textname, ext = os.path.splitext(basename)
            index = textname.find('_')
            author_name = textname[:index]

            teso_id =  textname.split('_')[1]
            clgs_id = textname.split('_')[2]

            subtitle = re.findall("</FONT>[^§]*?<BR><BR>([^§]*?)<BR>", h_header) #fixme
            if len(subtitle) > 0:
                subtitle = subtitle[0]
                subtitle = str(subtitle)
                subtitle = re.sub("[.].*", "", subtitle, re.DOTALL) #fixme
            else:
                subtitle = "n.av."
            subtitle = re.sub(" ", "-", subtitle)
            subtitle = re.sub("\n", "", subtitle)
            #print(subtitle)

            maintitle = re.findall("<BR><FONT SIZE=\"\+1.5\">([^§]*?)</FONT>", h_header)
            if len(maintitle) > 0:
                maintitle = maintitle[0]
                maintitle = str(maintitle)
                maintitle = maintitle[:-1]
            else:
                maintitle = "n.av."
            maintitle = re.sub(" ", "-", maintitle)
            maintitle = re.sub(",", "-", maintitle)
            maintitle = re.sub("--", "-", maintitle)

            metadata = clgs_id +","+ author_name +","+ date_stmt +","+ maintitle +","+ subtitle +","+ teso_id +"\n"
            #print(metadata)

        all_metadata = all_metadata + metadata

        # Turn entities into characters whenever legal
        all_metadata = re.sub("&agrave;","à",all_metadata)
        all_metadata = re.sub("&egrave;","è",all_metadata)
        all_metadata = re.sub("&igrave;","ì",all_metadata)
        all_metadata = re.sub("&ograve;","ò",all_metadata)
        all_metadata = re.sub("&ugrave;","ù",all_metadata)
        all_metadata = re.sub("&aacute;","á",all_metadata)
        all_metadata = re.sub("&eacute;","é",all_metadata)
        all_metadata = re.sub("&iacute;","í",all_metadata)
        all_metadata = re.sub("&oacute;","ó",all_metadata)
        all_metadata = re.sub("&uacute;","ú",all_metadata)
        all_metadata = re.sub("&acirc;","â",all_metadata)
        all_metadata = re.sub("&ecirc;","ê",all_metadata)
        all_metadata = re.sub("&icirc;","î",all_metadata)
        all_metadata = re.sub("&ocirc;","ô",all_metadata)
        all_metadata = re.sub("&ucirc;","û",all_metadata)
        all_metadata = re.sub("&ntilde;","ñ",all_metadata)
        all_metadata = re.sub("&ccedil;","ç",all_metadata)
        all_metadata = re.sub("&c.","&amp;c.",all_metadata)

        #print(all_metadata)

        with open("teatroespanol.csv", "w") as outfile:
            outfile.write(str(all_metadata))




#######################
# Main                #
########################


def main(inputpath,teiheader,outputdir):
    for file in glob.glob(inputpath):
        html2tei(file,teiheader,outputdir)
    #get_metadata(inputpath)

main('./html/*29.html', "teiHeader.xml", "./tei/")

