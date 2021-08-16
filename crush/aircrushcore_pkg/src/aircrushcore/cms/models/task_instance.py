
class TaskInstance():
    
    def __init__(self,**kwargs):
               
        self.title=""  
        self.field_associated_participant_ses=""
        self.field_pipeline=""
        self.body=""
        self.field_remaining_retries=""
        self.field_status=""
        self.field_task=""
        self.uuid=None
        self.HOST=None
    
        if 'metadata' in kwargs:
            m=kwargs['metadata']   
                
            if 'title' in m:
                self.title=m['title']        
            if 'field_associated_participant_ses' in m:
                self.field_associated_participant_ses=m['field_associated_participant_ses']
            if 'field_pipeline' in m:
                self.field_pipeline=m['field_pipeline']
            if 'body' in m:
                self.body=m['body']
            if 'field_remaining_retries' in m:
                self.field_remaining_retries=m['field_remaining_retries']
            if 'field_status' in m:
                self.field_status=m['field_status']
            if 'field_task' in m:
                self.field_task=m['field_task']
            if "cms_host" in m:
                self.HOST=m['cms_host']    
            if 'uuid' in m:
                self.uuid=m['uuid']                


    def upsert(self):

            payload = {
                "data" : {
                    "type":"node--task_instance",                                                         
                    "attributes":{
                        "title": self.title,                                                                            
                        "body":{
                            "value":self.body
                        },
                        "field_remaining_retries":self.field_remaining_retries,
                        "field_status":self.field_status
                    },
                    "relationships":{
                        "field_associated_participant_ses":{
                            "data":{
                                "id":self.field_associated_participant_ses,
                                "type":"node--session"
                            }
                        },
                        "field_pipeline":{
                            "data":{
                                "id":self.field_pipeline,
                                "type":"node--pipeline"
                            }
                        },
                        "field_task":{
                            "data":{
                                "id":self.field_task,
                                "type":"node--task"
                            }
                        }                                                                   
                    }              
                }
            }
            print(payload)
            if self.uuid:   #Update existing  
                
                payload.data.id=self.uuid                                                                  
                r= self.HOST.patch(f"jsonapi/node/task_instance/{self.uuid}",payload)                
            else:            
                r= self.HOST.post("jsonapi/node/task_instance",payload)

            if(r.status_code!=200 and r.status_code!=201):  
                 raise ValueError(f"TaskInstance upsert failed [{self.uuid}/{self.title}] on CMS HOST: {r.status_code}\n\t{r.reason}")                             
            else:    
                self.uuid= r.json()['data']['id']     
                return r.json()['data']['id']          

    def delete(self):
        if self.uuid:          
            r= self.HOST.delete(f"jsonapi/node/task_instance/{self.uuid}")
        else: 
            return False
        
        if(r.status_code!=204):                   
            raise ValueError(f"TaskInstance deletion failed [{self.uuid}]\n\t{r.status_code}\n\t{r.reason}]")

        return True            