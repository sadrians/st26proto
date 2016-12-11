<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <head>
                <title>generated xseql</title>
                <link rel="stylesheet" type="text/css" href="resources/style.css"/>
            </head>
            <body>
                <h1>ST26 SEQUENCE LISTING</h1>
                <h2>GENERAL INFORMATION</h2>

                <table>
                    <tr>
                        <th>File name</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/@fileName"/>
                        </td>
                    </tr>
                    <tr>
                        <th>DTD version</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/@dtdVersion"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Software name</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/@softwareName"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Software version</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/@softwareVersion"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Production date</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/@productionDate"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Applicantion number</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicationIdentification/IPOfficeCode"/>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicationIdentification/ApplicationNumberText"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Filing date</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicationIdentification/FilingDate"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Applicant file reference</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicantFileReference"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Earliest priority number</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/EarliestPriorityApplicationIdentification/IPOfficeCode"/>
                            <xsl:value-of
                                    select="ST26SequenceListing/EarliestPriorityApplicationIdentification/ApplicationNumberText"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Earliest priority date</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/EarliestPriorityApplicationIdentification/FilingDate"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Applicant name</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicantName"/>
                            (
                                <xsl:value-of
                                    select="ST26SequenceListing/ApplicantName/@languageCode"/>
                            )
                        </td>
                    </tr>
                    <tr>
                        <th>Applicant name Latin</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/ApplicantNameLatin"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Inventor name</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/InventorName"/>
                            (
                                <xsl:value-of
                                    select="ST26SequenceListing/InventorName/@languageCode"/>
                            )
                        </td>
                    </tr>
                    <tr>
                        <th>Inventor name Latin</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/InventorNameLatin"/>
                        </td>
                    </tr>
                    <xsl:for-each select="ST26SequenceListing/InventionTitle">
                        <tr>
                            <th>Invention title</th>
                            <td>
                                <xsl:value-of
                                        select="."/>
                                (
                                    <xsl:value-of
                                        select="@languageCode"/>
                                )
                            </td>
                        </tr>
                    </xsl:for-each >
                    

                    <tr>
                        <th>Sequence total quantity</th>
                        <td>
                            <xsl:value-of
                                    select="ST26SequenceListing/SequenceTotalQuantity"/>
                        </td>
                    </tr>
                </table>
                
                <!-- SEQUENCE DATA -->
                <h2>SEQUENCE DATA</h2>
                <xsl:for-each select="ST26SequenceListing/SequenceData">
                    <table>
                        <tr>
                            <th>SEQ ID NO:</th>
                            <td><xsl:value-of select="@sequenceIDNumber"/></td>
                            <th>type</th>
                            <td><xsl:value-of select="INSDSeq/INSDSeq_moltype"/></td>
                            <th>length</th>
                            <td><xsl:value-of select="INSDSeq/INSDSeq_length"/></td>
                        </tr>
                    </table>
                    
                    <!-- FEATURE TABLE -->
                    <h4>FEATURES    Location/Qualifiers</h4> 
                    
                    <xsl:for-each select="INSDSeq/INSDSeq_feature-table/INSDFeature">
                        <div class="indented">
                            <b><xsl:value-of select="INSDFeature_key"/></b> 
                            <xsl:text> </xsl:text>
                            <xsl:value-of select="INSDFeature_location"/>
                        </div>
                        <xsl:for-each select="INSDFeature_quals/INSDQualifier">
                            <div class="qualifier">
                                /<xsl:value-of select="INSDQualifier_name"/>=
                                <xsl:value-of select="INSDQualifier_value"/>
                                <br />
                            </div>
                        </xsl:for-each>
                    </xsl:for-each>
                    <br />
                    <!-- END FEATURE TABLE -->
                    
                    <!-- RESIDUES -->
                    <table id="residuesTable">
                        <tr>
                            <th>residues</th>
                        </tr>
                        <tr>
                            <td>
                                <xsl:value-of
                                        select="INSDSeq/INSDSeq_sequence"/>
                                <!-- <xsl:analyze-string regex=".{{3}}" select="INSDSeq/INSDSeq_sequence">
                                    <xsl:matching-substring><item><xsl:value-of select="."/></item></xsl:matching-substring>
                                    <xsl:non-matching-substring><item><xsl:value-of select="."/></item></xsl:non-matching-substring>
                                </xsl:analyze-string> -->
                            </td>
                        </tr>
                    </table>
                    <!-- END RESIDUES -->
                    <br />
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>


