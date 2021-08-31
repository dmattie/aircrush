from aircrushcore.cms.models.subject import Subject
from aircrushcore.cms.models.subject_collection import SubjectCollection

class Session():
    
    def __init__(self,**kwargs):
               
        self.title=""                
        self.field_participant=""
        self.field_status=""
        self.uuid=None
        self.HOST=None
        self.published=True

        if 'metadata' in kwargs:
            m=kwargs['metadata']
        if 'title' in m:
            self.title=m['title']
        if 'field_participant' in m:
            self.field_participant=m['field_participant']
        if 'field_status' in m:
            self.field_status=m['field_status']      
        if 'uuid' in m:
            if m['uuid'] != "":
                self.uuid=m['uuid']
        if "cms_host" in m:
            self.HOST=m['cms_host']    
        if "published" in m:
            self.published=m['published']                 

    def upsert(self):

            payload = {
                "data" : {
                    "type":"node--session",                                                        
                    "attributes":{
                        "title": self.title,                                                    
                        "field_status": self.field_status,
                        "status":self.published
                    },
                    "relationships":{
                        "field_participant":{
                            "data":{
                                "type":"node--participant",
                                "id":self.field_participant
                            }
                        }                         
                    }              
                }
            }            
            if self.uuid:   #Update existing                  
                payload['data']['id']=self.uuid                                                                  
                r= self.HOST.patch(f"jsonapi/node/session/{self.uuid}",payload)                
            else:            
                r= self.HOST.post("jsonapi/node/session",payload)                     

            if(r.status_code!=200 and r.status_code!=201):  
                raise ValueError(f"Session upsert failed [{self.uuid}/{self.title}] on CMS HOST: {r.status_code}\n\t{r.reason}")                             
            else:    
                self.uuid= r.json()['data']['id']     
                return r.json()['data']['id']          

    def delete(self):
        if self.uuid:          
            r= self.HOST.delete(f"jsonapi/node/session/{self.uuid}")
        else: 
            return False
        
        if(r.status_code!=204):                   
            raise ValueError(f"Session deletion failed [{self.uuid}]")

        return True

    def subject(self):
        subject = SubjectCollection(cms_host=self.HOST).get_one(uuid=self.field_participant)
        return subject