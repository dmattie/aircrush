from aircrushcore.cms.models import *
class ComputeNode():
   
   
    def __init__(self,**kwargs):
        self.title=""                        
        self.field_host=""                
        self.field_username=""
        self.__field_password=""
        self.field_working_directory=""    
        self.body=""
        self.uuid=""  
        self.HOST=None    

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
                        "body":self.body                        
                    }                    
                }
            }

            if self.uuid:   #Update existing    
                payload.data.id=self.uuid                                                
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

    def allocate_session(self,session_uuid:str):
        if self.uuid is None:
            raise Exception("ComputeNode is new.  Save before allocation of sessions")

        pipe_col = PipelineCollection(cms_host=self.HOST)
        #Get Session
        sess_col = SessionCollection(cms_host=self.HOST)            
        sess = sess_col.get_one(uuid=session_uuid)

        #Look at existing task instances
        ti_col = TaskInstanceCollection(cms_host=self.HOST,session=session_uuid)
        ti_uuids = ti_col.get()

        ses_assigned_to_ti=None
        if not ti_uuids is None:
            #TIs exist for this session, let's see if they are with us or elsewhere
            #Get first task instance to determine allocated compute node    
            ti = ti_col.get_one(uuid=ti_uuids[0])
            ses_assigned_to_ti=ti.field_associated_participant_ses                 

        #If there are task instances assigned to this session or there are no task instances...
        if ses_assigned_to_ti is None or ses_assigned_to_ti==self.uuid:
            if sess.sticky==False: #not currently being allocated elsewhere
                sess.sticky=True  #Let's lock it up so it doesn't get allocated elsewhere
                sess.upsert()

            activated_pipelines = sess.project().field_activated_pipelines
            
            print(f"Activated pipelines for this session: {activated_pipelines}")
            sess.sticky=False
            sess.upsert()

            for pipeline_uuid in activated_pipelines:
                
                task_col = TaskCollection(cms_host=self.HOST,pipeline=pipeline_uuid)
                for task_uuid in task_col.get():
                    #Look for a task instance for this pipeline.task associated with this session
                    ti_col = TaskInstanceCollection(cms_host=self.HOST,pipeline=pipeline_uuid,task=task_uuid,session=session_uuid)
                    matching_tis = ti_col.get()
                    if matching_tis is None:
                        #Create this task instance
                        task = task_col.get_one(task_uuid)
                        pipeline = pipe_col.get_one(uuid=pipeline_uuid)
                        print(pipeline.title)
                        print(task.title)
                        print(sess.title)
                        new_title=f"{pipeline.title}/{task.title} on {sess.title}"
                        metadata={
                            "title":new_title,
                            "field_associated_participant_ses":session_uuid,
                            "field_pipeline":pipeline_uuid,                                                                       
                            "field_task":task_uuid,
                            "cms_host":self.HOST  
                        }
                        ti = TaskInstance(metadata=metadata)
                        ti_uid=ti.upsert()


        else:
            raise Exception(f"Session is found on another compute node")
        

    

