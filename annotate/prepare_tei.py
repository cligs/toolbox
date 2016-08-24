#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Submodule which prepares CLiGS-TEI-files for annotation with e.g. FreeLing and NLTK WordNet.
After the annotation (external to this module), the annotated files are brought together in new TEI files.

Check out the documentation for the functions prepare_input and prepare_output for more details.

- for chapterwise annotation
- just the body text is preserved
- headings, notes and inline markup are discarded

@author: Ulrike Henny
@filename: prepare_tei.py

"""

import os
import glob
import sys
import io
from lxml import etree
from pathlib import Path


class FileResolver(etree.Resolver):
	def resolve(self, url, pubid, context):
		return self.resolve_filename(url, context)


# XSLT snippets
xslt_TEIwrapper = etree.XML('''\
	<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
		
		<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
		
		<xsl:variable name="cligsID" select="//tei:idno[@type='cligs']"/>
		
		<xsl:template match="/">
			<xsl:processing-instruction name="xml-model">href="https://raw.githubusercontent.com/cligs/reference/61639b75deae2916eabeb036313dc8089da40e5e/tei/annotated/cligs_annotated.rnc" type="application/relax-ng-compact-syntax"</xsl:processing-instruction>
			
            <TEI xmlns="http://www.tei-c.org/ns/1.0">
                <xsl:apply-templates select="tei:TEI/tei:teiHeader"/>
                <text>
                    <body>
                        <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
                    </body>
                </text>
            </TEI>
		</xsl:template>
		
		<xsl:template match="tei:div[ancestor::tei:body][not(descendant::tei:div[not(ancestor::tei:floatingText)])][not(ancestor::tei:floatingText)]">
			<xsl:copy>
				<xsl:attribute name="xml:id"><xsl:value-of select="$cligsID"/>_d<xsl:value-of select="count(preceding::tei:div[ancestor::tei:body][not(descendant::tei:div[not(ancestor::tei:floatingText)])][not(ancestor::tei:floatingText)]) + 1"/></xsl:attribute>
			</xsl:copy>
		</xsl:template>
		
		<xsl:template match="tei:teiHeader | tei:teiHeader//node() | tei:teiHeader//@* | tei:teiHeader//processing-instruction() | tei:teiHeader//comment()">
			<xsl:copy>
				<xsl:apply-templates select="node() | @* | processing-instruction() | comment()"/>
			</xsl:copy>
		</xsl:template>
		
		<xsl:template match="text()[not(ancestor::tei:teiHeader)]"/>
		
	</xsl:stylesheet>
	''')
	
xslt_extractDIVs = etree.XML('''\
	<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
		
		<xsl:output method="text" encoding="UTF-8" indent="yes"/>
		
		<xsl:template match="tei:head|tei:note">
			<xsl:text> </xsl:text>
		</xsl:template>
		
		<xsl:template match="tei:*[not(name() = 'head') and not(name() = 'note')]">
			<xsl:text> </xsl:text><xsl:apply-templates /><xsl:text> </xsl:text>
		</xsl:template>
		
		<xsl:template match="text()">
			<xsl:value-of select="normalize-space(.)"/>
		</xsl:template>
		
	</xsl:stylesheet>
	''')

xslt_joinDIVs = '''\
	<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
    
		<xsl:param name="annofolder"/>
		
		<xsl:output method="xml" encoding="UTF-8" indent="yes" />
		
		<xsl:template match="node() | @* | processing-instruction() | comment()">
			<xsl:copy>
				<xsl:apply-templates select="node() | @* | processing-instruction() | comment()"/>
			</xsl:copy>
		</xsl:template>
		
		<xsl:template match="tei:text/tei:body/tei:div">
			<xsl:copy>
				<xsl:copy-of select="@*"/>
				<xsl:copy-of select="document(concat($annofolder, @xml:id,'.xml'))//body"/>
			</xsl:copy>
		</xsl:template>
		
	</xsl:stylesheet>
	'''



def prepare_anno(infolder, outfolder):
	"""
	Takes a collection of TEI files and prepares them for annotation (chapterwise).
	
	Arguments:
	infolder (string): path to the input folder (which should contain the input TEI files)
	outfolder (string): path to the output folder (which is created if it does not exist)
	"""
	print("Starting...")
	
	inpath = os.path.join(infolder, "*.xml")
	filecounter = 0
	
	# check output folders
	if not os.path.exists(outfolder):
		os.makedirs(outfolder)
		
	out_tei = os.path.join(outfolder, "temp")
	out_txt = os.path.join(outfolder, "txt")
	
	if not os.path.exists(out_tei):
		os.makedirs(out_tei)
	if not os.path.exists(out_txt):
		os.makedirs(out_txt)
		
	
	for filepath in glob.glob(inpath):
		filecounter+= 1
		fn = os.path.basename(filepath)[:-4]
		outfile_x = fn + ".xml"
		
		doc = etree.parse(filepath)
		
		transform = etree.XSLT(xslt_TEIwrapper)
		result_tree = transform(doc)
		result = str(result_tree)
		
		# create TEI wrapper for future annotation results
		with open(os.path.join(outfolder, "temp", outfile_x), "w") as output:
			output.write(result)
			
		# create one full text file per chapter
		tei = {'tei':'http://www.tei-c.org/ns/1.0'}
		cligs_id = doc.xpath("//tei:idno[@type='cligs']/text()", namespaces=tei)
		results = doc.xpath("//tei:div[ancestor::tei:body][not(descendant::tei:div[not(ancestor::tei:floatingText)])][not(ancestor::tei:floatingText)]", namespaces=tei)
		
		if isinstance(cligs_id, list):
			cligs_id = cligs_id[0]
		elif isinstance(cligs_id, str) == False:
			raise ValueError("This type (" + str(type(cligs_id)) + ") is not supported for cligs_id. Must be list or string.")
		
		for i,r in enumerate(results):
			transform = etree.XSLT(xslt_extractDIVs)
			result_tree = transform(r)
			result = str(result_tree)
			
			outfile = cligs_id + "_d" + str(i + 1) + ".txt"
			
			with open(os.path.join(outfolder, "txt", outfile), "w") as output:
				output.write(result)
	
	print("Done. " + str(filecounter) + " files treated.")
	
	
	

def postpare_anno(infolder, outfolder):
	"""
	Creates a TEI file from a collection of annotated full text files (one per chapter).
	Needs an input folder with two subfolders: 'temp' with the TEI file templates and 'anno' with the annotated text in XML format.
	Expects the annotated files to be named according to the following example/pattern: nh0006_d1.xml / [cligs_id]_d[division_id].xml
	
	Arguments:
	infolder (string): path to the input folder (which should contain a folder "temp" with the templates for the new TEI files and a folder "anno" with the annotations in XML format)
	outfolder (string): path to the output folder (which is created if it does not exist)
	"""
	print("Starting...")
	
	if not os.path.exists(infolder):
		raise ValueError("The input folder could not be found.")
		
	in_temp = os.path.join(infolder, "temp")
	in_anno = os.path.join(infolder, "anno")
	
	if not os.path.exists(in_temp):
		raise ValueError("The folder 'temp' could not be found inside the input folder.")
	if not os.path.exists(in_anno):
		raise ValueError("The folder 'anno' could not be found inside the input folder.")
	if not os.path.exists(outfolder):
		os.makedirs(outfolder)
		
	filecounter = 0	

	# fetch annotated snippets for each TEI template file
	for filepath in glob.glob(os.path.join(in_temp, "*.xml")):
		print("doing file " + filepath)
		filecounter+= 1
		fn = os.path.basename(filepath)
		annofolder = os.path.join(Path(os.path.join(infolder, "anno")).as_uri(), "")
		
		parser = etree.XMLParser(encoding="UTF-8")
		parser.resolvers.add(FileResolver())
		
		doc = etree.parse(filepath, parser)
		xslt_root = etree.parse(io.StringIO(xslt_joinDIVs), parser)
		
		transform = etree.XSLT(xslt_root)
		
		result_tree = transform(doc, annofolder= "'" + annofolder + "'")
		result = str(result_tree)
		
		# save the results
		with open(os.path.join(outfolder, fn), "w") as output:
			output.write(result)
	
	print("Done. " + str(filecounter) + " files treated.")
	
		


def prepare(mode, infolder, outfolder):
	"""
	Preparations for linguistically annotated versions of a collection of TEI files.
	There are two phases:
	- input phase: the full text is extracted chapterwise from the TEI files, templates for new TEI files meant to hold the annotated text are created
	- output phase: the annotated full text snippets are brought together in the new TEI files
	
	Arguments:
	mode(string): possible values are "split" or "merge"
	infolder (string): in split-mode: path to the input folder (which should contain the input TEI files); in merge-mode: path to the annotation output folder (with subfolder "temp" and "anno")
	outfolder (string): in split-mode: path to the output folder for annotation working files; in merge-mode: path to the output folder for annotated TEI result files. The folders are created if they do not exist.
	"""
	if mode == "split":
		prepare_anno(infolder, outfolder)
	elif mode == "merge":
		postpare_anno(infolder, outfolder)
	else:
		raise ValueError("Please indicate one of the following as the value for the first argument: 'split', 'merge'")



if __name__ == "__main__":
	prepare(int(sys.argv[1]))


