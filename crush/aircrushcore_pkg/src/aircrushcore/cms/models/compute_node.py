
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