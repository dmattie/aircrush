
class Subject():
    
    def __init__(self,**kwargs):
               
        self.title=""                
        self.field_project=""
        self.field_status=""
        self.uuid=None
        self.isbids=""
        self.HOST=None

        if 'metadata' in kwargs:
            m=kwargs['metadata']
        if 'title' in m:
            self.title=m['title']
        if 'field_project' in m:
            self.field_project=m['field_project']
        if 'field_status' in m:
            self.field_status=m['field_status']      
        if 'uuid' in m:
            self.uuid=m['uuid']
        if 'isbids' in m:
            self.isbids=m['isbids']
        if "cms_host" in m:
            self.HOST=m['cms_host']             


    def upsert(self):

            payload = {
                "data" : {
                    "type":"node--participant",     
                    #  "id":self.uuid,                                 
                    "attributes":{
                        "title": self.title,                                                    
                        "field_status": self.field_status,
                    },
                    "relationships":{
                        "field_project":{
                            "data":{
                                "type":"node--project",
                                "id":self.field_project
                            }
                        }                         
                    }              
                }
            }

            if self.uuid:   #Update existing        
                payload.data.id=self.uuid                                                                  
                r= self.HOST.patch(f"jsonapi/node/participant/{self.uuid}",payload)                
            else:            
                r= self.HOST.post("jsonapi/node/participant",payload)

            if(r.status_code!=200 and r.status_code!=201):  
                 raise ValueError(f"Subject upsert failed [{self.uuid}/{self.title}] on CMS HOST: {r.status_code}\n\t{r.reason}")                             
            else:    
                self.uuid= r.json()['data']['id']     
                return r.json()['data']['id']          

    def delete(self):                  
        if self.uuid:          
            r= self.HOST.delete(f"jsonapi/node/participant/{self.uuid}")
        else: 
            return False
        
        if(r.status_code!=204):                   
            raise ValueError(f"Subject deletion failed [{self.uuid}]")

        return True