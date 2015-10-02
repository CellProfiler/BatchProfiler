<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:fn="http://www.w3.org/2005/xpath-functions">
<xsl:variable name="quot">"</xsl:variable>
<xsl:template match="/">
  <xsl:for-each select="detailed_job_info/djob_info/element">
    <div>
      <h2>Job <xsl:value-of select="JB_job_number"/></h2>
      <div>
      <table><tr><th colspan="2">Tasks by state</th></tr>
    <tr><th>Held</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 16) mod 2 = 1])"/></td></tr>
    <tr><th>Migrating</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 32) mod 2 = 1])"/></td></tr>
    <tr><th>Queued</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 64) mod 2 = 1])"/></td></tr>
    <tr><th>Running</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 128) mod 2 = 1])"/></td></tr>
    <tr><th>Suspended</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 256) mod 2 = 1])"/></td></tr>
    <tr><th>Transferring</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 512) mod 2 = 1])"/></td></tr>
    <tr><th>Deleted</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 1024) mod 2 = 1])"/></td></tr>
    <tr><th>Waiting</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 2048) mod 2 = 1])"/></td></tr>
    <tr><th>Exiting</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 4096) mod 2 = 1])"/></td></tr>
    <tr><th>Written</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 8192) mod 2 = 1])"/></td></tr>
    <tr><th>Error</th><td><xsl:value-of select="count(JB_ja_tasks/element[floor(number(JAT_state) div 32768) mod 2 = 1])"/></td></tr>
  </table>
</div>
<div style="margin:10px">
  <table><tr><th colspan="2">Job attributes and values</th></tr>
    <xsl:for-each select="*[starts-with(name(), 'JB_') and substring(name(), string-length(name())-4) != '_list']">
      <tr>
        <th><xsl:value-of select="translate(substring(name(), 4),'_',' ')"/></th>
        <td style="text-align:left">
        <xsl:choose>
          <xsl:when test="substring(name(), string-length(name())-4) = '_time'">
            <span>
              <xsl:attribute name="id">
               <xsl:value-of select="generate-id()"/>
              </xsl:attribute>
            </span>
            <script>
              <xsl:value-of select="concat('document.getElementById(',$quot,generate-id(),$quot,').innerHTML=msec_to_time(',text(),');')"/>
            </script>
          </xsl:when>
          <xsl:when test="name()='JB_submission_command_line'">
            <xsl:for-each select="element/ST_name">
               <xsl:value-of select="concat(text(),' ')"/>
            </xsl:for-each>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="text()"/>
          </xsl:otherwise>
        </xsl:choose>
        </td>
      </tr>
    </xsl:for-each>
  </table>
</div>
<div>
  <h3>Tasks</h3>
  <table style="font-family:monospace;margin-bottom:10px">
    <tr><th colspan="2">State codes</th></tr>
    <tr><th>MIGRATING</th><td>0x0020</td></tr>
    <tr><th>QUEUED</th><td>0x0040</td></tr>
    <tr><th>RUNNING</th><td>0x0080</td></tr>
    <tr><th>SUSPENDED</th><td>0x0100</td></tr>
    <tr><th>TRANSFERRING</th><td>0x0200</td></tr>
    <tr><th>DELETED</th><td>0x0400</td></tr>
    <tr><th>WAITING</th><td>0x0800</td></tr>
    <tr><th>EXITING</th><td>0x1000</td></tr>
    <tr><th>WRITTEN</th><td>0x2000</td></tr>
    <tr><th>ERROR</th><td>0x8000</td></tr>
  </table>
  <table>
    <tr><th>ID</th><th>State</th><th>Host</th><th>Wall (sec)</th><th>CPU (sec)</th><th>Mem</th><th>I/O</th><th>Messages</th></tr>
    <xsl:for-each select="JB_ja_tasks/element">
      <tr>
        <td><xsl:value-of select="JAT_task_number"/></td>
        <td><xsl:value-of select="concat('0x',string(floor(number(JAT_state) div 4096) mod 16), string(floor(number(JAT_state) div 256) mod 16), string(floor(number(JAT_state) div 16) mod 16), string(number(JAT_state) mod 16))"/></td>
        <td><xsl:value-of select="JAT_granted_resources_list/grl/GRU_host"/></td>
        <td><xsl:value-of select="JAT_scaled_usage_list/Events[UA_name='wallclock']/UA_value"/></td>
        <td><xsl:value-of select="JAT_scaled_usage_list/Events[UA_name='cpu']/UA_value"/></td>
        <td><xsl:value-of select="JAT_scaled_usage_list/Events[UA_name='mem']/UA_value"/></td>
        <td><xsl:value-of select="JAT_scaled_usage_list/Events[UA_name='io']/UA_value"/></td>
        <td>
          <xsl:for-each select="JAT_message_list/element/QIM_Message">
            <div><xsl:value-of select="text()"/></div>
          </xsl:for-each>
        </td>
      </tr>
    </xsl:for-each>
  </table>
</div>
</div>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>