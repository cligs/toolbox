Ss<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:functx="http://www.functx.com"
    xmlns:cligs="cligs"
    exclude-result-prefixes="xs functx cligs"
    version="2.0">
    
    <!-- 
        Skript zur Transformation von Théatre classique-Dateien custom TEI-P4 zu TEI-P5
        Autorin: Ulrike Henny, 2016 
    -->
    
    <!-- 
        Verwendung: Variablen hier anpassen, Skript mit beliebigem Eingabe-XML laufen lassen
        - in den Ausgabeordner werden die Zieldateien geschrieben (neue TEI-Dateien und CSV-Dateien)
        - "who" wird als verantwortlich für die TEI-Erstellung eingetragen
    -->
    <xsl:variable name="Pfad_Eingabeordner">tei4</xsl:variable>
    <xsl:variable name="Pfad_Ausgabeordner">tei5</xsl:variable>
    <xsl:variable name="who">cf</xsl:variable>
    
    
    <!-- ################ Outputs ################## -->
    
    <xsl:output name="xml" method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:output name="csv" method="text" encoding="UTF-8"/>
    
    
    <!-- ################ Funktionen & allg. Templates ################ -->
    
    <xsl:function name="functx:capitalize-first" as="xs:string?">
        <xsl:param name="arg" as="xs:string?"/>
        <xsl:sequence select="concat(upper-case(substring($arg,1,1)),substring($arg,2))"/>
    </xsl:function>
    
    <xsl:function name="cligs:remove-special-characters" as="xs:string">
        <xsl:param name="arg" as="xs:string?"/>
        <xsl:variable name="str" select="translate($arg,'ÁÀÂÉÈÊÎÔÛÄÖÜ, ','AAAEEEIOUAOU')"/>
        <xsl:sequence select='replace($str,"&#x0027;","")'/>
    </xsl:function>
    
    <xsl:function name="cligs:get-idno" as="xs:string">
        <xsl:param name="context" as="node()"/>
        <xsl:value-of select="substring-before(tokenize(base-uri(root($context)),'/')[last()], '.xml')"/>
    </xsl:function>
    
    
    <!-- ################ Header-Template ################## -->
    <xsl:template name="header">
        <teiHeader xmlns="http://www.tei-c.org/ns/1.0">
            <fileDesc>
                <titleStmt>
                    <xsl:variable name="title-main" select="functx:capitalize-first(lower-case(//titleStmt/title/substring-before(.,',')))"/>
                    <xsl:variable name="title" select="//titleStmt/title"/>
                    <xsl:variable name="title" select="replace($title,'(^.*?)\.$','$1')"/>
                    <xsl:variable name="title-split" select="tokenize($title,'[,.]+\s?')"/>
                    <xsl:variable name="title-main" select="$title-split[1]"/>
                    <xsl:variable name="title-main" select="functx:capitalize-first(lower-case($title-main))"/>
                    <xsl:variable name="title-sub" select="$title-split[last()]"/>
                    <xsl:variable name="title-sub" select="functx:capitalize-first(lower-case($title-sub))"/>
                    <title type="main"><xsl:value-of select="$title-main"/></title>
                    <title type="sub"><xsl:value-of select="$title-sub"/></title>
                    <title type="short"><xsl:value-of select="$title-main"/></title>
                    <title type="idno">
                        <idno type="viaf"></idno>
                    </title>
                    <xsl:for-each select="tokenize(//titleStmt/author,'(;\s?|\set\s)')">
                        <author>
                            <name type="full"><xsl:value-of select="."/></name>
                            <name type="short">
                                <xsl:choose>
                                    <xsl:when test="contains(.,',')">
                                        <xsl:value-of select="functx:capitalize-first(lower-case(substring-before(.,',')))"/>
                                    </xsl:when>
                                    <xsl:otherwise><xsl:value-of select="functx:capitalize-first(lower-case(.))"/></xsl:otherwise>
                                </xsl:choose>
                            </name>
                            <idno type="viaf"></idno>
                        </author>
                    </xsl:for-each>
                    <principal><xsl:value-of select="normalize-space(//publicationStmt/editor)"/></principal>
                </titleStmt>
                <publicationStmt>
                    <publisher>CLiGS</publisher>
                    <idno type="cligs"><xsl:value-of select="cligs:get-idno(.)"/></idno>
                    <date>2016</date>
                </publicationStmt>
                <sourceDesc>
                    <bibl type="digital-source">
                        <date>
                            <xsl:choose>
                                <xsl:when test="//publicationStmt/publisher[matches(.,'\d{4}')]">
                                    <xsl:value-of select="replace(//publicationStmt/publisher,'^.*(\d{4}).*$','$1')"/>
                                </xsl:when>
                                <xsl:when test="//publicationStmt/p[2][matches(.,'\d{4}')]">
                                    <xsl:value-of select="replace(//publicationStmt/p[2],'^.*(\d{4}).*$','$1')"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="replace(//publicationStmt/p[1],'^.*(\d{4}).*$','$1')"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </date>
                        <xsl:text>, </xsl:text>
                        <idno><xsl:value-of select="//idno[@type='tc']"/></idno>
                        <xsl:text>, </xsl:text>
                        <ref target="http://theatre-classique-fr/"/>
                        <xsl:text>. Publié par Paul Fièvre.</xsl:text></bibl>
                    <bibl type="print-source">
                        <date><xsl:value-of select="//docDate/@value"/></date>, <idno></idno>, <ref target="#"/>. <xsl:value-of select="//docImprint/printer"/>.</bibl>
                    <bibl type="edition-first">
                        <date></date>, <idno></idno>, <ref target="#"/>.</bibl>
                    <bibl type="performance-first">
                        <date><xsl:value-of select="//performance/premiere/@date/replace(.,'^.*(\d{4}).*$','$1')"/></date>, <idno></idno>, <ref target="#"/>. <xsl:value-of select="//performance/premiere"/></bibl>
                </sourceDesc>
            </fileDesc>
            <profileDesc>
                <abstract>
                    <p></p>
                </abstract>
                <textClass>
                    <keywords scheme="keywords.csv">
                        <term type="supergenre">drama</term>
                        <term type="genre"><xsl:value-of select="//SourceDesc/genre"/></term>
                        <term type="structure"><xsl:value-of select="//SourceDesc//structure/lower-case(.)"/></term>
                        <term type="form"><xsl:value-of select="//SourceDesc/type"/></term>
                        <term type="period"><xsl:value-of select="//SourceDesc/periode"/></term>
                        <term type="taille"><xsl:value-of select="//SourceDesc/taille"/></term>
                    </keywords>
                </textClass>
            </profileDesc>
            <revisionDesc>
                <xsl:variable name="currdate" select="replace(xs:string(current-date()),'^.*(\d{4}-\d{2}-\d{2}).*$','$1')"/>
                <change when="{$currdate}" who="{$who}">Initial TEI version.</change>
            </revisionDesc>
        </teiHeader>
    </xsl:template>
    
    
    <!-- ########## Body-Templates ########## -->
    
    <xsl:template match="div1|div2">
        <div xmlns="http://www.tei-c.org/ns/1.0" type="{@type}" n="{@n}">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <xsl:template match="head">
        <head xmlns="http://www.tei-c.org/ns/1.0">
           <xsl:apply-templates/>
        </head>
    </xsl:template>
    
    <xsl:template match="sp">
        <sp xmlns="http://www.tei-c.org/ns/1.0" who="{cligs:get-idno(.)}-{cligs:remove-special-characters(@who)}">
            <xsl:apply-templates/>
        </sp>
    </xsl:template>
    
    <xsl:template match="speaker">
        <speaker xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </speaker>
    </xsl:template>
    
    <xsl:template match="l">
        <l xmlns="http://www.tei-c.org/ns/1.0" n="{@id}">
            <xsl:if test="@part">
                <xsl:attribute name="part" select="upper-case(@part)"/>
            </xsl:if>
            <xsl:apply-templates/>
        </l>
    </xsl:template>
    
    <xsl:template match="stage">
        <stage xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates/>
        </stage>
    </xsl:template>
    
    <xsl:template match="note">
        <note xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:if test="@type">
                <xsl:attribute name="type" select="@type"/>
            </xsl:if>
            <xsl:apply-templates/>
        </note>
    </xsl:template>
    
    <xsl:template match="p">
        <xsl:choose>
            <xsl:when test="@type='v'">
                <l xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:apply-templates/>
                </l>
            </xsl:when>
            <xsl:otherwise>
                <p xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:if test="@id">
                        <xsl:attribute name="n" select="@id"/>
                    </xsl:if>
                    <xsl:apply-templates/>
                </p>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="s">
        <s xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:if test="@id">
                <xsl:attribute name="n" select="@id"/>
            </xsl:if>
            <xsl:apply-templates/>
        </s>
    </xsl:template>
    
    <xsl:template match="sp/text()[matches(.,'\S')]">
        <ab xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:value-of select="."/>
        </ab>
    </xsl:template>
    
    <xsl:template match="preface">
        <div xmlns="http://www.tei-c.org/ns/1.0" type="preface">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    
    <!-- ################ Template zur Transformation der Dokumente ############### -->
    <xsl:template name="transform">
        <xsl:for-each select="collection($Pfad_Eingabeordner)//TEI">
            <xsl:variable name="dateiname" select="tokenize(base-uri(.),'/')[last()]"/>
            <xsl:message>
                <xsl:value-of select="$dateiname"/>
            </xsl:message>
            <xsl:result-document href="{$Pfad_Ausgabeordner}/{$dateiname}" format="xml">
                <xsl:processing-instruction name="xml-model">href="https://raw.githubusercontent.com/cligs/reference/master/tei/standard/cligs.rnc" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:processing-instruction>
                <TEI xmlns="http://www.tei-c.org/ns/1.0">
                    <xsl:call-template name="header"/>
                    <text>
                        <front>
                            <castList>
                                <head><xsl:value-of select="//castList/head"/></head>
                                <xsl:for-each select="//castList/castItem">
                                    <castItem>
                                        <role xml:id="{cligs:get-idno(.)}-{cligs:remove-special-characters(role)}"><xsl:value-of select="role"/></role>
                                    </castItem>
                                </xsl:for-each>
                            </castList>
                            <set>
                                <p><xsl:value-of select="//front/set"/></p>
                            </set>
                            <xsl:apply-templates select="//font/preface"/>
                        </front>
                        <body>
                            <xsl:apply-templates select="//text/body"/>
                        </body>
                    </text>
                </TEI>
            </xsl:result-document>
        </xsl:for-each>
    </xsl:template>
    
    
    <!-- ################ Template für CSV-Datei-Erstellung ############### -->
    
    <xsl:template name="csv">
        <xsl:result-document href="{$Pfad_Ausgabeordner}/authors.csv" format="csv">
            <xsl:text>cligs_id,surname,forname,born,born_location,death,death_location,academie,author_string</xsl:text>
            <xsl:for-each select="collection($Pfad_Eingabeordner)//titleStmt/author">
                <xsl:variable name="cligs-id" select="cligs:get-idno(.)"/>
                <xsl:variable name="born" select="@born"/>
                <xsl:variable name="born_location" select="@born_location"/>
                <xsl:variable name="death" select="@death"/>
                <xsl:variable name="death_location" select="@death_location"/>
                <xsl:variable name="academie" select="@academie"/>
                <xsl:variable name="author_string" select="."/>
                <xsl:for-each select="tokenize(.,'(;\s?|\set\s)')"><xsl:text>
