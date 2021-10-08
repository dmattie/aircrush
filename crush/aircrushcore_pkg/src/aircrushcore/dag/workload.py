from aircrushcore.cms.models.task_instance_collection import TaskInstanceCollection
from aircrushcore.cms.models.task_instance import TaskInstance
from aircrushcore.controller.configuration import AircrushConfig
#from aircrushcore.cms.models.host import Host
from aircrushcore.cms.models import *
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection
from aircrushcore.compute.compute import Compute

class Workload:
    def __init__(self,aircrush:AircrushConfig):            
        self.aircrush=aircrush 
        self.crush_host=Host(
            endpoint=aircrush.config['REST']['endpoint'],
            username=aircrush.config['REST']['username'],
            password=aircrush.config['REST']['password']
            )  

    def get_next_task(self,node_uuid:str):
        compute_node_coll = ComputeNodeCollection(cms_host=self.crush_host)
        compute_node = compute_node_coll.get_one(uuid=node_uuid)
        self._distribute_sessions_to_node(compute_node)
       
        filter="filter[status-filter][condition][path]=field_status&filter[status-filter][condition][operator]=IN&filter[status-filter][condition][value][1]=failed&filter[status-filter][condition][value][2]=notstarted"
        tic = TaskInstanceCollection(cms_host=self.crush_host)
        tic_col = tic.get(filter=filter)
        if(len(tic_col)>0):
            t = tic_col[list(tic_col)[0]]
            return t

    def _distribute_sessions_to_node(self,compute_node:ComputeNode):
        allocated_sessions = compute_node.allocated_sessions()
        
        if compute_node.concurrency_limit<=len(allocated_sessions):            
            print(f"Compute node at capacity ({compute_node.concurrency_limit} sessions). See crush.ini to increase limits.")
            #return
        else:
        
            ses_col = SessionCollection(cms_host=self.crush_host)
                #Get sessions that don't have a compute node allocated
                #outstanding_sessions = ses_col.get(filter="&filter[field_status][value]=notstarted")
                #outstanding_sessions = ses_col.get(filter="&filter[filter1][condition][path]=field_responsible_compute_node.id&filter[filter1][condition][operator]=IS NULL")
            outstanding_sessions = ses_col.get()
            for ses_uid in outstanding_sessions:
                session=ses_col.get_one(ses_uid)
                if session.field_responsible_compute_node is None:
                    subject=session.subject()
                    project=subject.project()
                    print(f"Allocating {project.title}/{subject.title}/{session.title}")
                    compute_node.allocate_session(session_uuid=session.uuid)                
                    allocated_sessions = compute_node.allocated_sessions()
                    if compute_node.concurrency_limit<=len(allocated_sessions):
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

                

                return response
        print("No worker nodes ready to perform this task instance")