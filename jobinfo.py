'''jobinfo.py - parse job info from qsub

'''
import subprocess
import xml.etree.ElementTree

#
# State flags from https://github.com/gridengine/gridengine/blob/master/source/libs/sgeobj/sge_job.h
#

STATE_HELD = 0x10
STATE_MIGRATING = 0x20
STATE_QUEUED = 0x40
STATE_RUNNING = 0x80
STATE_SUSPENDED = 0x100
STATE_TRANSFERRING = 0x200
STATE_DELETED = 0x400
STATE_WAITING = 0x800
STATE_EXITING = 0x1000
STATE_WRITTEN = 0x2000
STATE_ERROR = 0x8000

def fetch_jobinfo_by_id(job_id):
    '''Get job info for a specific job by job ID
    
    job_id - Job ID as returned by qsub
    
    returns a JobInfo instance
    '''
    return fetch_jobinfo(["-t", "-j", str(job_id), "-xml"])

def fetch_jobinfo_by_user(user_name):
    '''Get job info for a user's jobs
    
    user_name - name of user for qstat's -u switch
    
    returns a JobInfo instance
    '''
    return fetch_jobinfo(["-t", "-u", user_name, "-xml"])
    
def fetch_jobinfo(qstat_args):
    '''Get job info using qstat
    
    qstat_args - the command-line arguments to qstat
    
    returns a JobInfo instance
    '''
    p = subprocess.Popen(
        ["qstat"] + qstat_args,
        stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise RuntimeError("Failed to submit job: %s" % stderr)
    return QJobInfo(stdout)

class QJobInfo(object):
    '''Represents job info from a qstat command'''
    def __init__(self, xml_text):
        self.xml_text = xml_text
        self.root = xml.etree.ElementTree.fromstring(xml_text)
        
    def get_job_ids(self):
        '''Find all job IDs in the info
        
        returns a sequence of numeric job IDs
        '''
        return map((lambda node:int(node.text)),
                   self.root.findall(".//djob_info/element/JB_job_number"))
    
    def get_job_by_id(self, job_id):
        nodes = self.root.findall(".//djob_info/element[JB_job_number='%d']" %
                                  job_id)
        if len(nodes) == 0:
            return
        return QJob(nodes[0])
    
    def get_job_messages(self, job_id):
        '''Get any job-associated messages
        
        '''
        nodes = self.root.findall(
            ".//messages/element/SME_message_list/element/MES_job_number_list/"+
            ("element[ULNG_value='%d']/" % job_id)+
            "../../MES_message")
        return map((lambda node:node.text), nodes)
    
class QJob(object):
    '''Represents a single job'''
    def __init__(self, node):
        self.node = node
        
    @property
    def job_id(self):
        nodes = self.node.findall("./JB_job_number")
        if len(nodes) == 0:
            return
        return int(nodes[0].text)
    
    @property
    def cwd(self):
        nodes = self.node.findall("./JB_cwd")
        if len(nodes) == 0:
            return
        return nodes[0].text
    
    @property
    def stdout_path(self):
        nodes = self.node.findall("./JB_stdout_path_list/element/PN_path")
        if len(nodes) == 0:
            return
        return nodes[0].text
    
    @property
    def stderr_path(self):
        nodes = self.node.findall("./JB_stderr_path_list/element/PN_path")
        if len(nodes) == 0:
            return
        return nodes[0].text
    
    @property
    def env(self):
        '''The SGE-specific environment variables
        
        returns a dictionary of variable name to value
        '''   
        result = {}
        for node in self.node.findall("./JB_env_list/element[VA_variable][VA_value]"):
            result[node.findall("./VA_variable")[0].text] = \
                node.findall("./VA_value")[0].text
        return result
        
    @property
    def submission_command_line(self):
        nodes = self.node.findall("./JB_submission_comand_line/element/ST_name")
        return map((lambda node:node.text), nodes)
    
    @property
    def task_ids(self):
        nodes = self.node.findall("./JB_ja_tasks/element/JAT_task_number")
        return map((lambda node:int(node.text)), nodes)
    
    def get_task(self, task_id):
        nodes = self.node.findall(
            "./JB_ja_tasks/element[JAT_task_number='%d']" % task_id)
        if len(nodes) == 0:
            return
        return QTask(nodes[0])
    
class QTask(object):
    def __init__(self, node):
        self.node = node
        
    @property
    def task_id(self):
        nodes = self.node.findall("./JAT_task_number")
        if len(nodes) == 0:
            return
        return int(nodes[0].text)
    
    @property
    def state(self):
        '''The state flags for the task'''
        nodes = self.node.findall("./JAT_state")
        if len(nodes) == 0:
            return
        return int(nodes[0].text)
    
    @property
    def st_held(self):
        return (self.state & STATE_HELD) == STATE_HELD
    
    @property
    def st_migrating(self):
        return (self.state & STATE_MIGRATING) == STATE_MIGRATING
    
    @property
    def st_queued(self):
        return (self.state & STATE_QUEUED) == STATE_QUEUED
    
    @property
    def st_running(self):
        return (self.state & STATE_RUNNING) == STATE_RUNNING

    @property
    def st_suspended(self):
        return (self.state & STATE_SUSPENDED) == STATE_SUSPENDED
    
    @property
    def st_transferring(self):
        return (self.state & STATE_TRANSFERRING) == STATE_TRANSFERRING
    
    @property
    def st_deleted(self):
        return (self.state & STATE_DELETED) == STATE_DELETED
    
    @property
    def st_waiting(self):
        return (self.state & STATE_WAITING) == STATE_WAITING
    
    @property
    def st_exiting(self):
        return (self.state & STATE_EXITING) == STATE_EXITING
    
    @property
    def st_written(self):
        return (self.state & STATE_WRITTEN) == STATE_WRITTEN
    
    @property
    def st_error(self):
        return (self.state & STATE_ERROR) == STATE_ERROR

    @property
    def messages(self):
        nodes = self.node.findall(".//JAT_message_list/element/QIM_message")
        return map((lambda node:node.text), nodes)
    
    @property
    def host(self):
        nodes = self.node.findall(".//JAT_granted_resources_list/grl/GRU_host")
        if len(nodes) == 0:
            return
        return nodes[0].text
    
    
        
        
        