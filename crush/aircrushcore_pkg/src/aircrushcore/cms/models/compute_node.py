from aircrushcore.cms.models import *
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
        sess_col = SessionCollection(cms_host=self.HOST)            
        sessions = sess_col.get(filter=f"&filter[field_responsible_compute_node.id][value]={self.uuid}")
        for ses in sessions:
            print(sessions[ses].title)
            self._establish_task_instances(sessions[ses])

    def _attach_to_session(self,session:session):
        if session.field_responsible_compute_node is None:
            session.field_responsible_compute_node=self.uuid
            session.upsert
        else:
            cn_coll = ComputeNodeCollection(cms_host=self.HOST)
            cn=cn_coll.get_one(session.field_responsible_compute_node)
            if cn is None:
                subject=session.subject()
                raise Exception("Session {subject.title}/{session.title} is allocated to a compute node that no longer exists.  Task instances may be orphaned")
            else:                
                raise Exception("Session is already allocated to a compute node")
        
    def _establish_task_instances(self,session:Session):
        

        #Look at existing task instances
        ti_col = TaskInstanceCollection(cms_host=self.HOST,session=session.uuid)
        tis = ti_col.get()

        ses_assigned_to_ti=None
        for ti in tis:
            #TIs exist for this session, let's see if they are with us or elsewhere
            #Get first task instance to determine allocated compute node               
            #ti = ti_col.get_one(uuid=ti_uuids[0])            
            ses_assigned_to_ti=tis[ti].field_associated_participant_ses
            break                 

        #If there are task instances assigned to this session or there are no task instances...
        print(f"session_assigned_to_ti:{ses_assigned_to_ti}, session:{session.uuid}")
        if ses_assigned_to_ti is None or ses_assigned_to_ti==session.uuid:
           
            activated_pipelines = session.project().field_activated_pipelines
            
            print(f"Activated pipelines for this session: {activated_pipelines}")
            

            for pipeline_uuid in activated_pipelines:
                print(f"Pipeline:{pipeline_uuid}")
                task_col = TaskCollection(cms_host=self.HOST,pipeline=pipeline_uuid)
                for task_uuid in task_col.get():
                    print(f"task uuid:{task_uuid}")
                                      
                    #Look for a task instance for this pipeline.task associated with this session
                    ti_col = TaskInstanceCollection(cms_host=self.HOST,pipeline=pipeline_uuid,task=task_uuid,session=session.uuid)
                    
                    matching_tis = ti_col.get()
                    
                    if len(matching_tis)==0:
                        print("Create TI")
                        #Create this task instance
                        task = task_col.get_one(task_uuid)
                        pipeline = task.pipeline()#pipe_col.get_one(uuid=pipeline_uuid)
                        print("c")
                        metadata={
                            "title":f"{pipeline.title}/{task.title} ({task.field_operator}) on {session.title}",
                            "field_associated_participant_ses":session.uuid,
                            "field_pipeline":pipeline_uuid,                                                                       
                            "field_task":task_uuid,
                            "cms_host":self.HOST  
                        }
                        print("d")
                        ti = TaskInstance(metadata=metadata)
                        ti_uid=ti.upsert()
                        print("TI upserted")
                        print("e")


        else:
            raise Exception(f"Session is found on another compute node")
        

    

