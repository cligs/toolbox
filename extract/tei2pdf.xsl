<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">
    
    <!-- author: Ulrike Henny -->
    
    <xsl:param name="lang"/>
    
    <xsl:template name="toc">
        <xsl:param name="level">0</xsl:param>
        <xsl:if test="tei:head">
            <fo:block text-align-last="justify" text-indent="{$level * 5}mm">
                <xsl:choose>
                    <xsl:when test="tei:head[following-sibling::tei:head]">
                        <xsl:value-of select="concat(tei:head[1], ': ', tei:head[2])"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="tei:head"/>
                    </xsl:otherwise>
                </xsl:choose>
                <fo:leader leader-pattern="dots"/>
                <fo:basic-link internal-destination="{generate-id((tei:head)[1])}" color="#0066CC">
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
                <fo:simple-page-master master-name="A5" page-height="210mm" page-width="148mm" margin="15mm 15mm 5mm 15mm">
                    <fo:region-body margin="5mm 10mm 15mm 10mm"/>
                    <fo:region-after extent="10mm" region-name="Fußbereich"/>
                </fo:simple-page-master>
            </fo:layout-master-set>
            <fo:page-sequence master-reference="A5">
                <fo:flow flow-name="xsl-region-body" text-align="center">
                    <fo:block font-size="20pt" font-weight="bold" margin="40mm 0 10mm 0">
                        <xsl:value-of select="//tei:titleStmt/tei:title[@type='main']"/>
                    </fo:block>
                    <fo:block font-size="14pt" font-weight="bold" font-style="italic">
                        <xsl:value-of select="//tei:titleStmt/tei:title[@type='sub']"/>
                    </fo:block>
                    <fo:block font-size="16pt" font-weight="bold" margin-top="40mm">
                        <xsl:value-of select="//tei:titleStmt/tei:author/tei:name[@type='full']"/>
                    </fo:block>
                </fo:flow>
            </fo:page-sequence>
            <fo:page-sequence master-reference="A5" format="I">
                <fo:flow flow-name="xsl-region-body">
                    <fo:block font-weight="bold" font-size="16pt" margin-bottom="20mm">
                        <xsl:choose>
                            <xsl:when test="$lang='es'">Índice</xsl:when>
                            <xsl:when test="$lang='fr'">Table des matières</xsl:when>
                            <xsl:when test="$lang='en'">Table of contents</xsl:when>
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
                    <xsl:if test="position()=1">
                        <xsl:attribute name="initial-page-number">1</xsl:attribute>
                    </xsl:if>
                    <fo:static-content flow-name="Fußbereich" text-align="center">
                        <fo:block font-size="10pt">
                            <fo:page-number/>
                        </fo:block>
                    </fo:static-content>
                    <fo:flow flow-name="xsl-region-body" text-align="justify">
                        <fo:block><xsl:apply-templates/></fo:block>
                    </fo:flow>
                </fo:page-sequence>
            </xsl:for-each>
        </fo:root>
    </xsl:template>
    
    <xsl:template match="tei:teiHeader"/>
    
    <xsl:template match="tei:head">
        <xsl:choose>
            <xsl:when test="@type='sub'">
                <fo:block margin="0 0 5mm 0" font-weight="bold" 
                    font-size="14pt" text-align="center" id="{generate-id(.)}">
                    <xsl:apply-templates/>
                </fo:block>
            </xsl:when>
            <xsl:otherwise>
                <fo:block margin="7mm 0 5mm 0" font-weight="bold" 
                    font-size="14pt" text-align="center" id="{generate-id(.)}">
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
    
    <xsl:template match="tei:seg[@rend='italic']">
        <fo:inline font-style="italic">
            <xsl:apply-templates/>
        </fo:inline>
    </xsl:template>
    
    <xsl:template match="tei:l|tei:ab">
        <fo:block>
            <xsl:apply-templates/>
        </fo:block>
    </xsl:template>
    
    <xsl:template match="tei:note">
        [<xsl:apply-templates/>]
    </xsl:template>
    
</xsl:stylesheet>