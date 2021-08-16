
from aircrushcore.cms.models.pipeline import Pipeline
import traceback
import uuid
import asyncio, asyncssh, sys
class PipelineCollection():

    def __init__(self,**kwargs):    
        self.pipelines={}    
        
        if "cms_host" in kwargs:
            self.HOST=kwargs['cms_host']
            
        else:
            raise Exception("\nERROR:PipelineCollection::CMS host not specified\n")

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

        url=f"jsonapi/node/pipeline?{filter_uuid}"
        
        r = self.HOST.get(url)
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print(f"PipelineCollection:: No pipelines found on CRUSH Host.[{url}]")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--pipeline'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_author":item['attributes']['field_author'],   
                            "field_author_email":item['attributes']['field_author_email'],   
                            "body":item['attributes']['body'],
                            "field_id":item['attributes']['field_id'],
                            "field_plugin_warnings":item['attributes']['field_plugin_warnings'],
                            "uuid":uuid,
                            "cms_host":self.HOST                                               
                        }

                        self.pipelines[item['id']]=Pipeline(metadata=metadata)                
            return self.pipelines
        else:
            return None

