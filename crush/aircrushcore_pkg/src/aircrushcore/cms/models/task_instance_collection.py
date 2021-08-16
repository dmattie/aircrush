
from aircrushcore.cms.models.task_instance import TaskInstance
import traceback
import uuid
import asyncio, asyncssh, sys
class TaskInstanceCollection():

    def __init__(self,**kwargs):    
        self.taskinstances={}    
        self.pipeline=None   
        self.session=None
        self.task=None       

        if "cms_host" in kwargs:
            self.HOST=kwargs['cms_host']
            
        else:
            raise Exception("\nERROR:TaskCollection::CMS host not specified\n")

        if "pipeline" in kwargs:
            self.pipeline=kwargs['pipeline']        
        if "session" in kwargs:
            self.session=kwargs['session']
        if "task" in kwargs:
            self.task=kwargs['task']
    

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

        if self.pipeline!=None:
            filter_pipeline=f"&filter[field_pipeline.id][value]={self.pipeline}"
        else:
            filter_pipeline=""

        if self.session!=None:
            filter_session=f"&filter[field_session.id][value]={self.session}"
        else:
            filter_session=""

        if self.task!=None:
            filter_task=f"&filter[field_task.id][value]={self.task}"
        else:
            filter_task=""
        

        url=f"jsonapi/node/task_instance?{filter_uuid}{filter_pipeline}{filter_session}{filter_task}"
        
        r = self.HOST.get(url)
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print(f"TaskInstanceCollection:: No task instances found on CRUSH Host.[{url}]")                
            else:    
                  
                for item in r.json()['data']:
                    if(item['type']=='node--task_instance'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_pipeline":item['relationships']['field_pipeline']['data']['id'] ,   
                            "field_associated_participant_ses":item['relationships']['field_associated_participant_ses']['data']['id'],
                            "body":item['attributes']['body']['value'],
                            "field_remaining_retries":item['attributes']['field_remaining_retries'],
                            "field_status":item['attributes']['field_status'],
                            "field_task":item['relationships']['field_task']['data']['id'],                            
                            "uuid":uuid,
                            "cms_host":self.HOST                                               
                        }


                        self.taskinstances[item['id']]=TaskInstance(metadata=metadata)                
            return self.taskinstances
        else:
            return None

