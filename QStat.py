#!/usr/bin/env ./batchprofiler.sh
#
# QStat.py - run QStat on the role account to get job status
#
import cgitb
cgitb.enable()
import cgi
import jobinfo
import os
import urlparse
from bpformdata import JOB_ID, BATCHPROFILER_VARIABLES

job_id = BATCHPROFILER_VARIABLES[JOB_ID]
if job_id is None:
    ji = jobinfo.fetch_jobinfo(["-t", "-xml"])
else:
    ji = jobinfo.fetch_jobinfo_by_id(int(job_id))
print "ContentType: text/xml\r"
print "\r"
print ji.xml_text
    