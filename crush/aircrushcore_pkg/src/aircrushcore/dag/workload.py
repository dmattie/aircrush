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

    def get_next_task(self):
        filter="filter[status-filter][condition][path]=field_status&filter[status-filter][condition][operator]=IN&filter[status-filter][condition][value][1]=failed&filter[status-filter][condition][value][2]=notstarted"
        tic = TaskInstanceCollection(cms_host=self.crush_host)
        tic_col = tic.get(filter=filter)
        if(len(tic_col)>0):
            t = tic_col[list(tic_col)[0]]
            return t


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