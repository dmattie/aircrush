
from aircrushcore.cms.models.session import Session
import traceback
import uuid
import asyncio, asyncssh, sys
class SessionCollection():

    def __init__(self,**kwargs):    
        
        self.subject=None
        self.project=None
    

        if "cms_host" in kwargs:
            self.HOST=kwargs['cms_host']
            
        else:
            raise Exception("\nERROR:SessionCollection::CMS host not specified\n")

        if "subject" in kwargs:
            self.subject=kwargs['subject']              
    

    def get_one(self,uuid:str):
        col=self.get(uuid=uuid)        
        if(len(col)>0):
            x = col[list(col)[0]]
            return x
        else:
            return None
            
    def get(self,**kwargs):

        sessions={}    
        if 'uuid' in kwargs:
            uuid=kwargs['uuid']        
            filter_uuid=f"&filter[id][value]={uuid}"
        else:
            filter_uuid=""    

        if self.subject!=None:
            filter=f"&filter[field_participant.id][value]={self.subject}"
        else:
            filter=""

        if 'filter' in kwargs:
            custom_filter=kwargs['filter']
        else:
            custom_filter=""

        url=f"jsonapi/node/session?{filter}{filter_uuid}{custom_filter}"           
        r = self.HOST.get(url)
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])!=0:
            #    print(f"SessionCollection:: No sessions found on CRUSH Host.[{url}]")                
            #else:                     
                for item in r.json()['data']:
                    if(item['type']=='node--session'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_participant":item['relationships']['field_participant']['data']['id'] ,   
                            "field_responsible_compute_node": item['relationships']['field_responsible_compute_node']['data']['id'],
                            "field_status":item['attributes']['field_status'],
                            "uuid":uuid,
                            "sticky":item['attributes']['sticky'],
                            "cms_host":self.HOST                                               
                        }                                               
                        sessions[item['id']]=Session(metadata=metadata)                        
            return sessions
        else:
            return None

