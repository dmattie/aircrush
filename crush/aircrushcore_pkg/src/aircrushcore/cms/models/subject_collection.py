
from aircrushcore.cms.models.subject import Subject
import traceback
import uuid
import asyncio, asyncssh, sys
class SubjectCollection():
    
    
    def __init__(self,**kwargs):    
        self.subjects={}    
        self.project=None
    

        if "cms_host" in kwargs:
            self.HOST=kwargs['cms_host']
            
        else:
            raise Exception("\nERROR:SubjectRepository::CMS host not specified\n")

        if "project" in kwargs:
            self.project=kwargs['project']
    
    #    self.getKnownParticipants()
    

    def get_one(self,uuid:str):
        col=self.get(uuid=uuid)        
        if(len(col)>0):
            x = col[list(col)[0]]
            return x
        else:
            return None
            
    def get(self,**kwargs):


        if 'uuid' in kwargs:
            uuid=kwargs['uuid']        
            filter_uuid=f"&filter[id][value]={uuid}"
        else:
            filter_uuid=""    

        if self.project!=None:
            filter=f"&filter[field_project.id][value]={self.project}"
        else:
            filter=""

        url=f"jsonapi/node/participant?{filter}{filter_uuid}"
        
        r = self.HOST.get(url)
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print(f"SubjectCollection:: No subjects found on CRUSH Host.[{url}]")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--participant'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_project":item['relationships']['field_project']['data']['id'] ,   
                            "field_status":item['attributes']['field_status'],
                            "uuid":uuid,
                            "cms_host":self.HOST                                               
                        }

                        self.subjects[item['id']]=Subject(metadata=metadata)                
            return self.subjects
        else:
            return None
