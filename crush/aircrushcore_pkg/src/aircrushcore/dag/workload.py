from aircrushcore.cms.task_instance_collection import TaskInstanceCollection
from aircrushcore.cms.task_instance import TaskInstance
from aircrushcore.controller.configuration import AircrushConfig
#from aircrushcore.cms.host import Host
from aircrushcore.cms import Host,Task,TaskCollection,ComputeNodeCollection,ComputeNode,SessionCollection
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection
from aircrushcore.compute.compute import Compute
import subprocess
import urllib
class Workload:
    def __init__(self,aircrush:AircrushConfig):            
        self.aircrush=aircrush 
        self.crush_host=Host(
            endpoint=aircrush.config['REST']['endpoint'],
            username=aircrush.config['REST']['username'],
            password=aircrush.config['REST']['password']
            )  
        try:
            self.concurrency_limit=int(aircrush.config['COMPUTE']['concurrency_limit'])
        except Exception as e:
            print("Configuration setting concurrency_limit in COMPUTE section not found or not an integer. Defaulting to 2.")
            self.concurrency_limit=2

        try:
            self.seconds_between_failures=int(aircrush.config['COMPUTE']['seconds_between_failures'])
        except Exception as e:
            print("Configuration setting seconds_between_failures in COMPUTE section not found or not an integer. Defaulting to 18000 (5 hours).")
            self.seconds_between_failures=18000

    def get_running_tasks(self,node_uuid:str):
        #Look for tasks initiated by this compute node(node-uuid)
        #Used to determine job status
        tis_on_this_node={}
        compute_node_coll = ComputeNodeCollection(cms_host=self.crush_host)
        compute_node = compute_node_coll.get_one(uuid=node_uuid)

        filter="sort[sort_filter][path]=field_status&sort[sort_filter][direction]=DESC&filter[status-filter][condition][path]=field_status&filter[status-filter][condition][operator]=IN&filter[status-filter][condition][value][1]=running&filter[status-filter][condition][value][2]=limping"
        tic = TaskInstanceCollection(cms_host=self.crush_host)        
        tic_col = tic.get(filter=filter)
        for ti in tic_col:
            if tic_col[ti].associated_session().field_responsible_compute_node==node_uuid:
                tis_on_this_node[ti]=tic_col[ti]
        return tis_on_this_node

    def get_next_task(self,node_uuid:str):
        ###################################################################
        # Big fancy optimization AI brain goes here #######################
        ###################################################################
        #... but for now...
        #What node am I on?
        compute_node_coll = ComputeNodeCollection(cms_host=self.crush_host)
        compute_node = compute_node_coll.get_one(uuid=node_uuid)
        
        #Ensure sessions are allocated and task instances reflect the current pipeline
        self._distribute_sessions_to_node(compute_node)
       
        #Get task instances ready to run
        filter="sort[sort_filter][path]=field_status&sort[sort_filter][direction]=DESC&filter[status-filter][condition][path]=field_status&filter[status-filter][condition][operator]=IN&filter[status-filter][condition][value][1]=failed&filter[status-filter][condition][value][2]=notstarted"
        tic = TaskInstanceCollection(cms_host=self.crush_host)        
        tic_col = tic.get(filter=filter)
        #print("SIFT THROUGH THE PILE")
        if(len(tic_col)>0):
            #Iterate the tasks, looking for one we can do
            for ti_idx in tic_col:
                
                ti = tic_col[ti_idx]                
                session = ti.associated_session()    
                
                if session.field_responsible_compute_node == node_uuid: # This session has been allocated to the node asking for work
                    #print(f"Candidate task instance {ti.title}")
                    task = ti.task_definition()
                    if not self.unmet_dependencies(task,ti): #Ignore any with unmet dependencies
                        
                        if ti.field_jobid and ti.field_status=='failed':
                           #Let's see if this has failed long enough ago that we can go again
                            duration=self.duration_since_job_end(ti.field_jobid)
                            if duration>self.seconds_between_failures:
                                return ti
                            else:
                                print(f"{ti.title} recently failed and will not be re-attempted until {self.seconds_between_failures} seconds have elapsed after failure.  See ~/.crush.ini ")
                        else:
                            return ti
                    #else:
                    #    print(f"\ttask has unmet dependencies {task.title} {ti.associated_session().title}")
    def duration_since_job_end(self,jobid):
        # This command gets the seconds since unix epoch of job end and
        # seconds since unix epoch for now to get seconds between now and job failure
        cmd=f"expr $( date +%s ) - $( date \"+%s\" -d $( sacct -j {jobid}|head -3|tail -1|cut -c 55-74 ) )"
        
        code,out = self.getstatusoutput(cmd)
        if code==0:
            try:
                return int(out)
            except:
                return -1
        return -1
        
    
    def getstatusoutput(self,command):
        #print(command)    
        process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
        out, _ = process.communicate()
        return (process.returncode, out)

    def unmet_dependencies(self,task:Task,candidate_ti:TaskInstance):
        session_uuid=candidate_ti.associated_session()
        for prereq_task in task.field_prerequisite_tasks:
            #for the given task, find dependent tasks with incomplete task instances 

            
            #Look for any uncomplete task_instances matching this task_uuid for this session
            filter="&filter[status-filter][condition][path]=field_status&filter[status-filter][condition][operator]=NOT%20IN&filter[status-filter][condition][value][1]=completed"
            tic = TaskInstanceCollection(cms_host=self.crush_host,task=prereq_task['id'])        
            tic_col = tic.get(filter=filter,session=session_uuid)
            #print(f"\t{len(tic_col)} task instances instantiated for the same session that have failed or not started (including the candidate)")
            if not tic_col == None:
                for ti_uuid in tic_col:
                               
                    if ti_uuid != candidate_ti.uuid:
                        #print(f"\t{tic_col[ti_uuid].title} is a parent of the candidate and is incomplete || compare: found ti {ti_uuid}  candidate_ti.uuid {candidate_ti.uuid}") 
                        #print(f"compare: ti_uuid {ti_uuid}  candidate_ti.uuid {candidate_ti.uuid}")
                        return True
        #print("\tno unmet dependencies for the task definition associated with this task instance")
        return False


    def _distribute_sessions_to_node(self,compute_node:ComputeNode):
        allocated_sessions = compute_node.allocated_sessions()
        
        if int(self.concurrency_limit)<=len(allocated_sessions):            
            print(f"\tCompute node at capacity ({self.concurrency_limit} sessions). See ~/.crush.ini to increase limits.")
            #return
        else:
        
            ses_col = SessionCollection(cms_host=self.crush_host)
                #Get sessions that don't have a compute node allocated
            outstanding_sessions = ses_col.get(page_limit=2,filter="&filter[field_status][value]=notstarted")
            #isnull=urllib.parse.quote_plus("IS NULL")
            #outstanding_sessions = ses_col.get(page_limit=1,filter=f"&filter[filter1][condition][path]=field_responsible_compute_node.id&filter[filter1][condition][operator]={isnull}")
            #outstanding_sessions = ses_col.get(page_limit=1)
            for ses_uid in outstanding_sessions:
                session=ses_col.get_one(ses_uid)
                if session.field_responsible_compute_node is None:
                    subject=session.subject()
                    project=subject.project()

                    if subject == None or project == None:
                        print(f"Session {session.title} is orphaned, please conduct a health check.  Skipping")
                        continue

                    print(f"Allocating {project.title}/{subject.title}/{session.title}")
                    compute_node.allocate_session(session_uuid=session.uuid)                
                    allocated_sessions = compute_node.allocated_sessions()
                    if self.concurrency_limit<=len(allocated_sessions):
                        break

        compute_node.refresh_task_instances()
        

    def count_of_incomplete_tasks(self):
        tic = TaskInstanceCollection(cms_host=self.crush_host)
        tic_col = tic.get()
        return len(tic_col)

    def invoke_task(self,task_instance:TaskInstance):
        task = task_instance.task_definition()
        session = task_instance.associated_session()
        subject = session.subject()
        project = subject.project()               
        
        workers = ComputeNodeCollection(cms_host=self.crush_host).get(filter=f"filter[field_host][value]={project.field_host}")

        print(f"{len(workers)} worker nodes found matching host {project.field_host}")
        for worker_uuid in workers:
            worker=workers[worker_uuid]
            print(worker)
            if worker.isReady:
                print(f"Invoking Task {task.field_operator} on host {worker.field_host}")
                print(f"type======== {type(project.field_host)}")
                conn=ComputeNodeConnection(hostname=project.field_host,username=project.field_username,password=project.field_password)
                node=Compute(conn)
                #response = node.invoke(container="abc",command="whoami")

                

                #return response
        print("No worker nodes ready to perform this task instance")