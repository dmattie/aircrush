from . import crush
from ..workflow.pipeline import Pipeline
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
                        print(uuid)

    def upsertPipeline(self,pipeline):
        try:
            print("PipelineRepository:: Upserting")
            if pipeline.ID in self.Pipelines:
                pass
                #Update
            else:
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
                print(payload)

                r= self.HOST.post("jsonapi/node/pipeline",payload)
                if(r.status_code!=201):
                    print(f"[ERROR] failed to create {ID} on CRUSH HOST: {r.status_code},  {r.reason}")
        except:
            if( not isinstance(pipeline,Pipeline)):
                print("Pipeline object not passed to upsert")
            else:
                 traceback.print_exc()


