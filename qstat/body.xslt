<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:variable name="apos">'</xsl:variable>
<xsl:variable name="quot">"</xsl:variable>
<xsl:key name="Distinct" match="job_info/queue_info/job_list/JB_job_number" use="text()"/>

<xsl:template match="/">
<div style="float:left;background-color: #F0F0F0;width:100px;height:800px;padding: 20px 10px 20px 10px">
<h1>Jobs</h1>
<table>
<xsl:for-each select="job_info/queue_info/job_list[generate-id(JB_job_number) = generate-id(key('Distinct', JB_job_number)[1])]">
    <tr><td>
        <a>
            <xsl:attribute name="href">
                <xsl:value-of
                    select="concat('javascript:xform(',$apos,'content.xslt',$apos,',',$apos,'content',$apos,',',JB_job_number,',null)')"/>
            </xsl:attribute>
            <xsl:value-of select="JB_job_number"/>
            <xsl:value-of select="preceding-sibling::JB_job_number"/>
        </a>
    </td></tr>
</xsl:for-each>
</table>
</div>
<div id="content" style="margin-left:100px;width:800px;padding: 20px 10px 20px 10px"/>
</xsl:template>
</xsl:stylesheet>