<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">

    <!-- author: Ulrike Henny
    XSLT-script for the transformation of CLiGS text encoded in TEI into reading versions in PDF
    to be used together with tei2pdf.py
    -->

    <xsl:param name="lang"/>
    <xsl:variable name="textbox-link">https://github.com/cligs/textbox</xsl:variable>

    <xsl:template name="toc">
        <xsl:param name="level">0</xsl:param>
        <xsl:if test="tei:head">
            <fo:block text-align-last="justify" text-indent="{$level * 5}mm" margin-top="2mm">
                <xsl:choose>
                    <xsl:when test="tei:head[following-sibling::tei:head]">
                        <xsl:value-of select="concat(tei:head[1], ': ', tei:head[2])"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="tei:head"/>
                    </xsl:otherwise>
                </xsl:choose>
                <fo:leader leader-pattern="dots"/>
                <fo:basic-link internal-destination="{generate-id((tei:head)[1])}" color="#383d7d">
                    <fo:page-number-citation ref-id="{generate-id((tei:head)[1])}"/>
                </fo:basic-link>
            </fo:block>
        </xsl:if>
        <xsl:if test="tei:div">
            <xsl:for-each select="tei:div">
                <xsl:call-template name="toc">
                    <xsl:with-param name="level" select="count(ancestor::tei:div)"/>
                </xsl:call-template>
            </xsl:for-each>
        </xsl:if>
    </xsl:template>

    <xsl:template match="/">
        <fo:root>
            <fo:layout-master-set>
                <!-- allgemeine Seitenvorlage -->
                <fo:simple-page-master master-name="A5" page-height="210mm" page-width="148mm"
                    margin="15mm 15mm 5mm 15mm">
                    <fo:region-body margin="5mm 10mm 15mm 10mm"/>
                    <fo:region-after extent="10mm" region-name="Fußbereich"/>
                </fo:simple-page-master>
                <!-- Seitenvorlage für den Titel -->
                <fo:simple-page-master master-name="A5-title" page-height="210mm" page-width="148mm">
                    <fo:region-body margin="15mm 10mm 15mm 10mm" background-color="white"/>
                    <fo:region-before extent="210mm" background-color="#383d7d"/>
                    <fo:region-after extent="15mm" region-name="Fußbereich"/>
                    <!--<fo:region-start extent="10mm" />
                    <fo:region-end extent="10mm" />-->
                </fo:simple-page-master>
                <!-- Seitenvorlage für zweite Seite mit größerem Fußbereich -->
                <fo:simple-page-master master-name="A5-second" page-height="210mm"
                    page-width="148mm" margin="15mm 15mm 5mm 15mm">
                    <fo:region-body margin="5mm 10mm 15mm 10mm"/>
                    <fo:region-after extent="55mm" region-name="Fußbereich"/>
                </fo:simple-page-master>
            </fo:layout-master-set>
            <!-- Titelseite -->
            <fo:page-sequence master-reference="A5-title">
                <fo:static-content flow-name="Fußbereich" text-align="center" font-weight="bold"
                    color="white">
                    <fo:block font-size="10pt" margin-top="3mm">
                        <xsl:choose>
                            <xsl:when test="$lang = 'es'">
                                <xsl:text>Editado por </xsl:text>
                            </xsl:when>
                            <xsl:when test="$lang = 'fr'">
                                <xsl:text>Édité par </xsl:text>
                            </xsl:when>
                            <xsl:when test="$lang = 'en'">
                                <xsl:text>Edited by </xsl:text>
                            </xsl:when>
                        </xsl:choose>
                        <xsl:value-of select="//tei:principal"/>
                    </fo:block>
                    <fo:block font-size="10pt">
                        <xsl:value-of select="normalize-space(//tei:publisher)"/>
                        <xsl:text>, Würzburg </xsl:text>
                        <xsl:value-of select="//tei:publicationStmt/tei:date"/>
                    </fo:block>
                </fo:static-content>
                <fo:flow flow-name="xsl-region-body" text-align="center" font-family="serif">
                    <fo:block font-size="24pt" font-weight="bold" margin="40mm 0 10mm 0">
                        <xsl:value-of select="//tei:titleStmt/tei:title[@type = 'main']"/>
                    </fo:block>
                    <fo:block font-size="14pt" font-weight="bold" font-style="italic">
                        <xsl:value-of select="//tei:titleStmt/tei:title[@type = 'sub']"/>
                    </fo:block>
                    <fo:block font-size="16pt" font-weight="bold" margin-top="35mm">
                        <xsl:value-of select="//tei:titleStmt/tei:author/tei:name[@type = 'full']"/>
                    </fo:block>
                    <fo:block text-align="center" margin-top="15mm">
                        <fo:external-graphic content-width="3cm"
                            src="https://f.hypotheses.org/wp-content/blogs.dir/2707/files/2015/05/CLiGS_Logo_blau_klein-e1431341882941.jpg"
                        />
                    </fo:block>
                </fo:flow>
            </fo:page-sequence>
            <!-- 2. Seite -->
            <fo:page-sequence master-reference="A5-second">
                <fo:static-content flow-name="Fußbereich" text-align="left" font-size="10pt">
                    <fo:table>
                        <fo:table-column column-number="1" column-width="30%"/>
                        <fo:table-column column-number="2" column-width="70%"/>
                        <fo:table-body>
                            <fo:table-row>
                                <fo:table-cell font-weight="bold" text-align="right"
                                    margin-right="5mm">
                                    <fo:block>
                                        <xsl:text>CLiGS ID: </xsl:text>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block>
                                        <xsl:value-of select="//tei:idno[@type = 'cligs']"/>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row>
                                <fo:table-cell font-weight="bold" text-align="right"
                                    margin-right="5mm">
                                    <fo:block>
                                        <xsl:text>CLiGS Textbox: </xsl:text>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block><fo:basic-link external-destination="{$textbox-link}" color="#383d7d"><xsl:value-of select="$textbox-link"/></fo:basic-link></fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row>
                                <fo:table-cell font-weight="bold" text-align="right"
                                    margin-right="5mm">
                                    <fo:block>
                                        <xsl:choose>
                                            <xsl:when test="$lang = 'es'">
                                                <xsl:text>Fuente digital: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'fr'">
                                                <xsl:text>Source digitale: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'en'">
                                                <xsl:text>Digital source: </xsl:text>
                                            </xsl:when>
                                        </xsl:choose>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block>
                                        <xsl:apply-templates
                                            select="//tei:bibl[@type = 'digital-source']"/>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row>
                                <fo:table-cell font-weight="bold" text-align="right"
                                    margin-right="5mm">
                                    <fo:block>
                                        <xsl:choose>
                                            <xsl:when test="$lang = 'es'">
                                                <xsl:text>Fuente impresa: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'fr'">
                                                <xsl:text>Source imprimée: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'en'">
                                                <xsl:text>Print source: </xsl:text>
                                            </xsl:when>
                                        </xsl:choose>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block>
                                        <xsl:apply-templates
                                            select="//tei:bibl[@type = 'print-source']"/>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                            <fo:table-row>
                                <fo:table-cell font-weight="bold" text-align="right"
                                    margin-right="5mm">
                                    <fo:block>
                                        <xsl:choose>
                                            <xsl:when test="$lang = 'es'">
                                                <xsl:text>Licencia: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'fr'">
                                                <xsl:text>Licence: </xsl:text>
                                            </xsl:when>
                                            <xsl:when test="$lang = 'en'">
                                                <xsl:text>Licence: </xsl:text>
                                            </xsl:when>
                                        </xsl:choose>
                                    </fo:block>
                                </fo:table-cell>
                                <fo:table-cell>
                                    <fo:block>
                                        <xsl:apply-templates select="//tei:licence"/>
                                    </fo:block>
                                </fo:table-cell>
                            </fo:table-row>
                        </fo:table-body>
                    </fo:table>
                </fo:static-content>
                <fo:flow flow-name="xsl-region-body">
                    <fo:block/>
                </fo:flow>
            </fo:page-sequence>
            <!-- Inhaltsverzeichnis -->
            <fo:page-sequence master-reference="A5" format="I">
                <fo:flow flow-name="xsl-region-body">
                    <fo:block font-weight="bold" font-size="16pt" margin-bottom="20mm" font-family="serif">
                        <xsl:choose>
                            <xsl:when test="$lang = 'es'">Índice</xsl:when>
                            <xsl:when test="$lang = 'fr'">Table des matières</xsl:when>
                            <xsl:when test="$lang = 'en'">Table of contents</xsl:when>
                        </xsl:choose>
                    </fo:block>
                    <!-- ein Eintrag für jedes div mit head -->
                    <xsl:for-each select="//tei:text/tei:body/tei:div">
                        <xsl:call-template name="toc"/>
                    </xsl:for-each>
                </fo:flow>
            </fo:page-sequence>
            <!-- Page Sequence für jede oberste Div-Ebene; 
                neue Sequence, falls dort noch weitere divs verschachtelt sind -->
            <xsl:for-each select="//tei:text/tei:body/tei:div">
                <fo:page-sequence master-reference="A5">
                    <xsl:if test="position() = 1">
                        <xsl:attribute name="initial-page-number">1</xsl:attribute>
                    </xsl:if>
                    <fo:static-content flow-name="Fußbereich" text-align="center">
                        <fo:block font-size="10pt">
                            <fo:page-number/>
                        </fo:block>
                    </fo:static-content>
                    <fo:flow flow-name="xsl-region-body" text-align="justify">
                        <fo:block>
                            <xsl:apply-templates/>
                        </fo:block>
                    </fo:flow>
                </fo:page-sequence>
            </xsl:for-each>
        </fo:root>
    </xsl:template>

    <xsl:template match="tei:teiHeader"/>

    <xsl:template match="tei:head">
        <xsl:choose>
            <xsl:when test="@type = 'sub'">
                <fo:block margin="0 0 5mm 0" font-weight="bold" font-size="14pt" text-align="center"
                    id="{generate-id(.)}" font-family="serif">
                    <xsl:apply-templates/>
                </fo:block>
            </xsl:when>
            <xsl:otherwise>
                <fo:block margin="7mm 0 5mm 0" font-weight="bold" font-size="14pt"
                    text-align="center" id="{generate-id(.)}" font-family="serif">
                    <xsl:apply-templates/>
                </fo:block>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:p">
        <fo:block text-indent="5mm" margin-bottom="3mm">
            <xsl:apply-templates/>
        </fo:block>
    </xsl:template>

    <xsl:template match="tei:seg[@rend = 'italic']">
        <fo:inline font-style="italic">
            <xsl:apply-templates/>
        </fo:inline>
    </xsl:template>

    <xsl:template match="tei:l | tei:ab">
        <fo:block>
            <xsl:apply-templates/>
        </fo:block>
    </xsl:template>

    <xsl:template match="tei:note"> [<xsl:apply-templates/>] </xsl:template>

    <xsl:template match="tei:ref">
        <fo:basic-link external-destination="{@target}" color="#383d7d">
            <xsl:apply-templates/>
        </fo:basic-link>
    </xsl:template>

</xsl:stylesheet>