</xsl:text>     <xsl:value-of select="$cligs-id"/>
                    <xsl:text>,</xsl:text>
                    <xsl:choose>
                        <xsl:when test="contains(.,',')">
                            <xsl:value-of select="functx:capitalize-first(lower-case(substring-before(.,',')))"/>
                        </xsl:when>
                        <xsl:otherwise><xsl:value-of select="functx:capitalize-first(lower-case(.))"/></xsl:otherwise>
                    </xsl:choose>
                    <xsl:text>,</xsl:text>
                    <xsl:choose>
                        <xsl:when test="contains(.,',')">
                            <xsl:value-of select="normalize-space(substring-after(.,','))"/>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$born"/>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$born_location"/>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$death"/>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$death_location"/>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$academie"/>
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="$author_string"/>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:result-document>
        <xsl:result-document href="{$Pfad_Ausgabeordner}/roles.csv" format="csv">
            <xsl:text>role_id,civil,type,statut,age,stat_amour</xsl:text>
            <xsl:for-each select="collection($Pfad_Eingabeordner)//castList//role"><xsl:text>
</xsl:text>     <xsl:value-of select="concat(cligs:get-idno(.),'-',cligs:remove-special-characters(@id))"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@civil"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@type"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@statut"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@age"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@stat_amour"/>
            </xsl:for-each>
        </xsl:result-document>
        <xsl:result-document href="{$Pfad_Ausgabeordner}/sets.csv" format="csv">
            <xsl:text>cligs_id,location,country,periode,link</xsl:text>
            <xsl:for-each select="collection($Pfad_Eingabeordner)//front/set"><xsl:text>
</xsl:text>     <xsl:value-of select="cligs:get-idno(.)"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@location"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@country"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@periode"/>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@link"/>
            </xsl:for-each>
        </xsl:result-document>
    </xsl:template>
    
    
    <!-- ################ Main ###################### -->
    <xsl:template match="/">
        <xsl:call-template name="transform"/>
        <xsl:call-template name="csv"/>
    </xsl:template>
    
    
</xsl:stylesheet>
