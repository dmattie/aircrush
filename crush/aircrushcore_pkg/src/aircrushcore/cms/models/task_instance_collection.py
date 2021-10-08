
from aircrushcore.cms.models.task_instance import TaskInstance
import traceback
import uuid
import asyncio, asyncssh, sys
class TaskInstanceCollection():

    def __init__(self,**kwargs):    
        
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
            
    def __nvl(self,x,y):
        try:
            if x:
                print(f"\nxxxxxxxxxxxxxxx {x} xxxxxxxxxxxxxxx\n")
                return x
        except:
            return y
        
    def get(self,**kwargs):
        taskinstances={}    

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
            filter_session=f"&filter[field_associated_participant_ses.id][value]={self.session}"
        else:
            filter_session=""

        if self.task!=None:
            filter_task=f"&filter[field_task.id][value]={self.task}"
        else:
            filter_task=""
        if 'filter' in kwargs:
            filter=kwargs['filter']            
        else:
            filter=""

        

        url=f"jsonapi/node/task_instance?{filter_uuid}{filter_pipeline}{filter_session}{filter_task}{filter}"
        print(url)
        r = self.HOST.get(url)
        if r.status_code==200:  #We can connect to CRUSH host                       
            if len(r.json()['data'])!=0:

                for item in r.json()['data']:
                    print(".",end='')
                    if(item['type']=='node--task_instance'):
                        
                        uuid=item['id']

                        try:
                            body=item['attributes']['body']['value']
                        except:
                            body=""

                        try:
                            metadata={    
                                "title":item['attributes']['title']  ,                            
                                "field_pipeline":item['relationships']['field_pipeline']['data']['id'] ,   
                                "field_associated_participant_ses":item['relationships']['field_associated_participant_ses']['data']['id'],
                                "body":body,
                                "field_remaining_retries":item['attributes']['field_remaining_retries'],
                                "field_status":item['attributes']['field_status'],
                                "field_task":item['relationships']['field_task']['data']['id'],                            
                                "uuid":uuid,
                                "cms_host":self.HOST                                               
                            }
                            #print("\n\n------------------------------------\n\n")


                            taskinstances[item['id']]=TaskInstance(metadata=metadata)                
                        except:
                            print("ERROR:Some task instances may be malformed and ignored")
            return taskinstances
        else:      
            print(r.status_code)      
            return None

