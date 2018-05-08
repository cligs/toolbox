#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Submodule which prepares CLiGS-TEI-files for annotation with FreeLing and NLTK WordNet or HeidelTime.
After the annotation (external to this module), the annotated files are brought together in new TEI files.

Check out the documentation for the functions prepare_input and prepare_output for more details.

- for chapterwise annotation (preserving chapter structure) or annotation of the whole text at once (without preserving chapter structure)
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
# wrapper for chapterwise annotation
xslt_TEIwrapper = etree.XML('''\
	<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
		
		<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
		
		<xsl:variable name="cligsID" select="//tei:idno[@type='cligs']"/>
		
		<xsl:template match="/">
			<xsl:processing-instruction name="xml-model">href="https://raw.githubusercontent.com/cligs/reference/master/tei/cligs.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:processing-instruction>
			
            <TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:cligs="https://cligs.hypotheses.org/ns/cligs">
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
	
# wrapper for annotation of the whole text
xslt_TEIwrapper_1 = etree.XML('''\
	<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
		
		<xsl:output method="xml" encoding="UTF-8" indent="yes"/>
		
		<xsl:variable name="cligsID" select="//tei:idno[@type='cligs']"/>
		
		<xsl:template match="/">
			<xsl:processing-instruction name="xml-model">href="https://raw.githubusercontent.com/cligs/reference/master/tei/cligs.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:processing-instruction>
			
            <TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:cligs="https://cligs.hypotheses.org/ns/cligs">
                <xsl:apply-templates select="tei:TEI/tei:teiHeader"/>
                <text>
                    <body>
                        <div>
							<xsl:attribute name="xml:id"><xsl:value-of select="$cligsID"/>_d1</xsl:attribute>
                        </div>
                    </body>
                </text>
            </TEI>
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
		<xsl:param name="mode"/>
		
		<xsl:output method="xml" encoding="UTF-8" indent="yes" />
		
		<xsl:template match="node() | @* | processing-instruction() | comment()">
			<xsl:copy>
				<xsl:apply-templates select="node() | @* | processing-instruction() | comment()"/>
			</xsl:copy>
		</xsl:template>
		
		<xsl:template match="tei:text/tei:body/tei:div">
			<xsl:copy>
				<xsl:copy-of select="@*"/>
				<xsl:choose>
					<xsl:when test="$mode='ht'">
						<xsl:for-each select="document(concat($annofolder, @xml:id,'.xml'))//wrapper">
							<xsl:copy-of select="."/>
						</xsl:for-each>
					</xsl:when>
					<xsl:otherwise>
						<xsl:for-each select="document(concat($annofolder, @xml:id,'.xml'))//s">
							<xsl:element name="ab" xmlns="http://www.tei-c.org/ns/1.0">
								<xsl:element name="{local-name()}" xmlns="http://www.tei-c.org/ns/1.0">
									<xsl:copy-of select="@*"/>
									<xsl:for-each select="w">
										<xsl:element name="{local-name()}" xmlns="http://www.tei-c.org/ns/1.0">
											<xsl:copy-of select="@*"/>
											<xsl:value-of select="."/>
										</xsl:element>
									</xsl:for-each>
								</xsl:element>
							</xsl:element>
						</xsl:for-each>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:copy>
		</xsl:template>
		
	</xsl:stylesheet>
	'''



def prepare_anno(infolder, outfolder, mode="split"):
	"""
	Takes a collection of TEI files and prepares them for annotation.
	
	Arguments:
	infolder (string): path to the input folder (which should contain the input TEI files)
	outfolder (string): path to the output folder (which is created if it does not exist)
	mode (string): default is "split" (chapterwise), also possible is "split-1" (text as a whole)
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
		
		if mode == "split-1":
			transform = etree.XSLT(xslt_TEIwrapper_1)
		else:
			transform = etree.XSLT(xslt_TEIwrapper)

		result_tree = transform(doc)
		result = str(result_tree)
		
		# create TEI wrapper for future annotation results
		with open(os.path.join(outfolder, "temp", outfile_x), "w") as output:
			output.write(result)
			
		# create one full text file per chapter (or for the whole text)
		tei = {'tei':'http://www.tei-c.org/ns/1.0'}
		cligs_id = doc.xpath("//tei:idno[@type='cligs']/text()", namespaces=tei)
		if mode == "split-1":
			results = doc.xpath("//tei:text/tei:body", namespaces=tei)
		else:
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
	
	
	

def postpare_anno(infolder, outfolder, mode="fl"):
	"""
	Creates a TEI file from a collection of annotated full text files (one per chapter or for the whole text).
	Needs an input folder with two subfolders: 'temp' with the TEI file templates and 'anno' with the annotated text in XML format.
	Expects the annotated files to be named according to the following example/pattern: nh0006_d1.xml / [cligs_id]_d[division_id].xml
	
	Arguments:
	infolder (string): path to the input folder (which should contain a folder "temp" with the templates for the new TEI files and a folder "anno" with the annotations in XML format)
	outfolder (string): path to the output folder (which is created if it does not exist)
	mode (string): which kind of annotation to treat; default: "fl" (= FreeLing), alternative: "ht" (= HeidelTime)
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
		# which annotation mode are we in?
		annomode = mode
		
		parser = etree.XMLParser(encoding="UTF-8")
		parser.resolvers.add(FileResolver())
		
		doc = etree.parse(filepath, parser)
		xslt_root = etree.parse(io.StringIO(xslt_joinDIVs), parser)
		
		transform = etree.XSLT(xslt_root)
		
		result_tree = transform(doc, annofolder= "'" + annofolder + "'", mode= "'" + annomode + "'")
		result = str(result_tree)
		
		# save the results
		with open(os.path.join(outfolder, fn), "w") as output:
			output.write(result)
	
	print("Done. " + str(filecounter) + " files treated.")
	
		


def prepare(mode, infolder, outfolder):
	"""
	Preparations for linguistically annotated versions of a collection of TEI files.
	There are two phases:
	- input phase: the full text is extracted chapterwise (or as a whole) from the TEI files, templates for new TEI files meant to hold the annotated text are created
	- output phase: the annotated full text snippets are brought together in the new TEI files
	
	Arguments:
	mode(string): possible values are "split" (chapterwise), "split-1" (the whole text at once) or "merge"
	infolder (string): in split-mode: path to the input folder (which should contain the input TEI files); in merge-mode: path to the annotation output folder (with subfolder "temp" and "anno")
	outfolder (string): in split-mode: path to the output folder for annotation working files; in merge-mode: path to the output folder for annotated TEI result files. The folders are created if they do not exist.
	"""
	if mode == "split":
		prepare_anno(infolder, outfolder, mode="split")
	elif mode == "split-1":
		prepare_anno(infolder, outfolder, mode="split-1")
	elif mode == "merge":
		postpare_anno(infolder, outfolder)
	elif mode == "merge-hdt":
		postpare_anno(infolder, outfolder, mode="ht")
	else:
		raise ValueError("Please indicate one of the following as the value for the first argument: 'split', 'merge'")



if __name__ == "__main__":
	prepare(int(sys.argv[1]))


