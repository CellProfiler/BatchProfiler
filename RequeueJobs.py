#!/usr/bin/env ./batchprofiler.sh
#
# Requeue jobs
#
"""
CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Copyright (c) 2003-2009 Massachusetts Institute of Technology
Copyright (c) 2009-2015 Broad Institute
All rights reserved.

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
"""
print "Content-Type: text/html\r"
print "\r"
import cgitb
cgitb.enable()
import RunBatch
import bputilities
from bpformdata import *
import cgi
import os
import subprocess
import sys

batch_id = BATCHPROFILER_VARIABLES[BATCH_ID]
if job_id is not None:
    bputilities.requeue_job(job_id)
    print "Content-Type: text/html"
    print"""
    <html><head><title>Job %(job_id)d requeued</title></head>
    <body>Job %(job_id)d requeued
    </body>
    </html>
"""%(globals())
else:
    print """<html><head><title>Requeue jobs</title></head>
    <body>
    <h1>Requeue jobs started by the imageweb webserver</h1>
    <form action='RequeueJobs.py' method='POST'>
    Job ID:<input type='text' name='job_id' />
    <input type='submit' value='Kill'/>
    </form>
    """
    script = """#!/bin/sh
set -v
if [ -e "$HOME/.batchprofiler.sh" ]; then
. "$HOME/.batchprofiler.sh"
fi
set +v
qstat
"""
    scriptfile = bputilities.make_temp_script(script)
    try:
        output = subprocess.check_output([scriptfile])
    finally:
        os.remove(scriptfile)
    result = []
    lines = output.split("\n")
    header = lines[0]
    columns = [i for i in range(len(header))
               if i == 0 or (header[i-1].isspace() and not header[i].isspace())]
    columns.append(len(header))
    rows = [[line[columns[i]:columns[i+1]].strip() 
             for i in range(len(columns)-1)]
            for line in lines]
    header = rows[0]
    body = rows[2:]
    print """
    <h2>Jobs on imageweb</h2>
    <table>
    """
    print "<tr>%s</tr>"%("".join([
        '<th>%s</th>'%field for field in header]))
    for fields in body:
        try:
            job_id = int(fields[0])
        except:
            continue
        fields[0] = """
        <form action='RequeueJobs.py' method='POST'>
        Job ID: %d 
        <input type='hidden' name='job_id' value='%d'/>
        <input type='submit' value='Requeue'/>
        </form>""" % (job_id, job_id)
        
        print "<tr><td>%s</td></tr>" % "</td><td>".join(fields)
    """
    </table>
    </body>
    """
sys.stdout.close()
bputilities.shutdown_cellprofiler()