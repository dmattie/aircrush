from . import crush
from ..Models import Pipeline
import traceback

class PipelineRepository():
    Pipelines={}
    
    def __init__(self,**kwargs):        
        username=kwargs['username']
        password=kwargs['password']
        endpoint=kwargs['endpoint']  

        self.HOST=crush.crush(
            endpoint="http://localhost:81/",
            username="crush",
            password="crush"
        )
        self.getKnownPipelines()

    def getKnownPipelines(self):
        r = self.HOST.get('jsonapi/node/pipeline')
        if r.status_code==200:  #We can connect to CRUSH host
            # Iterate the pipelines
            pipeline_count=0    
            if len(r.json()['data'])==0:
                print("PipelineRepository:: No pipelines found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--pipeline'):
                        pipeline_count=pipeline_count+1
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,  
                            "author":item['attributes']['field_author'],
                            "author_email":item['attributes']['field_author_email'],
                            "abstract":item['attributes']['body']['value'],                             
                        }

                        self.Pipelines[item['attributes']['field_id']]=Pipeline(item['attributes']['field_id'] ,metadata=metadata)                        

    def upsertPipeline(self,pipeline):
        
        try:            
            if pipeline.ID in self.Pipelines:
                print(f"PipelineRepository::found profile for [{pipeline.ID}] on CRUSH host, updating metadata")
                pass
                #Update
            else:
                print(f"PipelineRepository::New {pipeline.ID}, Inserting")
                #Insert
 
                payload = {"data" : {
                    "type":"node--pipeline",                    
                    "attributes":{
                        "field_author": pipeline.author, 
                        "title": pipeline.title,
                        "field_author_email":pipeline.author_email,
                        "body":pipeline.abstract,
                        "field_id":pipeline.ID
                    }               
                }}

                r= self.HOST.post("jsonapi/node/pipeline",payload)
                if(r.status_code!=201):
                    print(f"[ERROR] failed to create {ID} on CRUSH HOST: {r.status_code},  {r.reason}")
        except:
            if( not isinstance(pipeline,Pipeline)):
                print("Pipeline object not passed to upsert")
            else:
                 traceback.print_exc()


