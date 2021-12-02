import json
from .session import Session
from .session_collection import SessionCollection
from .task_instance import TaskInstance
from .task_collection import TaskCollection
from .task_instance_collection import TaskInstanceCollection
#from .compute_node_collection import ComputeNodeCollection
from .pipeline_collection import PipelineCollection

class ComputeNode():
   
    def __init__(self,**kwargs):
        self.title=""                        
        self.field_host=""                
        self.field_username=""
        self.__field_password=""
        self.field_working_directory=""   
        self.field_account="" 
        self.body=""
        self.uuid=""  
        self.HOST=None    
        self.concurrency_limit=2 #TODO

        #TODO  Need log and error locations, job start directory       
      
        if 'metadata' in kwargs:
            m=kwargs['metadata']

        if 'title' in m:
            self.title=m['title']
        if 'field_host' in m:
            self.field_host=m['field_host']      
        if 'field_username' in m:            
            self.field_username=m['field_username']                     
        if 'field_password' in m:
            self.__field_password=m['field_password']
        if 'field_working_directory' in m:            
            self.field_working_directory=m['field_working_directory']
        if 'field_account' in m:
            self.field_account=m['field_account']
        if 'body' in m:
            self.body=m['body']     
        if "uuid" in m:
            self.uuid=m['uuid']          
        if "cms_host" in m:
            self.HOST=m['cms_host'] 
   
    def upsert(self):

            payload = {
                "data" : {
                    "type":"node--compute_node",                      
                    "attributes":{
                        "title": self.title,                                                                            
                        "field_host":self.field_host,
                        "field_username":self.field_username,
                        "field_password":self.__field_password,
                        "field_working_directory":self.field_working_directory,    
                        "field_account":self.field_account,                                            
                        "body":self.body                        
                    }                    
                }
            }
            #print(json.dumps(payload))
            if self.uuid:   #Update existing                     
                payload['data']['id']=self.uuid                                             
                r= self.HOST.patch(f"jsonapi/node/compute_node/{self.uuid}",payload)
            else:                
                r= self.HOST.post("jsonapi/node/compute_node",payload)

            if(r.status_code!=200 and r.status_code!=201):                   
                print(f"[ERROR] failed to upsert ComputeNode {self.uuid} ({self.title}) on CMS HOST: {r.status_code},  {r.reason}\n\n{payload}")
            else:   
                self.uuid =r.json()['data']['id']      
                return r.json()['data']['id']          
              
    def delete(self):
        if self.uuid:          
            r= self.HOST.delete(f"jsonapi/node/compute_node/{self.uuid}")
        else: 
            return False
        
        if(r.status_code!=204):                   
            raise ValueError(f"ComputeNode deletion failed [{self.uuid}]")

        return True

    def isReady(self):
        return True
        #TODO, check connectivity, disk quota, etc

    def allocated_sessions(self):
        
        sess_col = SessionCollection(cms_host=self.HOST)   
        sess_uids = sess_col.get(filter=f"&filter[field_responsible_compute_node.id][value]={self.uuid}")
        
        return sess_uids
        #sess_uids = sess_col.get()
    def allocate_session(self,session_uuid:str):
        if self.uuid is None:
            raise Exception("ComputeNode is new.  Save before allocation of sessions")
        #Get Session
        sess_col = SessionCollection(cms_host=self.HOST)            
        sess = sess_col.get_one(uuid=session_uuid)

        # if sess.sticky==False: #not currently being allocated elsewhere
        #     sess.sticky=True  #Let's lock it up so it doesn't get allocated elsewhere
        #     sess.upsert()
        # else:
        #     subject=sess.subject()

        #     print("---------------------------------------------------------------------------")
        #     print(f"Attempted to allocate {subject.title}/{sess.title}, but session currently undergoing lock operation another compute node.  Check session sticky flag if problem continues")
        #     print("---------------------------------------------------------------------------")
        #     raise Exception("Session currently locked by another compute node")

        self._attach_to_session(session=sess)
        self._establish_task_instances(session=sess)

        sess.sticky=False
        sess.upsert()
    def refresh_task_instances(self):
        print("Refreshing task instances")
        sess_col = SessionCollection(cms_host=self.HOST)            
        sessions = sess_col.get(filter=f"&filter[field_responsible_compute_node.id][value]={self.uuid}")
        for ses in sessions:
            #print(f"\t{sessions[ses].title}")
            self._establish_task_instances(sessions[ses])

    def _attach_to_session(self,session:Session):
    #    pass
        if session.field_responsible_compute_node is None:
            session.field_responsible_compute_node=self.uuid
            session.upsert
        # else:
        #     cn_coll = ComputeNodeCollection(cms_host=self.HOST)
        #     cn=cn_coll.get_one(session.field_responsible_compute_node)
        #     if cn is None:
        #         subject=session.subject()
        #         raise Exception("Session {subject.title}/{session.title} is allocated to a compute node that no longer exists.  Task instances may be orphaned")
        #     else:                
        #         raise Exception("Session is already allocated to a compute node")
        
    def _establish_task_instances(self,session:Session):
        

        #Look at existing task instances
        ti_col = TaskInstanceCollection(cms_host=self.HOST,session=session.uuid)
        pipe_col = PipelineCollection(cms_host=self.HOST)
        tis = ti_col.get()

        ses_assigned_to_ti=None
        for ti in tis:
            #TIs exist for this session, let's see if they are with us or elsewhere
            #Get first task instance to determine allocated compute node               
            #ti = ti_col.get_one(uuid=ti_uuids[0])            
            ses_assigned_to_ti=tis[ti].field_associated_participant_ses
            break                 

        #If there are task instances assigned to this session or there are no task instances...
        #print(f"\tsession_assigned_to_ti:{ses_assigned_to_ti}, session:{session.uuid}")
        if ses_assigned_to_ti is None or ses_assigned_to_ti==session.uuid:
            project = session.project()
            if project == None:
                print(f"WARNING: Session {session.title} has been assigned to this compute node, but is orphaned or project is unpublished")
                return
           
            activated_pipelines = session.project().field_activated_pipelines
            
        #    print(f"\t\tActivated pipelines for this session: {activated_pipelines}")
            

            for pipeline_uuid in activated_pipelines:
                
                pipe = pipe_col.get_one(uuid=pipeline_uuid)
        #        print(f"\t\tPipeline: {pipe.title} ({pipeline_uuid})")
                task_col = TaskCollection(cms_host=self.HOST,pipeline=pipeline_uuid)
                for task_uuid in task_col.get():
        #            print(f"\t\t\ttask uuid:{task_uuid}")
                                      
                    #Look for a task instance for this pipeline.task associated with this session
                   ##This caused a TIMEOUT ti_col = TaskInstanceCollection(cms_host=self.HOST,pipeline=pipeline_uuid,task=task_uuid,session=session.uuid)
                    ti_col = TaskInstanceCollection(cms_host=self.HOST,session=session.uuid)
                    matching_tis = ti_col.get()
                    ti_exists=False
                    for match in matching_tis:
                        if matching_tis[match].field_pipeline==pipeline_uuid and matching_tis[match].field_task==task_uuid:
                            ti_exists=True
                    
                    if not ti_exists:
        #                print("\t\t\tCreate TI")
                        #Create this task instance
                        task = task_col.get_one(task_uuid)
                        pipeline = task.pipeline()#pipe_col.get_one(uuid=pipeline_uuid)
                        subject = session.subject()
        #                print("c")
                        metadata={
                            "title":f"{pipeline.title}/{task.title} ({task.field_operator}) on {subject.title}/{session.title}",
                            "field_associated_participant_ses":session.uuid,
                            "field_pipeline":pipeline_uuid,                                                                       
                            "field_task":task_uuid,
                            "cms_host":self.HOST  
                        }
        #                print(metadata)
                        ti = TaskInstance(metadata=metadata)
                        ti_uid=ti.upsert()
        #                print("TI upserted")
        #                print("e")


        else:
            raise Exception(f"Session is found on another compute node")
        

    

